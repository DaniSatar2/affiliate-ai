import streamlit as st
from ai_engine import generate_affiliate_ideas

# ---------- Helper: Parse AI output ----------
def parse_ai_output(text: str):
    sections = {}
    current_key = None
    valid_keys = ["PROBLEM", "IDEA 1", "IDEA 2", "IDEA 3", "HOOK", "CTA"]

    for line in text.splitlines():
        line = line.strip()
        if line.endswith(":") and line[:-1] in valid_keys:
            current_key = line[:-1]
            sections[current_key] = ""
        elif current_key and line:
            sections[current_key] += line + " "

    return sections


# ---------- Page Config ----------
st.set_page_config(
    page_title="AI Affiliate Idea Generator",
    page_icon="🚀",
    layout="centered"
)

# ---------- Header ----------
st.title("🚀 AI Affiliate Idea Generator")
st.caption("Masukkan nama produk dan dapatkan idea video TikTok secara automatik")
st.divider()

# ---------- Input ----------
st.subheader("📦 Maklumat Produk")

product_name = st.text_input(
    "Nama Produk",
    placeholder="Contoh: Logitech M331 Silent Mouse"
)

st.divider()

# ---------- Action ----------
if st.button("🚀 Generate Idea", use_container_width=True):
    if not product_name:
        st.warning("Sila masukkan nama produk.")
    else:
        with st.spinner("AI sedang jana idea..."):
            result = generate_affiliate_ideas(product_name)

        st.session_state["result"] = result

# ---------- Output ----------
if "result" in st.session_state:
    data = parse_ai_output(st.session_state["result"])

    st.success("Idea berjaya dijana!")
    st.subheader("💡 Cadangan Kandungan")

    # Problem
    st.markdown("### 🧠 Problem Statement")
    st.info(data.get("PROBLEM", "—"))

    # Ideas
    st.markdown("### 🎬 Idea Video TikTok")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(data.get("IDEA 1", "—"))

    with col2:
        st.success(data.get("IDEA 2", "—"))

    with col3:
        st.success(data.get("IDEA 3", "—"))

    # Hook
    st.markdown("### 🎣 Hook (3 saat pertama)")
    st.warning(data.get("HOOK", "—"))

    # CTA
    st.markdown("### 👉 Call To Action")
    st.error(data.get("CTA", "—"))
