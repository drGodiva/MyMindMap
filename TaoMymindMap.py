import streamlit as st
import streamlit.components.v1 as components

# Mở rộng toàn màn hình để có không gian vẽ sơ đồ
st.set_page_config(layout="wide", page_title="Người Mài Rìu - AI MindMap")

# Ép sát viền, loại bỏ khoảng trắng dư thừa của Streamlit
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

try:
    # Mở cuộn băng giao diện HTML
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Rút chìa khóa từ Két sắt (Secrets) và bí mật tiêm vào bộ nhớ trình duyệt của người dùng
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        inject_script = f"<script>localStorage.setItem('geminiApiKey', '{api_key}');</script>"
        html_content = html_content.replace('</body>', inject_script + '</body>')
    else:
        st.warning("⚠️ Chưa tìm thấy chìa khóa API trong két sắt Secrets của Streamlit.")

    # Phát giao diện lên màn hình
    components.html(html_content, height=900, scrolling=True)

except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file index.html. Thầy kiểm tra lại đã up file HTML lên chưa nhé!")