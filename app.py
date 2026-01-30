import streamlit as st
from ai_engine import generate_affiliate_ideas, extract_product_name

st.set_page_config(
    page_title="AI Affiliate Link Assistant",
    page_icon="🔗",
    layout="centered"
)

# ================= HEADER =================
st.title("🔗 AI Affiliate Link Assistant")
st.caption("Tukar link produk kepada idea video TikTok secara automatik")
st.divider()

# ================= INPUT =================
st.subheader("📦 Maklumat Produk")

product_link = st.text_input(
    "Link Produk (Shopee / TikTok)",
    placeholder="https://shopee.com.my/..."
)

auto_name = extract_product_name(product_link) if product_link else ""

product_name = st.text_input(
    "Nama Produk (boleh edit)",
    value=auto_name,
    placeholder="Contoh: Apple iPad 11th Generation"
)

st.divider()

# ================= ACTION =================
if st.button("🚀 Generate Idea", use_container_width=True):
    if not product_link or not product_name:
        st.warning("Sila masukkan link dan nama produk.")
    else:
        with st.spinner("AI sedang jana idea..."):
            result = generate_affiliate_ideas(
                product_link=product_link,
                product_name=product_name
            )

        # SIMPAN RESULT
        st.session_state["result"] = result

# ================= OUTPUT =================
if "result" in st.session_state:
    st.success("Idea berjaya dijana!")
    st.subheader("💡 Cadangan Kandungan")

    # GUNA st.text → CONFIRM PAPAR
    st.text(st.session_state["result"])
