import streamlit as st
import streamlit.components.v1 as components
import json
from openai import OpenAI

st.set_page_config(layout="wide", page_title="Người Mài Rìu - AI MindMap Pro Max")
st.markdown("<style>.block-container { padding: 0rem; }</style>", unsafe_allow_html=True)

# Lấy khóa OpenAI từ Két sắt
api_key = st.secrets.get("OPENAI_API_KEY", "").strip()

ai_data_payload = {"ideas": []}
query_params = st.query_params

if "ai_node" in query_params:
    node_label = query_params["ai_node"]
    try:
        client = OpenAI(api_key=api_key)
        
        # Bơm prompt nhập vai chuyên gia chiến lược
        prompt_str = f'Bạn là một Chuyên gia tư vấn chiến lược và phân tích dữ liệu hàng đầu thế giới. Tôi đang vẽ sơ đồ tư duy. Hãy suy nghĩ đột phá và liệt kê 3 đến 5 ý phụ mang tính chiến lược, chuyên sâu và xuất sắc nhất để phát triển cho từ khóa: "{node_label}". Các ý phải cực kỳ cô đọng (tối đa 6 từ mỗi ý). TRẢ VỀ DUY NHẤT MỘT MẢNG JSON hợp lệ chứa các chuỗi, ví dụ: ["Chiến lược A", "Giải pháp B", "Đo lường C"]. Tuyệt đối không giải thích thêm, không có dấu markdown.'
        
        # Dùng mô hình gpt-4o-mini thế hệ mới siêu thông minh và rẻ
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt_str}]
        )
        raw_text = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
        ai_data_payload = {"node": node_label, "ideas": json.loads(raw_text)}
    except Exception as e:
        ai_data_payload = {"error": str(e)}

try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    injection_script = f"<script>window.SERVER_AI_RESULT = {json.dumps(ai_data_payload)};</script>"
    html_content = html_content.replace('</body>', injection_script + '</body>')

    components.html(html_content, height=900, scrolling=True)
except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file index.html trên GitHub.")