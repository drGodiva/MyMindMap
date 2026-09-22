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

# Cấu hình API Gemini bằng Két sắt Secrets của Streamlit
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Lắng nghe yêu cầu gọi AI từ giao diện HTML gửi về
query_params = st.query_params
if "action" in query_params and query_params["action"] == "ask_ai":
    node_label = query_params.get("node", "")
    try:
        # Python gọi AI trực tiếp tại máy chủ (An toàn tuyệt đối, không lộ khóa)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt_str = f'Tôi đang vẽ sơ đồ tư duy. Hãy liệt kê 3 đến 5 ý phụ thật ngắn gọn (tối đa 5 từ mỗi ý) để phát triển cho từ khóa: "{node_label}". TRẢ VỀ DUY NHẤT MỘT MẢNG JSON hợp lệ chứa các chuỗi, ví dụ: ["ý 1", "ý 2", "ý 3"]. Tuyệt đối không giải thích thêm, không có dấu markdown.'
        
        response = model.generate_content(prompt_str)
        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        
        # Trả kết quả JSON về cho giao diện HTML
        st.json({"success": True, "ideas": json.loads(raw_text)})
    except Exception as e:
        st.json({"success": False, "error": str(e)})
    st.stop()

# Đọc và hiển thị giao diện HTML
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=900, scrolling=True)
except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file index.html.")