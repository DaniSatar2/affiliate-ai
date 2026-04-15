import re

import streamlit as st

from ai_engine import generate_affiliate_ideas

SECTION_KEYS = (
    "BRAND",
    "FEATURES",
    "PROBLEM",
    "IDEA 1",
    "IDEA 2",
    "IDEA 3",
    "HOOK",
    "CTA",
)


def parse_ai_output(text: str) -> dict[str, str]:
    data = {key: "" for key in SECTION_KEYS}
    current_key = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        match = re.match(
            r"^(BRAND|FEATURES|PROBLEM|IDEA 1|IDEA 2|IDEA 3|HOOK|CTA)\s*:\s*(.*)$",
            line,
        )

        if match:
            current_key = match.group(1)
            data[current_key] = match.group(2).strip()
            continue

        if current_key == "FEATURES":
            data[current_key] = "\n".join(
                part for part in (data[current_key], line) if part
            )
        elif current_key:
            data[current_key] = " ".join(
                part for part in (data[current_key], line) if part
            )

    return data


def has_structured_content(data: dict[str, str]) -> bool:
    required_sections = ("BRAND", "PROBLEM", "HOOK", "CTA")
    return all(data.get(section, "").strip() for section in required_sections)


def make_safe_filename(product_name: str, language: str) -> str:
    safe_name = re.sub(r'[<>:"/\\|?*]+', "", product_name).strip()
    safe_name = re.sub(r"\s+", "_", safe_name)

    if not safe_name:
        safe_name = "affiliate_idea"

    return f"{safe_name}_{language}.txt"


st.set_page_config(
    page_title="AI Affiliate Idea Generator",
    page_icon=":bulb:",
    layout="centered",
)

if "language" not in st.session_state:
    st.session_state.language = "BM"

if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

if "last_product" not in st.session_state:
    st.session_state.last_product = ""

if "last_language" not in st.session_state:
    st.session_state.last_language = st.session_state.language

st.title("AI Affiliate Idea Generator")
st.caption("Masukkan nama produk, pilih bahasa, dan jana idea konten TikTok.")
st.divider()

st.subheader("Maklumat Produk")

product_name = st.text_input(
    "Nama Produk",
    placeholder="Contoh: Logitech M331 Silent Mouse",
)

st.markdown("### Pilihan Bahasa")

col_lang1, col_lang2 = st.columns(2)

with col_lang1:
    if st.button("Bahasa Melayu", use_container_width=True):
        st.session_state.language = "BM"

with col_lang2:
    if st.button("English", use_container_width=True):
        st.session_state.language = "EN"

selected_language_label = (
    "Bahasa Melayu" if st.session_state.language == "BM" else "English"
)
st.caption(f"Bahasa dipilih: **{selected_language_label}**")

st.divider()

if st.button("Generate Idea", use_container_width=True):
    clean_product_name = product_name.strip()

    if not clean_product_name:
        st.warning("Sila masukkan nama produk.")
    else:
        with st.spinner("AI sedang jana idea..."):
            result = generate_affiliate_ideas(
                product_name=clean_product_name,
                language=st.session_state.language,
            )

        st.session_state.last_product = clean_product_name
        st.session_state.last_language = st.session_state.language
        st.session_state.result = result

        if result["ok"]:
            st.session_state.history.insert(
                0,
                {
                    "product": clean_product_name,
                    "language": st.session_state.language,
                    "result": result["content"],
                },
            )

if st.session_state.result:
    result = st.session_state.result

    if result["ok"]:
        data = parse_ai_output(result["content"])

        st.success("Idea berjaya dijana.")
        st.subheader("Cadangan Kandungan")

        st.markdown("### Brand")
        st.info(data.get("BRAND", "-") or "-")

        st.markdown("### Features / Ciri-ciri")
        st.success(data.get("FEATURES", "-") or "-")

        st.markdown("### Problem Statement")
        st.info(data.get("PROBLEM", "-") or "-")

        st.markdown("### Idea Video TikTok")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.success(data.get("IDEA 1", "-") or "-")
        with col2:
            st.success(data.get("IDEA 2", "-") or "-")
        with col3:
            st.success(data.get("IDEA 3", "-") or "-")

        st.markdown("### Hook")
        st.warning(data.get("HOOK", "-") or "-")

        st.markdown("### Call To Action")
        st.error(data.get("CTA", "-") or "-")

        if not has_structured_content(data):
            st.warning(
                "Output AI tidak ikut format sepenuhnya. Lihat output mentah di bawah."
            )

        with st.expander("Lihat output mentah"):
            st.text(result["content"])

        st.download_button(
            "Download Script (.txt)",
            data=result["content"],
            file_name=make_safe_filename(
                st.session_state.last_product,
                st.session_state.last_language,
            ),
            mime="text/plain",
        )
    else:
        st.error(result["error"])

if st.session_state.history:
    st.divider()
    st.subheader("History Idea (Session)")

    for i, item in enumerate(st.session_state.history[:5], 1):
        with st.expander(f"{i}. {item['product']} ({item['language']})"):
            st.text(item["result"])
