# prompts.py
from typing import List

BASE_TEMPLATES = [
    "Minimal premium product ad with white background and centered product. Include logo at top-left.",
    "Festive theme ad with warm tones, decorative patterns, product in center, logo bottom-right.",
    "Lifestyle ad: product in use with soft bokeh background and call-to-action overlay.",
    "Bold social-media square: high-contrast colors, large headline space, product on right.",
    "Premium spotlight: dark background, dramatic rim light on product, logo subtle.",
    "Eco-friendly theme: green hues, natural textures, product on wooden surface.",
    "Flat illustration style: simplified shapes, playful mood, big CTA area.",
    "Monochrome modern: grayscale palette with a single accent color from the brand.",
    "Product-on-isolated-surface: shadow underneath, very clean studio shot.",
    "Retro poster style with bold geometric shapes and vintage typography.",
]

def generate_prompts(brand_name: str, product_desc: str, logo_pos_hint: str = "top-left", n: int = 10) -> List[str]:
    """Generate n prompts mixing base templates with brand/product info."""
    prompts = []
    for i in range(n):
        template = BASE_TEMPLATES[i % len(BASE_TEMPLATES)]
        prompt = (
            f"{template} "
            f"Show the product: {product_desc}. "
            f"Include the brand name '{brand_name}' and place the logo {logo_pos_hint}. "
            "High-resolution, photorealistic where applicable, clean composition."
        )
        prompts.append(prompt)
    return prompts
