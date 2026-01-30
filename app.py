import streamlit as st
from ai_engine import generate_affiliate_ideas

st.set_page_config(page_title="AI Affiliate Link Assistant")

st.title("🔗 AI Affiliate Link Assistant")
st.write("Paste link produk Shopee / TikTok dan AI akan cadangkan idea video.")

product_link = st.text_input("Link Produk")

if st.button("Generate Idea"):
    if product_link:
        with st.spinner("AI sedang menganalisis produk..."):
            result = generate_affiliate_ideas(product_link)

        if result.startswith("⚠️") or result.startswith("❌"):
            st.warning(result)
        else:
            st.success("Idea berjaya dijana!")
            st.write(result)
    else:
        st.warning("Sila masukkan link produk.")
