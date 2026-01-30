import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    # optional tapi elok (OpenRouter suka)
    "HTTP-Referer": "http://localhost",
    "X-Title": "AI Affiliate Link Assistant"
}

def generate_affiliate_ideas(product_link: str) -> str:
    prompt = f"""
Anda ialah pakar affiliate marketing TikTok & Shopee.

Berdasarkan link produk berikut:
{product_link}

Sila hasilkan:
1. Problem statement pengguna (1–2 ayat)
2. 3 idea video TikTok (angle berbeza & praktikal)
3. Hook 3 saat pertama (ayat spoken)
4. CTA ringkas

Gunakan Bahasa Melayu yang santai dan sesuai untuk content creator.
"""

    payload = {
        "model": "openai/gpt-4o-mini",  # 🔥 murah & padu
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 400
    }

    for _ in range(3):
        try:
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]

            time.sleep(2)

        except requests.exceptions.RequestException:
            time.sleep(2)

    return "⚠️ AI sedang sibuk. Sila cuba lagi sebentar."
