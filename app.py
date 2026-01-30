import streamlit as st
from ai_engine import generate_affiliate_ideas

# ================= PARSER =================
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

# ================= DARK MODE =================
def set_theme(dark: bool):
    if dark:
        st.markdown("""
        <style>
        body, .stApp { background-color:#0e1117; color:#fafafa; }
        </style>
        """, unsafe_allow_html=True)

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Affiliate Idea Generator",
    page_icon="🚀",
    layout="centered"
)

# ================= STATE INIT =================
if "history" not in st.session_state:
    st.session_state.history = []

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ================= SIDEBAR =================
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)

set_theme(st.session_state.dark_mode)

# ================= HEADER =================
st.title("🚀 AI Affiliate Idea Generator")
st.caption("Masukkan nama produk → dapatkan idea video TikTok siap guna")
st.divider()

# ================= INPUT =================
product_name = st.text_input(
    "📦 Nama Produk",
    placeholder="Contoh: Logitech M331 Silent Mouse"
)

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

# ================= OUTPUT =================
if "result" in st.session_state:
    data = parse_ai_output(st.session_state.result)

    st.success("Idea berjaya dijana!")
    st.subheader("💡 Cadangan Kandungan")

    def card(title, content, color="info"):
        st.markdown(f"### {title}")
        getattr(st, color)(content)
        st.button("📋 Copy", key=title, on_click=lambda: st.toast("Disalin!"))

    card("🧠 Problem Statement", data.get("PROBLEM", "—"))
    
    st.markdown("### 🎬 Idea Video TikTok")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success(data.get("IDEA 1", "—"))
        st.button("📋 Copy", key="idea1")
    with col2:
        st.success(data.get("IDEA 2", "—"))
        st.button("📋 Copy", key="idea2")
    with col3:
        st.success(data.get("IDEA 3", "—"))
        st.button("📋 Copy", key="idea3")

    card("🎣 Hook (3 saat pertama)", data.get("HOOK", "—"), "warning")
    card("👉 Call To Action", data.get("CTA", "—"), "error")

    # ===== DOWNLOAD =====
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

# ================= HISTORY =================
if st.session_state.history:
    st.divider()
    st.subheader("📊 History Idea (Session)")

    for i, item in enumerate(st.session_state.history[:5], 1):
        with st.expander(f"{i}. {item['product']}"):
            st.text(item["result"])
