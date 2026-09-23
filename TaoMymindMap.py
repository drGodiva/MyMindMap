import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

st.set_page_config(layout="wide", page_title="Người Mài Rìu - AI MindMap Pro Max")
st.markdown("<style>.block-container { padding: 0rem; }</style>", unsafe_allow_html=True)

# Khởi tạo bộ nhớ tạm thời cho kết quả AI
if "ai_payload" not in st.session_state:
    st.session_state.ai_payload = None

# Khai báo bản đồ tư duy là một Component chính ngạch (đọc từ thư mục hiện tại)
mindmap_component = components.declare_component("mindmap", path=".")

# Khởi chạy giao diện và nhận lệnh nếu người dùng bấm nút AI
ui_request = mindmap_component(ai_data=st.session_state.ai_payload, key="mindmap_ui")

# Khi frontend gửi tín hiệu yêu cầu AI
if ui_request and ui_request.get("action") == "ask_ai":
    node_label = ui_request.get("node")
    st.session_state.ai_payload = None # Xóa trạng thái cũ
    
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "").strip()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt chuyên gia chiến lược
        prompt = f'Bạn là một Chuyên gia tư vấn chiến lược và phân tích dữ liệu hàng đầu thế giới. Tôi đang vẽ sơ đồ tư duy. Hãy suy nghĩ đột phá và liệt kê 3 đến 5 ý phụ mang tính chiến lược, chuyên sâu và xuất sắc nhất để phát triển cho từ khóa: "{node_label}". Các ý phải cực kỳ cô đọng (tối đa 6 từ mỗi ý). TRẢ VỀ DUY NHẤT MỘT MẢNG JSON hợp lệ chứa các chuỗi, ví dụ: ["Chiến lược A", "Giải pháp B", "Đo lường C"]. Tuyệt đối không giải thích thêm, không có dấu markdown.'
        
        response = model.generate_content(prompt)
        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        st.session_state.ai_payload = {"node": node_label, "ideas": json.loads(raw_text)}
    except Exception as e:
        st.session_state.ai_payload = {"error": str(e)}
    
    # Ra lệnh tải lại hệ thống ngầm để bơm dữ liệu mới xuống frontend
    st.rerun()