import streamlit as st
from ai_engine import generate_affiliate_ideas, extract_product_name

st.set_page_config(
    page_title="AI Affiliate Link Assistant",
    page_icon="🔗",
    layout="centered"
)

# ---------- HEADER ----------
st.title("🔗 AI Affiliate Link Assistant")
st.caption("Tukar link produk kepada idea video TikTok secara automatik")

st.divider()

# ---------- INPUT SECTION ----------
st.subheader("📦 Maklumat Produk")

product_link = st.text_input(
    "Link Produk (Shopee / TikTok)",
    placeholder="https://shopee.com.my/..."
)

product_name = ""
if product_link:
    product_name = extract_product_name(product_link)

product_name = st.text_input(
    "Nama Produk (boleh edit)",
    value=product_name,
    placeholder="Contoh: Logitech M331 Silent Mouse"
)

st.divider()

# ---------- ACTION ----------
if st.button("🚀 Generate Idea", use_container_width=True):
    if not product_link or not product_name:
        st.warning("Sila masukkan link dan nama produk.")
    else:
        with st.spinner("AI sedang jana idea..."):
            result = generate_affiliate_ideas(
                product_link=product_link,
                product_name=product_name
            )

        if result.startswith("⚠️"):
            st.warning(result)
        else:
            st.success("Idea berjaya dijana!")
            st.session_state["result"] = result

# ---------- OUTPUT ---------
