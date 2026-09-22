import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

st.set_page_config(layout="wide", page_title="Người Mài Rìu - AI MindMap")

st.markdown("""
    <style>
        .block-container { padding: 0rem; }
    </style>
""", unsafe_allow_html=True)

# 1. Cấu hình API Gemini bằng Két sắt Secrets an toàn tuyệt đối
api_key_status = "Chưa có"
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        api_key_status = "Đang hoạt động"
    except Exception as e:
        api_key_status = f"Lỗi: {str(e)}"

# 2. Xử lý yêu cầu gọi AI từ JavaScript gửi ngược về Python
query_params = st.query_params
if "action" in query_params and query_params["action"] == "ask_ai":
    st.set_page_config(page_title="API Response", layout="centered")
    node_label = query_params.get("node", "")
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt_str = f'Tôi đang vẽ sơ đồ tư duy. Hãy liệt kê 3 đến 5 ý phụ thật ngắn gọn (tối đa 5 từ mỗi ý) để phát triển cho từ khóa: "{node_label}". TRẢ VỀ DUY NHẤT MỘT MẢNG JSON hợp lệ chứa các chuỗi, ví dụ: ["ý 1", "ý 2", "ý 3"]. Tuyệt đối không giải thích thêm, không có dấu markdown.'
        
        response = model.generate_content(prompt_str)
        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        
        # Trả về kết quả JSON sạch 100%
        st.write(json.dumps({"success": True, "ideas": json.loads(raw_text)}))
    except Exception as e:
        st.write(json.dumps({"success": False, "error": str(e)}))
    st.stop()

# 3. Đọc file HTML giao diện
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Tiêm trạng thái báo cáo vào giao diện
    status_script = f"<script>window.isBackendReady = true;</script>"
    html_content = html_content.replace('</body>', status_script + '</body>')

    components.html(html_content, height=900, scrolling=True)
except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file index.html trên GitHub.")