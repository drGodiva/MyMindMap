import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang mở rộng tối đa để có không gian vẽ sơ đồ
st.set_page_config(layout="wide", page_title="Người Mài Rìu - MindMap")

# Loại bỏ khoảng trắng dư thừa của Streamlit
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

# Đọc và hiển thị file HTML
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    # Nhúng giao diện với chiều cao 900px
    components.html(html_content, height=900, scrolling=True)
except FileNotFoundError:
    st.error("Không tìm thấy file index.html. Thầy kiểm tra lại đã up file HTML lên chưa nhé!")