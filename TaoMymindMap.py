import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Người Mài Rìu - AI MindMap")

st.markdown("""
    <style>
        .block-container { padding: 0rem; }
    </style>
""", unsafe_allow_html=True)

try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Tiêm khóa từ Két sắt Secrets vào bộ nhớ trình duyệt
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        inject_script = f"<script>localStorage.setItem('geminiApiKey', '{api_key}');</script>"
        html_content = html_content.replace('</body>', inject_script + '</body>')
    else:
        st.warning("⚠️ Chưa cấu hình GEMINI_API_KEY trong Secrets.")

    components.html(html_content, height=900, scrolling=True)
except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file index.html.")