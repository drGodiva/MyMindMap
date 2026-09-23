import streamlit as st
import streamlit.components.v1 as components
import json
from openai import OpenAI

st.set_page_config(layout="wide", page_title="Người Mài Rìu - AI MindMap")
st.markdown("<style>.block-container { padding: 0rem; }</style>", unsafe_allow_html=True)

# Lấy khóa OpenAI từ Két sắt
api_key = st.secrets.get("OPENAI_API_KEY", "").strip()

ai_data_payload = {"ideas": []}
query_params = st.query_params
if "ai_node" in query_params:
    node_label = query_params["ai_node"]
    try:
        client = OpenAI(api_key=api_key)
        prompt_str = f'Tôi đang vẽ sơ đồ tư duy. Hãy liệt kê 3 đến 5 ý phụ thật ngắn gọn (tối đa 5 từ mỗi ý) để phát triển cho từ khóa: "{node_label}". TRẢ VỀ DUY NHẤT MỘT MẢNG JSON hợp lệ chứa các chuỗi, ví dụ: ["ý 1", "ý 2", "ý 3"]. Tuyệt đối không giải thích thêm, không có dấu markdown.'
        
        # Dùng gpt-3.5-turbo (hoặc gpt-4o-mini) cực kỳ rẻ, 5$ của thầy gọi được cả vạn lần
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
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