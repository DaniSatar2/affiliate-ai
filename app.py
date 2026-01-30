import streamlit as st
from ai_engine import generate_affiliate_ideas

# ---------- PARSER ----------
def parse_ai_output(text: str):
    keys = ["BRAND", "FEATURES", "PROBLEM", "IDEA 1", "IDEA 2", "IDEA 3", "HOOK", "CTA"]
    data = {}
    current = None

    for line in text.splitlines():
        line = line.strip()
        if line.endswith(":") and line[:-1] in keys:
            current = line[:-1]
            data[current] = ""
        elif current and line:
            data[current] += line + " "

    return data


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Affiliate Idea Generator",
    page_icon="🚀",
    layout="centered"
)

# ---------- SESSION STATE ----------
if "language" not in st.session_state:
    st.session_state.language = "BM"

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- HEADER ----------
st.title("🚀 AI Affiliate Idea Generator")
st.caption("Masukkan nama produk → pilih bahasa → AI jana idea TikTok")
st.divider()

# ---------- INPUT ----------
st.subheader("📦 Maklumat Produk")

product_name = st.text_input(
    "Nama Produk",
    placeholder="Contoh: Logitech M331 Silent Mouse"
)

# ---------- LANGUAGE SELECT (DI BAWAH INPUT) ----------
st.markdown("### 🌐 Pilihan Bahasa")

col_lang1, col_lang2 = st.columns(2)

with col_lang1:
    if st.button("🇲🇾 Bahasa Melayu", use_container_width=True):
        st.session_state.language = "BM"

with col_lang2:
    if st.button("🇬🇧 English", use_container_width=True):
        st.session_state.language = "EN"

st.caption(
    f"Bahasa dipilih: **{'Bahasa Melayu' if st.session_state.language == 'BM' else 'English'}**"
)

st.divider()

# ---------- ACTION ----------
if st.button("🚀 Generate Idea", use_container_width=True):
    if not product_name:
        st.warning("Sila masukkan nama produk.")
    else:
        with st.spinner("AI sedang jana idea..."):
            result = generate_affiliate_ideas(
                product_name=product_name,
                language=st.session_state.language
            )

        st.session_state.result = result
        st.session_state.history.insert(0, {
            "product": product_name,
            "language": st.session_state.language,
            "result": result
        })

# ---------- OUTPUT ----------
if "result" in st.session_state:
    data = parse_ai_output(st.session_state.result)

    st.success("Idea berjaya dijana!")
    st.subheader("💡 Cadangan Kandungan")

    st.markdown("### 🏷️ Brand")
    st.info(data.get("BRAND", "—"))

    st.markdown("### ⚙️ Features / Ciri-ciri")
    st.success(data.get("FEATURES", "—"))

    st.markdown("### 🧠 Problem Statement")
    st.info(data.get("PROBLEM", "—"))

    st.markdown("### 🎬 Idea Video TikTok")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(data.get("IDEA 1", "—"))
    with col2:
        st.success(data.get("IDEA 2", "—"))
    with col3:
        st.success(data.get("IDEA 3", "—"))

    st.markdown("### 🎣 Hook (3 saat pertama)")
    st.warning(data.get("HOOK", "—"))

    st.markdown("### 👉 Call To Action")
    st.error(data.get("CTA", "—"))

    # ---------- DOWNLOAD ----------
    st.download_button(
        "📥 Download Script (.txt)",
        data=st.session_state.result,
        file_name=f"{product_name}_{st.session_state.language}.txt",
        mime="text/plain"
    )

# ---------- HISTORY ----------
if st.session_state.history:
    st.divider()
    st.subheader("📊 History Idea (Session)")

    for i, item in enumerate(st.session_state.history[:5], 1):
        with st.expander(f"{i}. {item['product']} ({item['language']})"):
            st.text(item["result"])
