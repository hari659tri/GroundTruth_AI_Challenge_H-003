import requests
from io import BytesIO
from PIL import Image
import streamlit as st   # ✅ Use Streamlit secrets

# Load API key from secrets.toml
STABILITY_API_KEY = st.secrets["STABILITY_API_KEY"]


def generate_image_with_stability(prompt, width=1024, height=1024, model_name="sd3"):
    """
    Generate image using Stability API (SD3, Core, or Ultra)
    """

    if not STABILITY_API_KEY:
        raise Exception("Missing STABILITY_API_KEY in secrets.toml")

    # Map model names to real endpoints
    endpoints = {
        "sd3": "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        "core": "https://api.stability.ai/v2beta/stable-image/generate/core",
        "ultra": "https://api.stability.ai/v2beta/stable-image/generate/ultra"
    }

    if model_name not in endpoints:
        raise Exception(f"Invalid model_name '{model_name}'. Use sd3, core, or ultra.")

    url = endpoints[model_name]

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/*"
    }

    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
        "aspect_ratio": (None, "1:1")
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        raise Exception(f"Stability Error {response.status_code}: {response.text}")

    return Image.open(BytesIO(response.content))
