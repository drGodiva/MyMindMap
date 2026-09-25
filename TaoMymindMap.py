import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import json

st.set_page_config(layout="wide", page_title="Người Mài Rìu - AI MindMap Pro Max")
st.markdown("<style>.block-container { padding: 0rem; }</style>", unsafe_allow_html=True)

# Khởi tạo hòm thư giao liên giữa Python và Bản đồ Web
if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

# Khai báo bản đồ tư duy là một Ứng dụng Chính ngạch (đọc file index.html cùng thư mục)
mindmap_component = components.declare_component("mindmap", path=".")

# Hiển thị bản đồ và lắng nghe tín hiệu từ Web gửi về Python
frontend_data = mindmap_component(ai_data=st.session_state.ai_result, key="mindmap_ui")

# Khi người dùng bấm nút AI trên Web, Web sẽ gửi chữ "ask_ai" về đây
if frontend_data and frontend_data.get("action") == "ask_ai":
    node_label = frontend_data.get("node")
    st.session_state.ai_result = None # Xóa kết quả cũ
    
    try:
        # Lấy khóa bảo mật một cách kín đáo (tuyệt đối không bơm ra Web)
        api_key = st.secrets["OPENAI_API_KEY"]
        client = OpenAI(api_key=api_key)
        
        prompt_str = f'Bạn là một Chuyên gia tư vấn chiến lược và phân tích dữ liệu hàng đầu thế giới. Tôi đang vẽ sơ đồ tư duy. Hãy suy nghĩ đột phá và liệt kê 3 đến 5 ý phụ mang tính chiến lược, chuyên sâu và xuất sắc nhất để phát triển cho từ khóa: "{node_label}". Các ý phải cực kỳ cô đọng (tối đa 6 từ mỗi ý). TRẢ VỀ DUY NHẤT MỘT MẢNG JSON hợp lệ chứa các chuỗi, ví dụ: ["Chiến lược A", "Giải pháp B", "Đo lường C"]. Tuyệt đối không giải thích thêm, không có dấu markdown.'
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_str}],
            temperature=0.7
        )
        raw_text = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
        
        # Đóng gói kết quả gửi về lại cho bản đồ
        st.session_state.ai_result = {"node": node_label, "ideas": json.loads(raw_text)}
    except Exception as e:
        st.session_state.ai_result = {"error": str(e)}
    
    # Kích hoạt lại luồng ngầm để đẩy kết quả ra Web
    st.rerun()