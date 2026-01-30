import streamlit as st
from ai_engine import generate_affiliate_ideas

st.set_page_config(
    page_title="AI Affiliate Idea Generator",
    page_icon="🚀",
    layout="centered"
)

# ================= HEADER =================
st.title("🚀 AI Affiliate Idea Generator")
st.caption("Masukkan nama produk dan AI akan cadangkan idea video TikTok")
st.divider()

# ================= INPUT =================
st.subheader("📦 Maklumat Produk")

product_name = st.text_input(
    "Nama Produk",
    placeholder="Contoh: Apple iPad 11th Generation (WiFi)"
)

st.divider()

# ================= ACTION =================
if st.button("🚀 Generate Idea", use_container_width=True):
    if not product_name:
        st.warning("Sila masukkan nama produk.")
    else:
        with st.spinner("AI sedang jana idea..."):
            result = generate_affiliate_ideas(product_name)

        st.session_state["result"] = result

# ================= OUTPUT =================
if "result" in st.session_state:
    st.success("Idea berjaya dijana!")
    st.subheader("💡 Cadangan Kandungan")

    # CONFIRM PAPAR
    st.text(st.session_state["result"])
