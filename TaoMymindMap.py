import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

# =========================================================================
# 1. KHU VỰC XỬ LÝ NGẦM (BACKEND API PROXY) - ĐẶT LÊN TRÊN CÙNG
# =========================================================================
query_params = st.query_params
if "action" in query_params and query_params["action"] == "ask_ai":
    # Xóa sạch toàn bộ giao diện mặc định của Streamlit, chỉ in ra JSON
    st.set_page_config(page_title="AI API Proxy", layout="centered")
    
    node_label = query_params.get("node", "")
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt_str = f'Tôi đang vẽ sơ đồ tư duy. Hãy liệt kê 3 đến 5 ý phụ thật ngắn gọn (tối đa 5 từ mỗi ý) để phát triển cho từ khóa: "{node_label}". TRẢ VỀ DUY NHẤT MỘT MẢNG JSON hợp lệ chứa các chuỗi, ví dụ: ["ý 1", "ý 2", "ý 3"]. Tuyệt đối không giải thích thêm, không có dấu markdown.'
            
            response = model.generate_content(prompt_str)
            raw_text = response.text.replace("```json", "").replace("```", "").strip()
            
            # Xuất dữ liệu chuẩn JSON cho JavaScript đọc
            st.write(json.dumps({"success": True, "ideas": json.loads(raw_text)}))
        else:
            st.write(json.dumps({"success": False, "error": "Chưa cấu hình GEMINI_API_KEY trong Secrets"}))
    except Exception as e:
        st.write(json.dumps({"success": False, "error": str(e)}))
    
    # Dừng toàn bộ chương trình tại đây, không cho vẽ giao diện rườm rà ra nữa
    st.stop()

# =========================================================================
# 2. KHU VỰC TRÌNH CHIẾU GIAO DIỆN CHÍNH (FRONTEND)
# =========================================================================
st.set_page_config(layout="wide", page_title="Người Mài Rìu - AI MindMap")

st.markdown("""
    <style>
        .block-container { padding: 0rem; }
    </style>
""", unsafe_allow_html=True)

try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=900, scrolling=True)
except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file index.html.")