import streamlit as st
from ai_engine import generate_affiliate_ideas

# ---------- Helper: Parse AI output ----------
def parse_ai_output(text: str):
    keys = ["PROBLEM", "IDEA 1", "IDEA 2", "IDEA 3", "HOOK", "CTA"]
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


# ---------- Page Config ----------
st.set_page_config(
    page_title="AI Affiliate Idea Generator",
    page_icon="🚀",
    layout="centered"
)

# ---------- Session State ----------
if "history" not in st.session_state:
    st.session_state.history = []

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

# ---------- Action ----------
if st.button("🚀 Generate Idea", use_container_width=True):
    if not product_name:
        st.warning("Sila masukkan nama produk.")
    else:
        with st.spinner("AI sedang jana idea..."):
            result = generate_affiliate_ideas(product_name)

        st.session_state.result = result
        st.session_state.history.insert(0, {
            "product": product_name,
            "result": result
        })

# ---------- Output ----------
if "result" in st.session_state:
    data = parse_ai_output(st.session_state.result)

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

    # ---------- Download ----------
    full_script = f"""
PROBLEM:
{data.get("PROBLEM","")}

IDEA 1:
{data.get("IDEA 1","")}

IDEA 2:
{data.get("IDEA 2","")}

IDEA 3:
{data.get("IDEA 3","")}

HOOK:
{data.get("HOOK","")}

CTA:
{data.get("CTA","")}
"""

    st.download_button(
        "📥 Download Skrip (.txt)",
        data=full_script,
        file_name=f"{product_name}_affiliate_idea.txt",
        mime="text/plain"
    )

# ---------- History ----------
if st.session_state.history:
    st.divider()
    st.subheader("📊 History Idea (Session)")

    for i, item in enumerate(st.session_state.history[:5], 1):
        with st.expander(f"{i}. {item['product']}"):
            st.text(item["result"])
