import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "AI Affiliate Idea Generator"
}

def generate_affiliate_ideas(product_name: str, language: str) -> str:
    if language == "EN":
        lang_instruction = "Use English language. Casual and natural tone."
    else:
        lang_instruction = "Gunakan Bahasa Melayu yang santai dan natural."

    prompt = f"""
You are an affiliate marketing expert for TikTok.

Product:
{product_name}

Steps:
1. Identify the BRAND based on the product name.
2. List 3–5 MAIN FEATURES of the product (based on general knowledge, estimation allowed).
3. Use the information to generate affiliate content.

Respond in the following format (MUST follow exactly):

BRAND:
<brand name>

FEATURES:
- <feature 1>
- <feature 2>
- <feature 3>

PROBLEM:
<main user problem>

IDEA 1:
<first video idea>

IDEA 2:
<second video idea>

IDEA 3:
<third video idea>

HOOK:
<first 3-second spoken hook>

CTA:
<short call to action>

Language rule:
{lang_instruction}
"""

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 700
    }

    for _ in range(3):
        try:
            r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)

            if r.status_code == 200:
                content = r.json()["choices"][0]["message"]["content"]
                if content and content.strip():
                    return content
                return "⚠️ AI returned empty text."

            elif r.status_code in (429, 500, 503):
                time.sleep(2)
                continue
            else:
                return f"❌ API Error: {r.text}"

        except requests.exceptions.RequestException as e:
            return f"❌ Network error: {str(e)}"

    return "⚠️ AI is busy. Please try again."
