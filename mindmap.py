import pandas as pd
from pyvis.network import Network
import json

# 1. Khởi tạo sơ đồ: Khóa bố cục, màu nền Xanh ngọc đặc trưng
net = Network(height='100vh', width='100%', bgcolor='#012B1D', font_color='white', directed=True, layout=True)
net.set_options("""
var options = {
  "layout": { "hierarchical": { "enabled": true, "direction": "LR", "sortMethod": "directed", "levelSeparation": 250 } },
  "physics": { "hierarchicalRepulsion": { "centralGravity": 0.0, "springLength": 100, "nodeDistance": 150, "damping": 0.09 }, "solver": "hierarchicalRepulsion" }
}
""")

# THẦY DÁN LINK GOOGLE SHEETS VÀO ĐÂY (Đuôi CSV):
csv_url = "THAY_LINK_CUA_THAY_VAO_DAY"

# Dữ liệu Demo "All-in-One"
if csv_url == "THAY_LINK_CUA_THAY_VAO_DAY":
    data = {
        'Nút Cha': ['Bệnh nhân A', 'Bệnh nhân A', 'Bệnh nhân A', 'Chỉ số Kizen 520', 'Chỉ số Kizen 520'],
        'Nút Con': ['Chỉ số Kizen 520', 'Lộ trình F1+F2+F3', 'Khảo sát PRO2COL', 'Mỡ nội tạng (Chỉ số: 12)', 'Khối lượng cơ (Tốt)'],
        'Link Hình': ['', '', '', 'https://cdn-icons-png.flaticon.com/512/5029/5029136.png', ''],
        'Nét Đứt': ['', '', '', '', ''],
        'Ghi Chú': ['', 'Dùng thay thế bữa sáng', 'Làm ngay sau khi tư vấn', 'CẢNH BÁO CAO: Nguy cơ tiểu đường, tim mạch', 'Duy trì tập luyện'],
        'Link Web': ['', '', 'https://bacsiphungtam.com', '', ''],
        'Màu Sắc': ['', '', '', 'red', 'green'] # Mỡ nội tạng màu đỏ, Cơ màu xanh lá
    }
    df = pd.DataFrame(data)
else:
    df = pd.read_csv(csv_url)
    for col in ['Link Hình', 'Nét Đứt', 'Ghi Chú', 'Link Web', 'Màu Sắc']:
        if col not in df.columns: df[col] = ""

nodes_added = set()
node_links = {} 
search_data = [] # Lưu dữ liệu để làm thanh tìm kiếm

for index, row in df.iterrows():
    nut_cha = str(row['Nút Cha']).strip()
    nut_con = str(row['Nút Con']).strip()
    link_hinh = str(row['Link Hình']).strip()
    net_dut = str(row['Nét Đứt']).strip().lower()
    ghi_chu = str(row['Ghi Chú']).strip()
    link_web = str(row['Link Web']).strip()
    mau_sac = str(row['Màu Sắc']).strip()
    
    # Xử lý Nút Cha
    if nut_cha not in nodes_added:
        net.add_node(nut_cha, label=nut_cha, color='#D4AF37', size=40, shape='box', font={'size': 20, 'color': '#012B1D'})
        nodes_added.add(nut_cha)
        search_data.append({'id': nut_cha, 'label': nut_cha.lower()})
        
    # Xử lý Nút Con
    if nut_con not in nodes_added:
        title_html = f"<div style='font-family: Arial; padding: 10px; font-size: 14px;'>{ghi_chu}</div>" if ghi_chu and ghi_chu != 'nan' else ""
        node_color = mau_sac if mau_sac and mau_sac != 'nan' else '#004D40'
        
        if link_hinh and link_hinh != 'nan':
            net.add_node(nut_con, label=nut_con, shape='image', image=link_hinh, size=30, title=title_html, color=node_color)
        else:
            net.add_node(nut_con, label=nut_con, color=node_color, size=25, title=title_html)
            
        nodes_added.add(nut_con)
        search_data.append({'id': nut_con, 'label': nut_con.lower()})
        
        if link_web and link_web != 'nan':
            node_links[nut_con] = link_web
            
    # Vẽ đường nối
    is_dashed = True if net_dut == 'x' or net_dut == 'có' else False
    net.add_edge(nut_cha, nut_con, color='#D4AF37', dashes=is_dashed)

# Khởi tạo file HTML
html_content = net.generate_html()

# --- BƠM GIAO DIỆN & TÍNH NĂNG VÀO HTML ---
ui_injection = f"""
<!-- CSS LÀM ĐẸP GIAO DIỆN -->
<style>
    .m-btn {{ padding: 8px 15px; background: #D4AF37; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; color: #012B1D; margin-left: 5px; }}
    .m-btn:hover {{ background: #FFF; }}
    #search-box {{ padding: 8px; border-radius: 5px; border: none; width: 200px; outline: none; }}
    .floating-panel {{ position: absolute; z-index: 999; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 8px; }}
    #top-left {{ top: 20px; left: 20px; }}
    #top-right {{ top: 20px; right: 20px; }}
</style>

<!-- GIAO DIỆN NÚT BẤM -->
<div id="top-left" class="floating-panel">
    <input type="text" id="search-box" placeholder="🔎 Nhập tên nhánh để tìm...">
    <button class="m-btn" onclick="searchNode()">Tìm kiếm</button>
</div>
<div id="top-right" class="floating-panel">
    <button class="m-btn" id="btn-freeze" onclick="togglePhysics()">❄️ Đóng băng</button>
    <button class="m-btn" onclick="exportMap()">📸 Chụp ảnh bản đồ</button>
</div>

<!-- JAVASCRIPT XỬ LÝ SỰ KIỆN -->
<script type="text/javascript">
    var nodeLinks = {json.dumps(node_links)};
    var searchData = {json.dumps(search_data)};
    var physicsEnabled = true;

    // 1. TÌM KIẾM & ZOOM VÀO NHÁNH
    function searchNode() {{
        var keyword = document.getElementById('search-box').value.toLowerCase().trim();
        if (!keyword) return;
        var foundId = null;
        for (var i = 0; i < searchData.length; i++) {{
            if (searchData[i].label.includes(keyword)) {{
                foundId = searchData[i].id;
                break;
            }}
        }}
        if (foundId) {{
            network.selectNodes([foundId]);
            network.focus(foundId, {{ scale: 1.5, animation: {{ duration: 1000, easingFunction: 'easeInOutQuad' }} }});
        }} else {{ alert("Không tìm thấy nhánh nào chứa chữ: " + keyword); }}
    }}

    // 2. CHỤP ẢNH PNG
    function exportMap() {{
        var canvas = document.getElementsByTagName('canvas')[0];
        var dataURL = canvas.toDataURL("image/png");
        var link = document.createElement('a');
        link.download = 'SoDoTuDuy_NguoiMaiRiu.png';
        link.href = dataURL;
        link.click();
    }}

    // 3. ĐÓNG BĂNG / MỞ BĂNG CHUYỂN ĐỘNG
    function togglePhysics() {{
        physicsEnabled = !physicsEnabled;
        network.setOptions({{ physics: {{ enabled: physicsEnabled }} }});
        document.getElementById('btn-freeze').innerText = physicsEnabled ? "❄️ Đóng băng" : "🔥 Mở chuyển động";
    }}

    // 4. CLICK 1 LẦN -> MỞ LINK WEB
    network.on("click", function (params) {{
        if (params.nodes.length === 1) {{
            var nodeId = params.nodes[0];
            if (nodeLinks[nodeId]) window.open(nodeLinks[nodeId], '_blank');
        }}
    }});
    
    // 5. NHẤP ĐÚP CHUỘT -> THU GỌN / MỞ RỘNG NHÁNH
    network.on("doubleClick", function (params) {{
        if (params.nodes.length === 1) {{
            var nodeId = params.nodes[0];
            var connectedNodes = network.getConnectedNodes(nodeId, "to");
            if (connectedNodes.length > 0) {{
                var isExpanded = false;
                for (var i = 0; i < connectedNodes.length; i++) {{
                    if (nodes.get(connectedNodes[i]).hidden) {{ isExpanded = true; break; }}
                }}
                for (var i = 0; i < connectedNodes.length; i++) {{
                    nodes.update({{id: connectedNodes[i], hidden: !isExpanded}});
                }}
            }}
        }}
    }});
</script>
</body>
"""
html_content = html_content.replace('</body>', ui_injection)

# Lưu thành file chính thức
file_name = 'MindMap_Ultimate_NguoiMaiRiu.html'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"BÙM! Ứng dụng bản Ultimate đã hoàn thành! File: {file_name}")