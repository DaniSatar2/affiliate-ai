import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openai/gpt-4o-mini"


def _build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Affiliate Idea Generator",
    }


def _extract_message_content(payload: dict) -> str:
    choices = payload.get("choices") or []
    if not choices:
        return ""

    message = choices[0].get("message") or {}
    content = message.get("content", "")

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                text_parts.append(part.get("text", ""))
        return "\n".join(part.strip() for part in text_parts if part.strip())

    return ""


def generate_affiliate_ideas(product_name: str, language: str) -> dict[str, str | bool]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {
            "ok": False,
            "content": "",
            "error": "OPENROUTER_API_KEY tidak dijumpai. Sila semak fail .env.",
        }

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
2. List 3-5 MAIN FEATURES of the product (based on general knowledge, estimation allowed).
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
""".strip()

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 700,
    }

    last_error = "AI sedang sibuk. Cuba lagi sebentar."

    for _ in range(3):
        try:
            response = requests.post(
                API_URL,
                headers=_build_headers(api_key),
                json=payload,
                timeout=30,
            )
        except requests.exceptions.RequestException as exc:
            return {
                "ok": False,
                "content": "",
                "error": f"Network error: {exc}",
            }

        if response.status_code == 200:
            try:
                body = response.json()
            except ValueError:
                return {
                    "ok": False,
                    "content": "",
                    "error": "API response tidak sah dan tidak boleh dibaca.",
                }

            content = _extract_message_content(body)
            if content:
                return {"ok": True, "content": content, "error": ""}

            return {
                "ok": False,
                "content": "",
                "error": "AI memulangkan output kosong.",
            }

        if response.status_code in (429, 500, 503):
            last_error = (
                f"Temporary API error ({response.status_code}). Sila cuba lagi."
            )
            time.sleep(2)
            continue

        error_text = response.text.strip() or "Unknown API error."
        return {
            "ok": False,
            "content": "",
            "error": f"API Error {response.status_code}: {error_text}",
        }

    return {"ok": False, "content": "", "error": last_error}
