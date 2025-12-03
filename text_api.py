# text_api.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    import openai
    openai.api_key = OPENAI_API_KEY
else:
    openai = None

def generate_caption(prompt_image_desc: str, tone: str = "energetic", max_tokens: int = 30) -> str:
    """
    Generate a short caption for an image via OpenAI (if key is provided).
    If OPENAI_API_KEY is not set, returns a simple fallback caption.
    """
    if not openai:
        # fallback: simple rule-based caption
        # keep it short, 10 words
        words = prompt_image_desc.split()
        short = " ".join(words[:10])
        return f"{short}..."
    try:
        system = (
            "You are a creative ad copywriter. Produce a short, punchy marketing caption "
            "(<= 15 words) suitable for social media ad. No hashtags.")
        user = f"Image details: {prompt_image_desc} \nWrite one caption."

        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini" if hasattr(openai, 'ChatCompletion') else "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=0.8,
        )
        text = resp['choices'][0]['message']['content'].strip()
        return text.split('\n')[0]
    except Exception as e:
        # fallback
        words = prompt_image_desc.split()
        short = " ".join(words[:10])
        return f"{short}..."
