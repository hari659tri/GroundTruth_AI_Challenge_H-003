import streamlit as st
import tempfile
import uuid
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

from prompts import generate_prompts
from image_api import generate_image_with_stability
from text_api import generate_caption
from utils import ensure_dir, make_zip, save_metadata


# -------------------------------------
# STREAMLIT CONFIG
# -------------------------------------
st.set_page_config(page_title="Auto-Creative Engine", layout='wide')
st.title("Auto-Creative Engine — Generate 2 Ad Variations (Stability AI)")


# -------------------------------------
# SIDEBAR
# -------------------------------------
with st.sidebar:
    st.header("Settings")

    brand_name = st.text_input("Brand name", value="MyBrand")
    product_desc = st.text_input(
        "Short product description",
        value="wireless earbuds with charging case"
    )

    logo_pos = st.selectbox(
        "Logo position hint",
        ["top-left", "top-right", "bottom-left", "bottom-right"],
        index=0
    )

    # Hard limit max = 2
    num_variations = st.slider(
        "Number of variations",
        min_value=1,
        max_value=2,
        value=2
    )

    size = st.selectbox(
        "Output size",
        ["512", "768", "1024", "1536"],
        index=2
    )

    st.markdown("---")
    st.markdown("**Upload transparent PNG logo for best results.**")

    st.markdown("### Stability Model")
    model_name = st.selectbox(
        "Model",
        ["sd3", "core", "ultra"],
        index=0
    )


# -------------------------------------
# UPLOAD SECTION
# -------------------------------------
st.markdown("### Upload brand logo and product image")

col1, col2 = st.columns(2)
with col1:
    logo = st.file_uploader("Upload logo", type=["png", "jpg", "jpeg"])
with col2:
    product = st.file_uploader("Upload product image", type=["png", "jpg", "jpeg"])


# -------------------------------------
# MAIN GENERATE BUTTON
# -------------------------------------
if st.button("Generate Creatives"):

    if not logo or not product:
        st.error("Upload both logo & product first.")
        st.stop()

    # Temporary output folder
    tmpdir = tempfile.mkdtemp(prefix="autocreative_")
    out_dir = Path(tmpdir)
    ensure_dir(out_dir)

    # Save uploaded images
    logo_img = Image.open(logo).convert("RGBA")
    product_img = Image.open(product).convert("RGBA")
    logo_img.save(out_dir / "logo.png")
    product_img.save(out_dir / "product.png")

    # Generate prompts (max=2)
    prompts = generate_prompts(
        brand_name=brand_name,
        product_desc=product_desc,
        logo_pos_hint=logo_pos,
        n=2
    )[:2]

    files_for_zip = []
    metadata = {"brand": brand_name, "product": product_desc, "items": []}

    progress = st.progress(0.0)
    img_cols = st.columns(3)

    # -------------------------------------
    # IMAGE GENERATION LOOP
    # -------------------------------------
    for i, prompt in enumerate(prompts, start=1):

        st.write(f"### Generating Image {i}/2")

        # Stability AI call
        try:
            img = generate_image_with_stability(
                prompt=prompt,
                width=int(size),
                height=int(size),
                model_name=model_name
            )
        except Exception as e:
            st.error(f"Error generating image {i}: {e}")
            continue

        if img.mode != "RGBA":
            img = img.convert("RGBA")

        composite = Image.new("RGBA", img.size)
        composite.paste(img, (0, 0))

        # -------------------------------------
        # LOGO OVERLAY
        # -------------------------------------
        try:
            logo_copy = logo_img.copy()
            max_w = img.width // 6
            ratio = max_w / logo_copy.width

            logo_copy = logo_copy.resize(
                (int(logo_copy.width * ratio), int(logo_copy.height * ratio)),
                Image.Resampling.LANCZOS
            )

            pos = {
                "top-left": (10, 10),
                "top-right": (img.width - logo_copy.width - 10, 10),
                "bottom-left": (10, img.height - logo_copy.height - 10),
                "bottom-right": (img.width - logo_copy.width - 10,
                                 img.height - logo_copy.height - 10),
            }

            composite.paste(logo_copy, pos[logo_pos], mask=logo_copy)

        except Exception as e:
            st.warning(f"Logo overlay failed: {e}")

        # Save file
        out_img_path = out_dir / f"creative_{i}.png"
        composite.save(out_img_path)

        # Generate caption
        caption_prompt = f"Brand: {brand_name}. Product: {product_desc}. Style: {prompt}"
        caption = generate_caption(caption_prompt)

        caption_path = out_dir / f"caption_{i}.txt"
        caption_path.write_text(caption)

        # Add files for ZIP
        files_for_zip.append((str(out_img_path), out_img_path.name))
        files_for_zip.append((str(caption_path), caption_path.name))

        metadata["items"].append({
            "image": out_img_path.name,
            "caption": caption,
            "prompt": prompt
        })

        # SHOW IMAGE IN UI
        with img_cols[(i - 1) % 3]:
            st.image(out_img_path, caption=f"Creative {i}")

        progress.progress(i / 2)

    # Metadata
    meta_path = out_dir / "metadata.json"
    save_metadata(metadata, meta_path)
    files_for_zip.append((str(meta_path), meta_path.name))

    # ZIP final output
    zip_name = f"{brand_name}_creatives_{uuid.uuid4().hex[:6]}.zip"
    zip_path = out_dir / zip_name
    make_zip(zip_path, files_for_zip)

    st.success("🎉 Generated exactly 2 creatives!")

    with open(zip_path, "rb") as f:
        st.download_button(
            "Download ZIP",
            data=f,
            file_name=zip_name,
            mime="application/zip"
        )
