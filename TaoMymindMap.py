import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json
import os

# Ép buộc Python chạy chế độ Google AI Studio (Dùng API Key), loại bỏ hoàn toàn Vertex AI / OAuth
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "false"

st.set_page_config(layout="wide", page_title="Người Mài Rìu - AI MindMap")
st.markdown("<style>.block-container { padding: 0rem; }</style>", unsafe_allow_html=True)

# Cấu hình két sắt API Key an toàn
if "GEMINI_API_KEY" in st.secrets:
    api_key_val = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=api_key_val)

# Nhận yêu cầu tạo nhánh AI từ giao diện gửi lên
ai_data_payload = {"ideas": []}
query_params = st.query_params
if "ai_node" in query_params:
    node_label = query_params["ai_node"]
    try:
        # Sử dụng model chuẩn AI Studio
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt_str = f'Tôi đang vẽ sơ đồ tư duy. Hãy liệt kê 3 đến 5 ý phụ thật ngắn gọn (tối đa 5 từ mỗi ý) để phát triển cho từ khóa: "{node_label}". TRẢ VỀ DUY NHẤT MỘT MẢNG JSON hợp lệ chứa các chuỗi, ví dụ: ["ý 1", "ý 2", "ý 3"]. Tuyệt đối không giải thích thêm, không có dấu markdown.'
        
        response = model.generate_content(prompt_str)
        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        ai_data_payload = {"node": node_label, "ideas": json.loads(raw_text)}
    except Exception as e:
        ai_data_payload = {"error": str(e)}

# Đọc file HTML và tiêm dữ liệu AI trực tiếp vào trình duyệt
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    injection_script = f"<script>window.SERVER_AI_RESULT = {json.dumps(ai_data_payload)};</script>"
    html_content = html_content.replace('</body>', injection_script + '</body>')

    components.html(html_content, height=900, scrolling=True)
except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file index.html trên GitHub.")