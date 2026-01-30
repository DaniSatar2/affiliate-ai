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

Langkah:
1. Kenal pasti BRAND berdasarkan nama produk.
2. Senaraikan 3–5 CIRI UTAMA produk (berdasarkan pengetahuan umum, anggaran dibenarkan).
3. Gunakan maklumat tersebut untuk bina kandungan affiliate.

Sila jawab dalam format berikut (WAJIB ikut):

BRAND:
<nama brand>

CIRI:
- <ciri 1>
- <ciri 2>
- <ciri 3>

PROBLEM:
<problem utama pengguna>

IDEA 1:
<idea video pertama>

IDEA 2:
<idea video kedua>

IDEA 3:
<idea video ketiga>

HOOK:
<hook 3 saat pertama (ayat spoken)>

CTA:
<call to action ringkas>

Gunakan Bahasa Melayu yang santai dan natural.
"""

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 700
    }

    for _ in range(3):
        try:
            r = requests.post(
                API_URL,
                headers=HEADERS,
                json=payload,
                timeout=30
            )

            if r.status_code == 200:
                content = r.json()["choices"][0]["message"]["content"]
                if content and content.strip():
                    return content
                return "⚠️ AI tidak memulangkan teks."

            elif r.status_code in (429, 500, 503):
                time.sleep(2)
                continue

            else:
                return f"❌ Ralat API: {r.text}"

        except requests.exceptions.RequestException as e:
            return f"❌ Ralat rangkaian: {str(e)}"

    return "⚠️ AI sedang sibuk. Sila cuba lagi."
