import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenRouter API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    # Optional tapi bagus untuk OpenRouter analytics
    "HTTP-Referer": "http://localhost",
    "X-Title": "AI Affiliate Link Assistant"
}

# --------------------------------------------------
# Helper: Extract product name from Shopee URL
# --------------------------------------------------
def extract_product_name(shopee_url: str) -> str:
    """
    Extract nama produk dari URL Shopee.
    Contoh:
    https://shopee.com.my/Logitech-M331-Silent-Plus-Mouse-i.123.456
    -> Logitech M331 Silent Plus Mouse
    """
    try:
        slug = shopee_url.split("/")[-1]
        name_part = slug.split("-i.")[0]
        clean_name = name_part.replace("-", " ")
        return clean_name.title()
    except Exception:
        return ""

# --------------------------------------------------
# Main AI function
# --------------------------------------------------
def generate_affiliate_ideas(product_link: str, product_name: str) -> str:
    prompt = f"""
Anda ialah pakar affiliate marketing TikTok & Shopee.

Maklumat produk:
Nama produk: {product_name}
Link produk: {product_link}

Tugasan:
1. Tulis Problem Statement utama pengguna (1–2 ayat, fokus masalah harian)
2. Cadangkan 3 idea video TikTok (setiap satu angle berbeza & praktikal)
3. Tulis Hook 3 saat pertama (ayat spoken, ringkas & menarik)
4. Tulis CTA ringkas sesuai untuk TikTok

Gunakan Bahasa Melayu yang santai, natural dan sesuai untuk content creator.
Jangan guna ayat terlalu formal.
"""

    payload = {
        "model": "openai/gpt-4o-mini",  # murah + padu
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 400
    }

    # Retry mechanism
    for attempt in range(3):
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

            # Rate limit / server busy
            elif response.status_code in (429, 500, 503):
                time.sleep(2)
                continue

            else:
                return (
                    "⚠️ AI tidak dapat menjana idea buat masa ini.\n\n"
                    f"Maklumat ralat: {response.text}"
                )

        except requests.exceptions.Timeout:
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            return f"❌ Ralat rangkaian: {str(e)}"

    return (
        "⚠️ AI sedang sibuk selepas beberapa percubaan.\n"
        "Sila cuba semula sebentar lagi."
    )
