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

def generate_affiliate_ideas(product_name: str) -> str:
    prompt = f"""
Anda ialah pakar affiliate marketing TikTok.

Produk:
{product_name}

Sila hasilkan:
1. Problem statement utama pengguna (1–2 ayat)
2. 3 idea video TikTok (setiap satu angle berbeza)
3. Hook 3 saat pertama (ayat spoken)
4. CTA ringkas yang sesuai untuk TikTok

Gunakan Bahasa Melayu yang santai, ringkas dan mudah difahami.
"""

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    for _ in range(3):
        try:
            res = requests.post(
                API_URL,
                headers=HEADERS,
                json=payload,
                timeout=30
            )

            if res.status_code == 200:
                data = res.json()
                content = data["choices"][0]["message"]["content"]

                if content and content.strip():
                    return content
                else:
                    return "⚠️ AI tidak memulangkan sebarang teks."

            elif res.status_code in (429, 500, 503):
                time.sleep(2)
                continue

            else:
                return f"❌ Ralat API: {res.text}"

        except requests.exceptions.RequestException as e:
            return f"❌ Ralat rangkaian: {str(e)}"

    return "⚠️ AI sedang sibuk. Sila cuba lagi sebentar."
