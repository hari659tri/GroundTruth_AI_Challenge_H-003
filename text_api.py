import streamlit as st
from openai import OpenAI

# Load OpenAI key from secrets.toml
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_caption(prompt_image_desc: str, tone: str = "energetic", max_tokens: int = 30) -> str:
    """
    Generate a short, punchy caption using OpenAI.
    If API fails, returns fallback caption.
    """

    try:
        system_prompt = (
            "You are a creative ad copywriter. Produce a short, punchy marketing caption "
            "(<= 15 words) suitable for social media ads. No hashtags."
        )

        user_prompt = f"Image details: {prompt_image_desc}\nTone: {tone}\nWrite one caption."

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.8
        )

        text = response.choices[0].message["content"].strip()
        return text.split('\n')[0]

    except Exception:
        # fallback caption (first 10 words)
        words = prompt_image_desc.split()
        return " ".join(words[:10]) + "..."
