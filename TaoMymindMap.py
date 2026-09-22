import streamlit as st
import streamlit.components.v1 as components
import json
import urllib.request
import urllib.error

st.set_page_config(layout="wide", page_title="Người Mài Rìu - AI MindMap")
st.markdown("<style>.block-container { padding: 0rem; }</style>", unsafe_allow_html=True)

# Lấy tự động API Key từ Két sắt Secrets (Giấu kín hoàn toàn trên GitHub)
api_key = st.secrets.get("GEMINI_API_KEY", "").strip()

# Xử lý yêu cầu tạo nhánh AI từ giao diện gửi lên
ai_data_payload = {"ideas": []}
query_params = st.query_params
if "ai_node" in query_params:
    node_label = query_params["ai_node"]
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        prompt_str = f'Tôi đang vẽ sơ đồ tư duy. Hãy liệt kê 3 đến 5 ý phụ thật ngắn gọn (tối đa 5 từ mỗi ý) để phát triển cho từ khóa: "{node_label}". TRẢ VỀ DUY NHẤT MỘT MẢNG JSON hợp lệ chứa các chuỗi, ví dụ: ["ý 1", "ý 2", "ý 3"]. Tuyệt đối không giải thích thêm, không có dấu markdown.'
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt_str}]
            }]
        }
        
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            raw_text = res_data['candidates'][0]['content']['parts'][0]['text']
            clean_json = raw_text.replace("```json", "").replace("```", "").strip()
            ai_data_payload = {"node": node_label, "ideas": json.loads(clean_json)}
            
    except Exception as e:
        ai_data_payload = {"error": str(e)}

# Đọc file HTML giao diện
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    injection_script = f"<script>window.SERVER_AI_RESULT = {json.dumps(ai_data_payload)};</script>"
    html_content = html_content.replace('</body>', injection_script + '</body>')

    components.html(html_content, height=900, scrolling=True)
except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file index.html trên GitHub.")