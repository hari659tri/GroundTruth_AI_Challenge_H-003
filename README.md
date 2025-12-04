
<body>

<h1>Auto-Creative Engine — AI Ad Creative Generator</h1>
<p class="muted"> Auto-Creative Engine is a web application built using Streamlit and Stability AI’s Stable Diffusion models. It allows users to generate high-quality ad creatives automatically by uploading a brand logo and product image, creating AI-powered visuals, adding logos, generating captions, and exporting everything as a downloadable ZIP file using Streamlit and Stability AI (SD3 / Core / Ultra).<br> Upload brand logo & product image → generate 2 high-quality ad variations → auto captions → ZIP export.<br>

</p>

<h2>Why Stable Diffusion?</h2>
<p> 
High-quality image generation: Stable Diffusion models (SD3, SDXL, Core, Ultra) produce realistic and artistic visuals suitable for marketing ads.
Customizable prompts: By generating dynamic prompts based on brand and product information, you can produce unique variations automatically.
Flexible API: Stability AI provides a REST API, which allows generating images in different styles, resolutions, and model types, making it easy to integrate into Python pipelines.
</p>

<h2>Quick Summary</h2>
<div class="card">
  <p><strong>What it does:</strong> Generates exactly <code>2</code> ad creatives per run using a Stability AI image model, composites your uploaded brand logo, generates a short caption, and packages results in a ZIP file (<code>images + captions + metadata.json</code>).</p>
  <p><strong>Tech stack:</strong> Python • Streamlit • Pillow • Requests • Stability AI Image API • OpenAI (optional captions)</p>
</div>

🔗 [StabilityAI API Key Testing](https://colab.research.google.com/drive/1RPxCZBJwzShAocupXbgWRjfewA5eYQfx?usp=sharing) <br>
🔗 [Demo](https://youtu.be/pOG89b-GmEM)

## 📸 Screenshot

<img width="1359" height="732" alt="Screenshot 2025-12-04 033109" src="https://github.com/user-attachments/assets/5bcf5a88-9d21-4b4d-ae09-d60ccb8cf14e" />

<img width="1366" height="768" alt="Screenshot 2025-12-03 234155" src="https://github.com/user-attachments/assets/53b90525-b101-4699-8c4d-9d79a255fef1" />

<img width="1366" height="768" alt="Screenshot 2025-12-03 234640" src="https://github.com/user-attachments/assets/4c9bb9e7-930e-4f16-a2bc-e7151b87e6d7" />

<img width="1366" height="768" alt="Screenshot 2025-12-03 121534" src="https://github.com/user-attachments/assets/2b452fbb-ed05-41b0-974f-913b5b5f28b6" />

<img width="1366" height="768" alt="Screenshot 2025-12-03 140317" src="https://github.com/user-attachments/assets/d4d7f975-5e61-4dc6-95c8-556af6116da3" />

<img width="796" height="484" alt="Screenshot 2025-12-04 115844" src="https://github.com/user-attachments/assets/8a9ceb52-87f2-4c7f-a5d5-b9d020784e38" />

<h2>Architecture & Pipeline</h2>
<pre>
User (browser)
  └─ Streamlit UI (app.py)
       ├─ Upload: logo + product, brand name, description, options
       ├─ Prompt generator (prompts.py) → produce 2 prompts
       ├─ Image generation (image_api.py) → Stability API (sd3 / core / ultra)
       ├─ Postprocessing: convert → composite with uploaded logo
       ├─ Caption generation (text_api.py) → OpenAI or HF fallback
       └─ Packaging: save images, captions, metadata.json → ZIP
</pre>

<h2>Key Files</h2>
<ul>
  <li><code>app.py</code> — Streamlit front-end and orchestration</li>
  <li><code>image_api.py</code> — Stability AI image API wrapper (multipart/form-data)</li>
  <li><code>prompts.py</code> — Prompt templates + generator</li>
  <li><code>text_api.py</code> — Caption generation (OpenAI or HuggingFace fallback)</li>
  <li><code>utils.py</code> — Helpers: ensure_dir, make_zip, save_metadata</li>
  <li><code>.env</code> — Environment variables (<code>STABILITY_API_KEY</code>, optional <code>OPENAI_API_KEY</code>)</li>
</ul>

<h2>Pipeline Flow (Code Style)</h2>
<h3>1) Inputs (Streamlit)</h3>
<pre>
brand_name = st.text_input("Brand name")
product_desc = st.text_input("Product description")
logo = st.file_uploader("Logo")
product = st.file_uploader("Product image")
size = st.selectbox("Output size", ["512","768","1024","1536"])
model_name = st.selectbox("Model", ["sd3","core","ultra"])
</pre>

<h3>2) Prompt Generation</h3>
<pre>
prompts = generate_prompts(
    brand_name=brand_name,
    product_desc=product_desc,
    logo_pos_hint=logo_pos,
    n=num_variations
)
prompts = prompts[:2]   # hard limit to 2
</pre>

<h3>3) Image Generation (Stability AI)</h3>
<p class="muted">Important: Stability requires <code>multipart/form-data</code> requests and uses endpoints such as <code>/v2beta/stable-image/generate/sd3</code>, <code>/.../core</code>, or <code>/.../ultra</code>.</p>
<pre>
ENDPOINTS = {
  "sd3": "https://api.stability.ai/v2beta/stable-image/generate/sd3",
  "core": "https://api.stability.ai/v2beta/stable-image/generate/core",
  "ultra": "https://api.stability.ai/v2beta/stable-image/generate/ultra"
}

files = {
  "prompt": (None, prompt),
  "output_format": (None, "png"),
  "aspect_ratio": (None, "1:1")
}
response = requests.post(url, headers=headers, files=files)
image = Image.open(BytesIO(response.content))
</pre>

<h3>4) Logo Overlay (Pillow)</h3>
<pre>
logo_copy = logo_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
composite = Image.new("RGBA", img.size)
composite.paste(img, (0,0))
composite.paste(logo_copy, position, mask=logo_copy)
</pre>

<h3>5) Caption Generation</h3>
<pre>
caption = generate_caption(f"Brand: {brand}. Product: {product}. Image style: {prompt}")
</pre>

<h3>6) Packaging & Export</h3>
<pre>
files_for_zip = [(creative_path, creative_name), (caption_path, caption_name), (metadata.json)]
make_zip(zip_path, files_for_zip)
st.download_button("Download ZIP", data=open(zip_path,"rb"), file_name=zip_name)
</pre>

<h2>Endpoints & Models</h2>
<table>
  <tr><th>Model Key</th><th>Endpoint</th><th>Notes</th></tr>
  <tr><td>sd3</td><td>/v2beta/stable-image/generate/sd3</td><td>High-quality artistic & realistic</td></tr>
  <tr><td>core</td><td>/v2beta/stable-image/generate/core</td><td>Balanced, lower cost</td></tr>
  <tr><td>ultra</td><td>/v2beta/stable-image/generate/ultra</td><td>Highest detail & cost</td></tr>
</table>

<h2>Main Challenges</h2>
<ul>
  <li>404 Not Found: wrong endpoint/model → use above endpoints</li>
  <li>Multipart/form-data required: send prompt via <code>files</code>, not JSON</li>
  <li>API credits / rate limits: limit images to 2 per run</li>
  <li>Pillow breaking changes: <code>Image.ANTIALIAS</code> removed → use <code>Image.Resampling.LANCZOS</code></li>
  <li>Streamlit hosting: no GPU → remote API call required</li>
</ul>

<h2>API Keys</h2>
<pre>
# .env (repo root)
STABILITY_API_KEY=sk-xxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxx   # optional
</pre>
<p class="muted">Get Stability key: <a href="https://platform.stability.ai/" target="_blank">https://platform.stability.ai/</a></p>

<h2>Example Prompts (Robot-Themed)</h2>
<pre>
# prompt 1 (realistic)
A highly detailed futuristic humanoid robot standing in a sci-fi environment. Metallic body, glowing LED eyes, ultra-realistic textures, cinematic lighting, sharp details, 8K render.

# prompt 2 (friendly mascot)
A cute friendly robot character with round features, glowing blue eyes, and a soft white plastic body. Pixar-style design, colorful environment, soft shadows, HD quality.
</pre>

<h2>Run Locally</h2>
<pre>
# 1. create venv & install
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 2. set .env
STABILITY_API_KEY and (optional) OPENAI_API_KEY

# 3. run
streamlit run app.py
</pre>

<h2>requirements.txt</h2>
<pre>
streamlit
Pillow
python-dotenv
requests
openai   # optional for captions
</pre>

<h2>Output Structure (ZIP)</h2>
<pre>
brand_creatives_abc123.zip
├─ creative_1.png
├─ caption_1.txt
├─ creative_2.png
├─ caption_2.txt
└─ metadata.json
</pre>

<h2>License & Credits</h2>
<p class="muted">MIT-like license for demo/hackathon use. Built by <strong>Harikesh Tripathi</strong>.</p>

</body>
</html>
