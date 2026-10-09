# -*- coding: utf-8 -*-
"""15 bài của khóa Thiết kế mạch PCB với Altium Designer."""
import figs

DRIVE = {
    "basic": "https://drive.google.com/drive/folders/1ntGAWmn761SY2FYf27y7f49tet2iK_A_?usp=sharing",
    "4lop": "https://drive.google.com/drive/folders/1YHw5ivbMP5qDJHukmPXfuaBxHfVxFykK?usp=sharing",
    "thuvien": "https://drive.google.com/drive/folders/1tUKCsGB7iSNjgao69q5aMWyYvZfuF8ex?usp=sharing",
    "thatco": "https://drive.google.com/drive/folders/1na2DnZkS68-9p8z7wnt1de6qebnjNdi2?usp=sharing",
}

_CALC_CSS = """<style>.calc{background:#fff;border:1px solid #cbd5e1;border-radius:12px;padding:12px 16px;margin:10px 0}
.calc h5{margin:0 0 8px}.calc label{display:inline-flex;flex-direction:column;font-size:.8rem;color:#475569;margin:0 12px 8px 0}
.calc input,.calc select{font:inherit;font-size:.9rem;padding:5px 8px;border:1px solid #cbd5e1;border-radius:8px;width:120px}.calc select{width:170px}
.calc .kq{font-weight:700;color:#0f172a;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:8px 12px;margin-top:4px}</style>"""

CALC_TRACE = _CALC_CSS + """
<div class="calc" id="ctrace"><h5>🧮 Máy tính bề rộng đường mạch (IPC-2221)</h5>
<label>Dòng điện (A)<input type="number" step="0.1" value="2" data-k="i"></label>
<label>Tăng nhiệt cho phép (°C)<input type="number" value="10" data-k="dt"></label>
<label>Độ dày đồng<select data-k="oz"><option value="0.5">0.5 oz (18 µm)</option><option value="1" selected>1 oz (35 µm)</option><option value="2">2 oz (70 µm)</option></select></label>
<label>Lớp<select data-k="k"><option value="0.048">ngoài (top/bottom)</option><option value="0.024">trong</option></select></label>
<div class="kq"></div></div>
<script>(function(){var r=document.getElementById('ctrace');function f(){var v={};r.querySelectorAll('[data-k]').forEach(function(e){v[e.dataset.k]=parseFloat(e.value)});
var A=Math.pow(v.i/(v.k*Math.pow(v.dt,0.44)),1/0.725),w=A/(v.oz*1.378);r.querySelector('.kq').textContent='Bề rộng tối thiểu: '+(w*0.0254).toFixed(2)+' mm  ('+w.toFixed(1)+' mil). Nên chọn rộng hơn 20–50% nếu còn chỗ.';}
r.addEventListener('input',f);f();})();</script>"""

CALC_HOLE = _CALC_CSS + """
<div class="calc" id="chole"><h5>🧮 Máy tính lỗ khoan & pad chân xuyên</h5>
<label>Chân tròn: đường kính (mm)<input type="number" step="0.01" value="0.6" data-k="d"></label>
<label>hoặc chân chữ nhật a (mm)<input type="number" step="0.01" value="0" data-k="a"></label>
<label>b (mm)<input type="number" step="0.01" value="0" data-k="b"></label>
<label>Vành khuyên (mm)<input type="number" step="0.05" value="0.3" data-k="r"></label>
<div class="kq"></div></div>
<script>(function(){var r=document.getElementById('chole'),M=[0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.5,1.6,2.0,2.5,3.2];function f(){var v={};r.querySelectorAll('[data-k]').forEach(function(e){v[e.dataset.k]=parseFloat(e.value)||0});
var d=(v.a>0&&v.b>0)?Math.hypot(v.a,v.b):v.d,h=d+0.2,lo=M.find(function(x){return x>=h-1e-9})||h;r.querySelector('.kq').textContent='Kích thước chân tính: '+d.toFixed(2)+' mm → lỗ khoan '+lo.toFixed(2)+' mm, pad '+(lo+2*v.r).toFixed(2)+' mm';}
r.addEventListener('input',f);f();})();</script>"""

CALC_DIV = _CALC_CSS + """
<div class="calc" id="cdiv"><h5>🧮 Máy tính cầu phân áp cho ADC 3.3 V</h5>
<label>Điện áp đo tối đa (V)<input type="number" step="0.1" value="25.2" data-k="v"></label>
<label>R1 – trên (kΩ)<input type="number" value="100" data-k="r1"></label>
<label>R2 – dưới (kΩ)<input type="number" value="10" data-k="r2"></label>
<label>ADC (bit)<input type="number" value="12" data-k="n"></label>
<div class="kq"></div></div>
<script>(function(){var r=document.getElementById('cdiv');function f(){var v={};r.querySelectorAll('[data-k]').forEach(function(e){v[e.dataset.k]=parseFloat(e.value)||0});
var k=v.r2/(v.r1+v.r2),o=v.v*k,lsb=3.3/Math.pow(2,v.n)/k*1000,s=o>3.3?'⛔ VƯỢT 3.3 V':(o>2.97?'⚠ sát giới hạn':'✓ an toàn');
r.querySelector('.kq').textContent='Áp vào ADC tối đa '+o.toFixed(2)+' V ('+s+'), độ phân giải '+lsb.toFixed(1)+' mV/bước, dòng qua cầu '+(v.v/(v.r1+v.r2)*1000).toFixed(0)+' µA';}
r.addEventListener('input',f);f();})();</script>"""

L01 = dict(
  id="tong-quan", short="Tổng quan PCB & Altium", title="Tổng quan PCB và Altium Designer", icon="🧭", time="2 giờ",
  goal="Hiểu mạch in là gì, quy trình thiết kế từ ý tưởng tới mạch thật, và làm quen giao diện Altium Designer 18.",
  goals=["Biết PCB gồm những gì, 1 lớp / 2 lớp / 4 lớp khác nhau thế nào", "Nắm quy trình 8 bước thiết kế PCB", "Biết cấu trúc project và các loại file của Altium",
         "Làm quen giao diện, phím tắt quan trọng"],
  sections=[
    dict(h="PCB là gì?", fig=figs.cross_section(), html="""
<p><b>PCB</b> (Printed Circuit Board – mạch in) là tấm vật liệu cách điện (thường là sợi thuỷ tinh epoxy <b>FR-4</b>) có các đường <b>đồng</b> nối các linh kiện thay cho dây điện. So với hàn dây trên testboard: gọn, bền, ít nhiễu, sản xuất hàng loạt được.</p>
<table class="tbl"><tr><th>Loại</th><th>Dùng khi</th><th>Giá gia công (tham khảo)</th></tr>
<tr><td>1 lớp</td><td>mạch rất đơn giản, tự làm thủ công (là ủi, ăn mòn)</td><td>rẻ nhất</td></tr>
<tr><td><b>2 lớp</b></td><td>đa số dự án học sinh, Arduino shield, mạch nguồn</td><td>~2 USD / 5 tấm 10×10 cm</td></tr>
<tr><td>4 lớp</td><td>vi điều khiển tốc độ cao, WiFi/BLE, USB, nhiều nguồn</td><td>~7–10 USD / 5 tấm</td></tr>
<tr><td>6+ lớp</td><td>BGA, DDR, máy tính nhúng</td><td>cao</td></tr></table>"""),
    dict(h="Quy trình thiết kế", fig=figs.design_flow(), html="""
<p>Mọi phần mềm (Altium, KiCad, EasyEDA, OrCAD) đều theo quy trình này. Altium Designer là phần mềm chuyên nghiệp phổ biến trong doanh nghiệp Việt Nam; <b>KiCad</b> (miễn phí) và <b>EasyEDA</b> (trực tuyến) có cùng khái niệm — học một cái là dùng được cái kia.</p>"""),
    dict(h="Altium Designer: project và giao diện", html="""
<table class="tbl"><tr><th>File</th><th>Nội dung</th></tr>
<tr><td><code>.PrjPcb</code></td><td>project – gom tất cả file lại, chứa cấu hình output</td></tr>
<tr><td><code>.SchDoc</code></td><td>bản vẽ nguyên lý</td></tr><tr><td><code>.PcbDoc</code></td><td>bản vẽ mạch in (layout)</td></tr>
<tr><td><code>.SchLib</code> / <code>.PcbLib</code></td><td>thư viện ký hiệu nguyên lý / thư viện footprint</td></tr>
<tr><td><code>.IntLib</code></td><td>thư viện tích hợp (symbol + footprint + 3D đã đóng gói)</td></tr>
<tr><td><code>.OutJob</code></td><td>cấu hình xuất file sản xuất một lần bấm</td></tr></table>
<table class="tbl"><tr><th>Phím tắt</th><th>Tác dụng</th></tr>
<tr><td><kbd>P</kbd> → <kbd>P</kbd></td><td>đặt linh kiện (Place Part)</td></tr><tr><td><kbd>P</kbd> → <kbd>W</kbd> / <kbd>Ctrl</kbd>+<kbd>W</kbd></td><td>vẽ dây (wire) trong Schematic</td></tr>
<tr><td><kbd>P</kbd> → <kbd>T</kbd> / <kbd>Ctrl</kbd>+<kbd>W</kbd></td><td>đi dây (track) trong PCB</td></tr><tr><td><kbd>Space</kbd>, <kbd>X</kbd>, <kbd>Y</kbd></td><td>xoay, lật linh kiện khi đang kéo</td></tr>
<tr><td><kbd>Tab</kbd></td><td>sửa thuộc tính khi đang đặt</td></tr><tr><td><kbd>Q</kbd></td><td>đổi đơn vị mm ↔ mil</td></tr>
<tr><td><kbd>G</kbd></td><td>đổi bước lưới (grid)</td></tr><tr><td><kbd>2</kbd> / <kbd>3</kbd></td><td>xem 2D / 3D</td></tr>
<tr><td><kbd>L</kbd></td><td>bật/tắt hiển thị các lớp</td></tr><tr><td><kbd>Shift</kbd>+<kbd>S</kbd></td><td>xem một lớp duy nhất</td></tr></table>
<div class="callout">💡 Đơn vị: <b>1 mil = 0.0254 mm</b> (1/1000 inch). Bước chân linh kiện chuẩn 2.54 mm = 100 mil. Nhiều quy tắc thiết kế vẫn ghi bằng mil.</div>"""),
  ],
  exercises=["Cài Altium Designer (bản dùng thử/giáo dục) hoặc KiCad, tạo project mới gồm 1 SchDoc và 1 PcbDoc.", "Mở một project mẫu trong thư mục tài liệu, xem 2D/3D, bật/tắt từng lớp."],
  refs=[("Tài liệu khóa Basic (Google Drive)", DRIVE["basic"]), ("Altium Designer Documentation", "https://www.altium.com/documentation/altium-designer"), ("KiCad (miễn phí)", "https://www.kicad.org")],
)

L02 = dict(
  id="lop-pcb", short="Thành phần & layer", title="Các thành phần và các lớp (layer) trên mạch PCB", icon="🥪", time="1,5 giờ",
  goal="Hiểu ý nghĩa từng lớp trong Altium để vẽ đúng lớp và đọc hiểu file sản xuất.",
  goals=["Phân biệt lớp đồng, solder mask, paste, silkscreen, mechanical, keep-out, drill", "Hiểu pad, via, track, polygon", "Biết các loại via"],
  sections=[
    dict(h="Các lớp trong Altium", html="""
<table class="tbl"><tr><th>Lớp</th><th>Ý nghĩa</th><th>Ghi chú</th></tr>
<tr><td><b>Top / Bottom Layer</b></td><td>lớp đồng dẫn điện</td><td>4 lớp thêm Mid-Layer / Internal Plane</td></tr>
<tr><td><b>Top / Bottom Overlay</b></td><td>silkscreen – chữ, ký hiệu, khung linh kiện in màu trắng</td><td>chữ cao ≥ 0.8–1 mm, nét ≥ 0.15 mm</td></tr>
<tr><td><b>Top / Bottom Solder</b></td><td>solder mask – vùng KHÔNG phủ sơn (để lộ đồng ra hàn)</td><td>vẽ “âm bản”</td></tr>
<tr><td><b>Top / Bottom Paste</b></td><td>lớp kem hàn – làm khuôn (stencil) cho linh kiện dán</td><td>chỉ có ở pad SMD</td></tr>
<tr><td><b>Mechanical 1…</b></td><td>đường viền mạch, kích thước, lỗ bắt vít, ghi chú</td><td>quy ước tuỳ công ty</td></tr>
<tr><td><b>Keep-Out Layer</b></td><td>vùng cấm đi dây/đổ đồng</td><td>mép mạch, anten</td></tr>
<tr><td><b>Drill Guide / Drill Drawing</b></td><td>bản vẽ lỗ khoan</td><td>xuất kèm file NC Drill</td></tr>
<tr><td><b>Multi-Layer</b></td><td>đối tượng có trên mọi lớp đồng (pad chân xuyên, via)</td><td></td></tr></table>"""),
    dict(h="Đối tượng trên lớp đồng", fig=figs.via_types(), html="""
<ul><li><b>Pad</b>: chỗ hàn chân linh kiện (chân xuyên: Multi-Layer có lỗ; chân dán: chỉ Top hoặc Bottom).</li>
<li><b>Track</b>: đường đồng nối các pad.</li><li><b>Via</b>: lỗ mạ đồng nối giữa các lớp, không để hàn linh kiện.</li>
<li><b>Polygon pour</b>: vùng đồng lớn (thường nối GND) — giảm nhiễu, tản nhiệt, giảm lượng đồng phải ăn mòn.</li>
<li><b>Fiducial</b>: dấu tròn để máy gắp đặt linh kiện tự căn chỉnh.</li></ul>""", fig2=None),
  ],
  embedded=["Độ dày đồng 1 oz/ft² ≈ 35 µm là mặc định; mạch công suất đặt 2 oz.", "Màu solder mask (xanh, đen, đỏ…) chỉ là thẩm mỹ, xanh lá rẻ và dễ kiểm tra nhất."],
  exercises=["Mở một PcbDoc mẫu, dùng <kbd>Shift</kbd>+<kbd>S</kbd> xem riêng từng lớp và ghi lại lớp đó chứa gì.", "Giải thích vì sao lớp Solder Mask được vẽ “âm bản”."],
)
L02["sections"][1].pop("fig2")

L03 = dict(
  id="nguyen-ly", short="Mạch nguyên lý", title="Thiết kế mạch nguyên lý (Schematic)", icon="📐", time="3 giờ",
  goal="Vẽ bản nguyên lý rõ ràng, đúng điện, sẵn sàng chuyển sang layout.",
  goals=["Đặt linh kiện, nối dây, net label, power port", "Chia trang, hierarchical sheet, bus", "Đánh số linh kiện (annotate), kiểm tra ERC, xuất BOM"],
  sections=[
    dict(h="Các bước vẽ nguyên lý", html="""
<ol><li><b>Đặt linh kiện</b> (<kbd>P</kbd><kbd>P</kbd>) từ thư viện; đặt giá trị (10k, 100nF) và footprint cho từng linh kiện.</li>
<li><b>Nối dây</b> (<kbd>Ctrl</kbd>+<kbd>W</kbd>); chỗ 3 dây gặp nhau phải có <b>chấm nối</b> (junction).</li>
<li>Dùng <b>Net Label</b> thay cho dây dài: hai điểm có cùng tên net là được nối với nhau.</li>
<li><b>Power Port</b> cho nguồn và đất (VCC, 3V3, GND) — đặt tên thống nhất.</li>
<li>Mạch lớn: chia thành nhiều trang theo khối chức năng (nguồn, MCU, cảm biến, giao tiếp), nối bằng <b>Port</b> hoặc <b>Hierarchical Sheet</b>.</li>
<li><b>Annotate</b> (Tools → Annotation): đánh số R1, R2, C1… tự động.</li>
<li><b>Compile / ERC</b> (Project → Validate): kiểm tra chân bỏ trống, net chỉ có 1 chân, hai đầu ra nối nhau…</li>
<li>Xuất <b>BOM</b> (Reports → Bill of Materials) để mua linh kiện.</li></ol>"""),
    dict(h="Quy tắc trình bày", html="""
<div class="grid2"><div class="card"><h5>✅ Nên</h5><p>Tín hiệu đi từ trái sang phải, nguồn ở trên, GND ở dưới · nhóm linh kiện theo khối, có khung và tiêu đề · ghi chú giá trị, công suất, điện áp tụ · tụ decoupling vẽ ngay cạnh IC mà nó phục vụ · đặt test point cho tín hiệu quan trọng.</p></div>
<div class="card"><h5>❌ Không nên</h5><p>Dây chéo nhau lung tung · nối dây vào giữa thân chân khác · đặt net label lơ lửng không chạm dây · dùng chung tên net vô tình (ví dụ hai net “OUT”) · để chân IC không dùng mà không đánh dấu No-ERC.</p></div></div>
<p>Ví dụ khối nguồn chuẩn cho ESP32: jack DC/USB → diode chống ngược → tụ 10 µF → LDO AMS1117-3.3 → tụ 10 µF + 100 nF → 3V3, kèm LED báo nguồn có điện trở 1k.</p>"""),
  ],
  mistakes=["Quên gán footprint → không chuyển được sang PCB.", "Ký hiệu symbol đúng nhưng thứ tự chân footprint sai (đặc biệt transistor, LDO, MOSFET) — luôn đối chiếu datasheet.",
            "Bỏ qua cảnh báo ERC."],
  exercises=["Vẽ nguyên lý mạch Arduino tối giản: ATmega328P, thạch anh 16 MHz + 2 tụ 22 pF, nút reset, LED chân 13, header ICSP.",
             "Vẽ khối nguồn 5 V → 3.3 V cho ESP32 kèm LED báo nguồn; chạy ERC và sửa hết lỗi."],
  refs=[("Tài liệu khóa Basic (Google Drive)", DRIVE["basic"])],
)

L04 = dict(
  id="layout-2-lop", short="Layout 2 lớp", title="Thiết kế layout mạch 2 lớp", icon="🛠", time="4 giờ",
  goal="Chuyển nguyên lý sang mạch in, sắp xếp linh kiện hợp lý, đặt quy tắc, đi dây, đổ đồng và kiểm tra DRC.",
  goals=["Import nguyên lý vào PCB (Update PCB Document)", "Vẽ khung mạch, đặt linh kiện theo khối", "Đặt Design Rules: clearance, width, via",
         "Đi dây, đổ đồng GND, chạy DRC"],
  sections=[
    dict(h="Từ nguyên lý sang PCB", html="""
<ol><li><b>Design → Update PCB Document</b>: linh kiện và các đường “chuột” (ratsnest) xuất hiện.</li>
<li>Vẽ <b>đường viền mạch</b> trên lớp Mechanical 1 rồi <b>Design → Board Shape → Define from selected objects</b>; bo góc 1–2 mm, lỗ bắt vít M3 (lỗ 3.2 mm) cách mép ≥ 3 mm.</li>
<li><b>Đặt linh kiện</b> (placement) — chiếm 50% chất lượng mạch:
<ul><li>Đặt trước: connector, nút, LED, màn hình (vị trí do vỏ hộp quyết định).</li>
<li>Theo khối chức năng giống nguyên lý; tụ decoupling sát chân nguồn IC; thạch anh sát vi điều khiển.</li>
<li>Phần công suất (nguồn, driver động cơ) tách khỏi phần tín hiệu/analog.</li>
<li>Xoay linh kiện cho đường chuột ngắn và ít chéo nhau; cùng loại linh kiện cùng hướng.</li></ul></li></ol>"""),
    dict(h="Design Rules – quy tắc thiết kế", html="""
<table class="tbl"><tr><th>Quy tắc</th><th>Giá trị an toàn cho xưởng giá rẻ (JLCPCB, PCBWay)</th></tr>
<tr><td>Clearance (khoảng cách đồng–đồng)</td><td>≥ 0.2 mm (8 mil); nguồn 220 V AC: ≥ 2.5–3 mm và có rãnh cách ly</td></tr>
<tr><td>Width – tín hiệu</td><td>0.25 mm (10 mil)</td></tr>
<tr><td>Width – nguồn</td><td>tính theo dòng (xem máy tính bên dưới), thường 0.5–1.5 mm</td></tr>
<tr><td>Via</td><td>lỗ 0.3 mm, đường kính 0.6 mm</td></tr>
<tr><td>Khoảng cách đồng tới mép mạch</td><td>≥ 0.3–0.5 mm</td></tr></table>
<p>Đặt trong <b>Design → Rules</b>. Có thể tạo rule riêng cho một net/lớp net: ví dụ <code>InNetClass('Power')</code> rộng 0.8 mm.</p>""",
         after=CALC_TRACE),
    dict(h="Đi dây, đổ đồng và DRC", fig=figs.decoupling(), html="""
<ul><li>Đi dây nguồn và tín hiệu quan trọng trước; góc gãy 45° (không 90°).</li>
<li>Mạch 2 lớp: ưu tiên một lớp đi ngang, một lớp đi dọc; hạn chế cắt vụn mặt GND ở lớp Bottom.</li>
<li><b>Polygon Pour</b> (<kbd>P</kbd><kbd>G</kbd>) nối net GND trên cả hai lớp, rải thêm via nối hai mặt GND (“via stitching”) mỗi 5–10 mm.</li>
<li><b>Tools → Design Rule Check</b>: sửa hết lỗi (khoảng cách, chưa nối, ngắn mạch, silkscreen đè pad).</li></ul>"""),
  ],
  mistakes=["Đi dây trước khi sắp xếp linh kiện xong.", "Đường nguồn mảnh như đường tín hiệu.", "Đổ đồng xong không nối vào net GND (polygon “chết”).", "Bỏ qua lỗi DRC “Un-Routed Net”."],
  exercises=["Layout mạch Arduino tối giản ở bài 3 trên khổ 50 × 50 mm, 2 lớp, đổ đồng GND.",
             "Dùng máy tính ở trên: đường cấp nguồn cho 4 động cơ servo (tổng 3 A) cần rộng bao nhiêu?"],
  refs=[("Tài liệu khóa Basic (Google Drive)", DRIVE["basic"]), ("Năng lực gia công JLCPCB", "https://jlcpcb.com/capabilities/pcb-capabilities")],
)

L05 = dict(
  id="logo", short="Thiết kế logo", title="Thiết kế logo và chữ trên mạch", icon="🎨", time="1 giờ",
  goal="Đưa logo trường, đội, tên dự án lên mạch đẹp và in được.",
  goals=["Chuẩn bị ảnh logo đúng cách", "Đưa logo vào lớp silkscreen hoặc đồng", "Biết giới hạn kích thước của xưởng"],
  sections=[
    dict(h="Cách đưa logo lên mạch", html="""
<ol><li>Chuẩn bị ảnh <b>đen trắng</b> (1 bit, không xám), độ phân giải đủ cao, dạng BMP/PNG.</li>
<li>Altium: chạy script <b>PCB Logo Creator</b> (DXP → Run Script → <code>PCBLogoCreator.PRJSCR</code>) hoặc <b>File → Import → DXF/DWG</b> nếu logo là file vector.</li>
<li>Chọn lớp: <b>Top Overlay</b> (chữ trắng), <b>Top Layer + Top Solder</b> (logo đồng vàng/ENIG lộ ra), hoặc khoét solder mask để logo màu đồng.</li>
<li>Chỉnh kích thước, đặt ở vùng trống, không đè lên pad.</li></ol>
<table class="tbl"><tr><th>Thông số silkscreen</th><th>Tối thiểu (xưởng phổ thông)</th></tr>
<tr><td>Bề rộng nét</td><td>0.15 mm</td></tr><tr><td>Chiều cao chữ</td><td>0.8–1.0 mm</td></tr><tr><td>Khoảng cách tới pad</td><td>0.15 mm (sẽ bị cắt nếu đè pad)</td></tr></table>
<p>Nên ghi trên mạch: tên dự án, phiên bản (v1.0), ngày, tên đội/trường, chú thích chân connector (GND, 5V, TX, RX), chiều cắm (+/−).</p>"""),
  ],
  exercises=["Đưa logo trường/đội lên mạch ở bài 4, kích thước 15 × 15 mm trên Top Overlay.", "Ghi chú đầy đủ tên chân cho mọi connector."],
  refs=[("Tài liệu khóa Basic (Google Drive)", DRIVE["basic"])],
)

L06 = dict(
  id="xuat-file-du-an", short="Xuất file & dự án mẫu", title="Xuất file sản xuất và thực hành dự án PCB mẫu", icon="📦", time="3 giờ",
  goal="Xuất đầy đủ file cho xưởng, đặt gia công và hoàn thành trọn vẹn một dự án mẫu.",
  goals=["Xuất Gerber, NC Drill, Pick & Place, BOM", "Kiểm tra file bằng trình xem Gerber", "Đặt gia công tại xưởng", "Thực hiện dự án mẫu từ đầu tới cuối"],
  sections=[
    dict(h="Bộ file gửi xưởng", html="""
<table class="tbl"><tr><th>File</th><th>Altium</th><th>Dùng để</th></tr>
<tr><td>Gerber (RS-274X)</td><td>File → Fabrication Outputs → Gerber Files</td><td>hình ảnh từng lớp: đồng, mask, silk, viền</td></tr>
<tr><td>NC Drill (Excellon)</td><td>File → Fabrication Outputs → NC Drill Files</td><td>toạ độ và kích thước lỗ khoan</td></tr>
<tr><td>Pick &amp; Place (CPL)</td><td>File → Assembly Outputs → Generates pick and place files</td><td>toạ độ, góc xoay linh kiện (nếu nhờ xưởng hàn)</td></tr>
<tr><td>BOM</td><td>Reports → Bill of Materials</td><td>danh sách linh kiện</td></tr></table>
<p>Gerber: chọn đơn vị mm, định dạng 4:4; chọn đủ các lớp đang dùng + Mechanical viền mạch. Nén tất cả thành một file .zip, kiểm tra lại bằng trình xem Gerber của xưởng trước khi đặt hàng. Dùng <b>OutJob</b> để lần sau chỉ bấm một nút.</p>"""),
    dict(h="Dự án mẫu: mạch đo nhiệt độ – độ ẩm ESP32", html="""
<ol><li><b>Yêu cầu</b>: ESP32-WROOM, nguồn USB-C 5 V → 3.3 V, cảm biến SHT31 (I2C), màn hình OLED 0.96" (I2C), 2 nút nhấn, LED trạng thái, header mở rộng.</li>
<li><b>Nguyên lý</b>: 4 khối — nguồn, ESP32 (kèm mạch reset/boot và nạp qua CH340C), cảm biến/màn hình, nút/LED.</li>
<li><b>Thư viện</b>: tải footprint ESP32 module và USB-C từ nhà sản xuất; tự làm footprint SHT31 (DFN) theo bài 9.</li>
<li><b>Layout</b>: mạch 2 lớp 60 × 40 mm; anten module nhô ra mép, cấm đồng dưới anten; cảm biến đặt xa LDO và ESP32 (tránh nhiệt) và có khe cắt cách nhiệt.</li>
<li><b>Kiểm tra</b>: ERC, DRC, xem 3D đối chiếu vỏ hộp, in giấy tỉ lệ 1:1 đặt linh kiện thật lên thử.</li>
<li><b>Xuất file, đặt hàng, hàn, nạp code đo kiểm</b>.</li></ol>"""),
  ],
  mistakes=["Quên lớp viền (Mechanical/Keep-Out) trong Gerber → xưởng không biết cắt.", "Quên file khoan.", "Không kiểm tra lại Gerber trước khi đặt hàng."],
  exercises=["Hoàn thành dự án mẫu tới bước xuất file Gerber, kiểm tra bằng trình xem trực tuyến.", "Viết checklist 15 mục kiểm tra trước khi gửi xưởng."],
  refs=[("Tài liệu dự án PCB mẫu (Google Drive)", DRIVE["basic"])],
)

L07 = dict(
  id="su-dung-thu-vien", short="Sử dụng thư viện", title="Sử dụng và quản lý thư viện linh kiện", icon="📚", time="1,5 giờ",
  goal="Tìm, cài và quản lý thư viện linh kiện; biết khi nào dùng thư viện có sẵn, khi nào tự làm.",
  goals=["Hiểu symbol, footprint, model 3D và thông số (parameter)", "Cài thư viện, tìm linh kiện bằng Manufacturer Part Search",
         "Tải thư viện từ SnapEDA, Ultra Librarian, LCSC/EasyEDA", "Tổ chức thư viện riêng của nhóm"],
  sections=[
    dict(h="Một linh kiện gồm những gì?", html="""
<table class="tbl"><tr><th>Thành phần</th><th>Nằm ở</th><th>Mô tả</th></tr>
<tr><td>Symbol</td><td>.SchLib</td><td>ký hiệu trên nguyên lý, các chân có số và tên</td></tr>
<tr><td>Footprint</td><td>.PcbLib</td><td>hình pad thực tế trên mạch, đúng kích thước datasheet</td></tr>
<tr><td>3D model</td><td>.step</td><td>để kiểm tra va chạm, xuất cho vỏ hộp</td></tr>
<tr><td>Parameter</td><td>trong symbol</td><td>giá trị, mã nhà sản xuất, nhà cung cấp, giá</td></tr></table>
<p>Chân số <b>N</b> của symbol phải nối với pad số <b>N</b> của footprint — sai ở đây là lỗi nguy hiểm nhất, mạch in ra không chạy mà nhìn không thấy.</p>"""),
    dict(h="Nguồn thư viện", html="""
<ul><li><b>Components panel</b> → Manufacturer Part Search (Altium 18+): tìm theo mã, kéo thả linh kiện đã có đủ symbol, footprint, 3D.</li>
<li><b>SnapEDA, Ultra Librarian, Component Search Engine</b>: tải miễn phí theo mã linh kiện, chọn định dạng Altium.</li>
<li><b>LCSC / EasyEDA</b>: thư viện linh kiện có sẵn ở kho JLCPCB (tiện khi nhờ xưởng hàn).</li>
<li>Thư viện của nhóm: một file .SchLib + .PcbLib (hoặc .IntLib) dùng chung, đặt tên theo quy ước, mỗi linh kiện được kiểm tra một lần.</li></ul>
<div class="callout warn">⚠️ Thư viện tải về <b>không phải lúc nào cũng đúng</b>: luôn kiểm tra kích thước pad, số chân, vị trí chân 1 với datasheet.</div>"""),
  ],
  exercises=["Tải thư viện của cảm biến BME280 và module ESP32-WROOM-32E, kiểm tra lại với datasheet.", "Tạo thư viện riêng của nhóm, đưa 10 linh kiện hay dùng vào."],
  refs=[("Tài liệu khóa thư viện (Google Drive)", DRIVE["thuvien"]), ("SnapEDA", "https://www.snapeda.com")],
)

L08 = dict(
  id="thu-vien-chan-xuyen", short="Footprint chân xuyên", title="Thiết kế thư viện linh kiện chân xuyên (THT)", icon="📌", time="2 giờ",
  goal="Tự vẽ symbol và footprint chân xuyên chính xác từ datasheet.",
  goals=["Đọc bản vẽ kích thước trong datasheet", "Tính lỗ khoan và pad", "Vẽ footprint DIP, header, TO-220 bằng tay và bằng IPC Footprint Wizard",
         "Vẽ symbol, gán footprint, thêm 3D"],
  sections=[
    dict(h="Lỗ khoan và pad", fig=figs.tht_pad(), code="02-lo-khoan-pad-cham-xuyen.py", after=CALC_HOLE,
         notes=["Header 2.54 mm có chân vuông 0.64 mm → đường chéo 0.91 mm → lỗ 1.2 mm, pad 1.8 mm, vẫn đủ chỗ đi 1 đường giữa 2 chân.",
                "Diode 3 A chân to 1.3 mm cần lỗ 1.5 mm — dùng nhầm footprint của diode 1 A (lỗ 0.8 mm) sẽ không cắm được linh kiện."]),
    dict(h="Các bước vẽ footprint trong PcbLib", html="""
<ol><li>Tools → New Blank Footprint, đặt tên theo quy ước (ví dụ <code>DIP8_W7.62mm</code>, <code>TO220-3_Vertical</code>).</li>
<li>Đặt pad (<kbd>P</kbd><kbd>P</kbd>) lớp Multi-Layer, nhập kích thước lỗ và pad đã tính; pad 1 hình vuông/chữ nhật.</li>
<li>Đặt pad theo toạ độ chính xác (khoảng cách chân 2.54 mm, hàng cách 7.62 mm với DIP-8) — dùng Edit → Set Reference → Center để gốc toạ độ ở tâm linh kiện.</li>
<li>Vẽ khung trên <b>Top Overlay</b> (nét 0.15–0.2 mm) và dấu chân 1; vẽ <b>courtyard</b> trên lớp Mechanical.</li>
<li>Gắn mô hình 3D (Place → 3D Body → .step).</li>
<li>Nhanh hơn: Tools → <b>IPC Compliant Footprint Wizard</b> → chọn loại gói (DIP, SIP…), nhập kích thước datasheet.</li></ol>"""),
  ],
  mistakes=["Nhìn nhầm kích thước inch/mm trong datasheet.", "Đặt gốc toạ độ lệch → máy gắp đặt sai vị trí.", "Footprint nhìn từ dưới (bottom view) bị lật ngược thứ tự chân."],
  exercises=["Vẽ footprint IC DIP-8, relay SRD-05VDC, terminal KF301-2P từ datasheet.", "Tạo symbol cho IC NE555 và gán footprint DIP-8 vừa vẽ."],
  refs=[("Tài liệu khóa thư viện (Google Drive)", DRIVE["thuvien"])],
)

L09 = dict(
  id="thu-vien-chan-dan", short="Footprint IC chân dán", title="Thiết kế thư viện IC chân dán (SMD)", icon="🔲", time="2 giờ",
  goal="Vẽ footprint SMD chuẩn IPC-7351 cho IC (SOIC, SOT-23, QFN, QFP).",
  goals=["Hiểu land pattern: toe, heel, side fillet", "Dùng IPC Compliant Footprint Wizard", "Thêm pad tản nhiệt (exposed pad), lớp paste, courtyard"],
  sections=[
    dict(h="Land pattern IPC-7351", fig=figs.smd_land(), html="""
<p>Pad SMD phải dài hơn chân linh kiện để tạo <b>mối hàn</b> đẹp: phần nhô ra phía ngoài (toe), phía trong (heel) và hai bên (side). IPC-7351 có 3 mức mật độ: <b>Most</b> (pad to, dễ hàn tay), <b>Nominal</b> (cân bằng – mặc định), <b>Least</b> (mạch dày đặc).</p>
<table class="tbl"><tr><th>Gói</th><th>Ghi chú khi vẽ</th></tr>
<tr><td>SOT-23</td><td>3 chân, thứ tự chân khác nhau giữa các hãng — kiểm tra kỹ (đặc biệt MOSFET, LDO)</td></tr>
<tr><td>SOIC-8</td><td>bước chân 1.27 mm, pad ~1.5 × 0.6 mm</td></tr>
<tr><td>QFN</td><td>chân nằm dưới thân + pad tản nhiệt giữa (nối GND, có via tản nhiệt); chia paste thành ô nhỏ (~50–60% diện tích)</td></tr>
<tr><td>QFP / TQFP</td><td>bước 0.5–0.8 mm, cần solder mask giữa các pad</td></tr></table>"""),
    dict(h="Quy trình với IPC Compliant Footprint Wizard", html="""
<ol><li>Tools → IPC Compliant Footprint Wizard → chọn họ (SOIC, SOT23, QFN, PQFP…).</li>
<li>Nhập kích thước tổng thể và kích thước chân lấy từ <b>bảng kích thước</b> trong datasheet (min/max).</li>
<li>Chọn mức mật độ, kiểm tra hình xem trước, đặt tên theo chuẩn IPC (ví dụ <code>SOIC127P600X175-8N</code>).</li>
<li>Kiểm tra pad tản nhiệt, lớp paste, dấu chân 1, tâm toạ độ; gắn 3D.</li></ol>"""),
  ],
  mistakes=["Quên solder mask giữa các pad bước nhỏ → chân dính thiếc.", "Pad tản nhiệt QFN phủ paste kín → linh kiện “nổi” lên, chân không ăn thiếc.", "Lấy kích thước điển hình (typ) thay vì min/max."],
  exercises=["Vẽ footprint SOIC-8 cho EEPROM 24C02 và SOT-23-5 cho LDO MIC5219.", "Vẽ footprint QFN-16 3×3 mm có pad tản nhiệt và 4 via tản nhiệt."],
  refs=[("Tài liệu khóa thư viện (Google Drive)", DRIVE["thuvien"])],
)

L10 = dict(
  id="thu-vien-dien-tro", short="Tính footprint R, C", title="Tính toán thiết kế thư viện điện trở, tụ điện dán", icon="📏", time="1,5 giờ",
  goal="Tự tính kích thước pad cho linh kiện chip (0402–1206) bằng công thức IPC-7351 và tạo footprint.",
  goals=["Hiểu mã kích thước 0402/0603/0805/1206 hệ inch và hệ mét", "Áp dụng công thức Z, G, X", "Chọn kích thước phù hợp hàn tay hay hàn máy"],
  sections=[
    dict(h="Kích thước linh kiện chip", fig=figs.chip_sizes(), html="""
<table class="tbl"><tr><th>Mã (inch)</th><th>Mã (mét)</th><th>Công suất điện trở thường gặp</th><th>Gợi ý</th></tr>
<tr><td>0402</td><td>1005</td><td>1/16 W</td><td>chỉ hàn máy</td></tr>
<tr><td>0603</td><td>1608</td><td>1/10 W</td><td>hàn tay được với nhíp + kính lúp</td></tr>
<tr><td>0805</td><td>2012</td><td>1/8 W</td><td><b>dễ hàn tay nhất cho người mới</b></td></tr>
<tr><td>1206</td><td>3216</td><td>1/4 W</td><td>dòng/áp lớn hơn</td></tr>
<tr><td>2512</td><td>6332</td><td>1 W</td><td>điện trở shunt đo dòng</td></tr></table>"""),
    dict(h="Tính land pattern", code="03-footprint-chip-smd.py", notes=[
        "Kết quả 0603: pad 0.75 × 0.90 mm, tâm cách tâm 1.66 mm — gần với footprint chuẩn của các hãng.",
        "Muốn dễ hàn tay hơn: chọn mức Most (Jt = 0.55) → pad dài thêm 0.2 mm về phía ngoài.",
        "Courtyard (vùng chiếm chỗ) giúp DRC phát hiện hai linh kiện đặt quá sát nhau."]),
  ],
  exercises=["Tính và vẽ footprint tụ 1210 (3.2 × 2.5 mm).", "So sánh footprint 0805 tự tính với footprint trong thư viện mặc định của Altium."],
  refs=[("Tài liệu khóa thư viện (Google Drive)", DRIVE["thuvien"])],
)

L11 = dict(
  id="4-lop", short="Mạch 4 lớp & stack-up", title="Thiết kế mạch 4 lớp, stack-up và trở kháng (Altium 18)", icon="🧱", time="3 giờ",
  goal="Thiết kế mạch 4 lớp đúng chuẩn: chọn stack-up, mặt GND/nguồn, đường trở kháng có kiểm soát.",
  goals=["Dùng Layer Stack Manager trong Altium 18", "Hiểu vì sao stack-up SIG–GND–PWR–SIG phổ biến", "Hiểu đường hồi dòng (return path)",
         "Tính bề rộng đường 50 Ω và cặp vi sai 90 Ω"],
  sections=[
    dict(h="Stack-up 4 lớp", fig=figs.cross_section(True), html="""
<p>Layer Stack Manager (<b>Design → Layer Stack Manager</b>): thêm 2 lớp nội (Internal Plane cho mặt nguồn/GND, hoặc Signal Layer). Nhập độ dày prepreg/lõi và hằng số điện môi theo stack-up của xưởng (JLCPCB công bố stack-up JLC04161H-7628).</p>
<ul><li><b>L2 = GND liền mạch</b>: mọi tín hiệu ở L1 có đường hồi ngay bên dưới, cách 0.21 mm → nhiễu giảm mạnh.</li>
<li><b>L3 = nguồn</b>: chia vùng 3V3, 5V bằng Split Plane.</li>
<li>Tín hiệu đi ở L1 và L4; khi đổi lớp tín hiệu nhanh, đặt via GND ngay cạnh via tín hiệu.</li></ul>"""),
    dict(h="Đường hồi dòng", fig=figs.return_path(), html="<p>Ở tần số cao, dòng hồi luôn đi theo đường có <b>cảm kháng nhỏ nhất</b> — ngay bên dưới đường tín hiệu. Nếu mặt GND bị cắt bởi khe hở, dòng hồi phải đi vòng, tạo vòng dòng lớn = anten phát nhiễu. <b>Không bao giờ</b> cho tín hiệu nhanh đi qua khe của mặt GND.</p>"),
    dict(h="Trở kháng có kiểm soát", fig=figs.microstrip(), code="04-tro-khang-microstrip.py", notes=[
        "Mạch 4 lớp: đường 50 Ω chỉ rộng 0.35 mm — dễ đi tới anten, connector u.FL.",
        "Mạch 2 lớp dày 1.6 mm: đường 50 Ω phải rộng 2.76 mm — lý do RF và USB tốc độ cao nên dùng 4 lớp.",
        "Altium 18 tính trở kháng ngay trong Layer Stack Manager (tab Impedance) và đặt rule Width theo trở kháng."]),
  ],
  mistakes=["Đặt hai lớp tín hiệu kề nhau ở giữa mà không có mặt tham chiếu.", "Chia vụn mặt GND ở L2.", "Dùng stack-up mặc định của Altium thay vì stack-up thật của xưởng."],
  exercises=["Tạo stack-up 4 lớp theo thông số JLC04161H-7628 trong Altium.", "Tính bề rộng đường 50 Ω cho anten chip 2.4 GHz và cặp USB 90 Ω."],
  refs=[("Tài liệu khóa Altium 4 lớp & highspeed (Google Drive)", DRIVE["4lop"]), ("JLCPCB stack-up & impedance", "https://jlcpcb.com/impedance")],
)

L12 = dict(
  id="chong-nhieu", short="Chống nhiễu (EMC)", title="Thiết kế chống nhiễu và tín hiệu tốc độ cao", icon="📡", time="3 giờ",
  goal="Áp dụng các quy tắc layout giúp mạch chạy ổn định, ít nhiễu, đạt EMC.",
  goals=["Đặt tụ decoupling đúng", "Bố trí thạch anh, analog/digital, nguồn xung", "Đi cặp vi sai, cân chiều dài", "Quy tắc 3W, 20H, via stitching"],
  sections=[
    dict(h="Nguồn và tụ decoupling", fig=figs.decoupling(), html="""
<ul><li>Mỗi chân nguồn IC có một tụ 100 nF đặt <b>sát nhất</b> có thể, via GND ngay cạnh tụ; thêm tụ 10 µF cho cả khối.</li>
<li>Dòng đi: nguồn → tụ → chân IC (đi qua tụ trước rồi mới vào IC).</li>
<li>Nguồn xung (buck): vòng dòng gồm tụ vào – MOSFET – diode phải nhỏ nhất; cuộn cảm và chân SW tránh xa tín hiệu nhạy.</li></ul>"""),
    dict(h="Tín hiệu tốc độ cao", fig=figs.diff_pair(), html="""
<ul><li><b>Thạch anh</b> sát chân vi điều khiển, tụ tải đối xứng, bao quanh bằng GND, không đi dây khác bên dưới.</li>
<li><b>Analog/Digital</b>: đặt tách vùng, dùng chung một mặt GND liền nhưng không để dòng digital chạy qua vùng analog.</li>
<li><b>Cặp vi sai</b> (USB, CAN, RS485, Ethernet): Altium → Place → Differential Pair Routing; đặt rule Differential Pairs; cân chiều dài bằng Interactive Length Tuning.</li>
<li><b>Via stitching</b> dọc mép mạch và quanh vùng RF mỗi λ/20.</li></ul>"""),
  ],
  embedded=["ESP32: chân EN cần mạch RC (10k + 1 µF) chống reset do nhiễu; chân GPIO0 có điện trở kéo lên.",
            "Động cơ DC: tụ 100 nF hàn trực tiếp hai cực động cơ, dây động cơ xoắn đôi, driver và MCU dùng GND công suất riêng nối tại một điểm."],
  mistakes=["Tụ decoupling đặt xa, nối bằng đường dài mảnh.", "Đường clock chạy song song sát đường analog.", "Đổ đồng tạo “đảo” đồng không nối GND (anten nhỏ)."],
  exercises=["Rà soát mạch dự án mẫu theo checklist chống nhiễu, chỉ ra 5 điểm cần sửa.", "Đi cặp USB D+/D− từ connector USB-C tới CH340C với lệch chiều dài < 0.5 mm."],
  refs=[("Tài liệu khóa Altium 4 lớp & highspeed (Google Drive)", DRIVE["4lop"])],
)

L13 = dict(
  id="that-co-chai", short="Dòng lớn & thắt cổ chai", title="Sửa lỗi thắt cổ chai và layout “đường ống nước” cho dòng lớn", icon="🚰", time="2 giờ",
  goal="Tính và vẽ đúng đường dòng lớn: bề rộng, via, polygon, thermal relief — tránh điểm nghẽn gây nóng cháy.",
  goals=["Tính bề rộng đường theo dòng và mức tăng nhiệt (IPC-2221)", "Phát hiện và sửa điểm thắt cổ chai", "Tính số via cần thiết",
         "Dùng polygon, đồng dày, thermal relief hợp lý"],
  sections=[
    dict(h="Dòng điện như nước chảy trong ống", fig=figs.bottleneck(), html="<p>Lưu lượng của cả đường ống do <b>chỗ hẹp nhất</b> quyết định. Một đường nguồn rộng 3 mm nhưng phải lách qua giữa 2 chân IC bằng đoạn 0.25 mm thì khả năng chịu dòng chỉ còn của đoạn 0.25 mm. Các điểm hẹp hay bị bỏ sót: lối vào pad, chỗ đổi lớp (1 via duy nhất), chỗ polygon bị thắt bởi via/lỗ, cổ thermal relief.</p>"),
    dict(h="Tính bề rộng đường", fig=figs.trace_chart(), figcap="Bề rộng tối thiểu theo dòng, đồng 1 oz, tăng nhiệt 10 °C (tính bằng công thức IPC-2221).",
         code="01-be-rong-duong-mach.py", notes=["1 A cần 0.30 mm ở lớp ngoài nhưng 0.78 mm ở lớp trong — lớp trong khó toả nhiệt.",
                                                  "Đồng 2 oz cho phép đường hẹp đi một nửa.",
                                                  "Ngoài nhiệt, kiểm tra cả sụt áp: 2 A qua đường 0.8 mm dài 50 mm mất 61 mV."]),
    dict(h="Via và thermal relief", fig=figs.thermal_relief(), code="05-via-dong-dien.py",
         notes=["Một via 0.3 mm chịu khoảng 1 A → 5 A cần cụm 7 via.", "Altium: Design → Rules → Plane → Polygon Connect Style chọn Relief Connect cho chân tín hiệu, Direct Connect cho net dòng lớn."]),
  ],
  mistakes=["Đường nguồn đổi lớp qua 1 via nhỏ.", "Polygon bị via và lỗ cắt thành dải hẹp.", "Thermal relief nan mảnh trên chân cấp nguồn động cơ."],
  exercises=["Rà soát mạch driver động cơ 5 A: tìm mọi điểm thắt cổ chai và sửa.", "Dùng máy tính ở bài 4: đường 10 A ở lớp ngoài 2 oz, tăng nhiệt 20 °C cần rộng bao nhiêu?"],
  refs=[("Tài liệu sửa lỗi thắt cổ chai & layout đường ống nước (Google Drive)", DRIVE["thatco"])],
)

L14 = dict(
  id="mach-dieu-khien", short="Mạch điều khiển", title="Thiết kế mạch điều khiển (vi điều khiển + công suất)", icon="🎛", time="3 giờ",
  goal="Bố trí mạch có cả vi điều khiển và phần công suất (driver động cơ, relay) chạy ổn định, an toàn.",
  goals=["Bố trí module ESP32/STM32: anten, nguồn, nạp code", "Layout mạch cầu H / driver động cơ", "Cách ly công suất – tín hiệu, relay, optocoupler"],
  sections=[
    dict(h="Khối vi điều khiển", fig=figs.module_layout(), html="""
<ul><li>Module WiFi: anten nhô ra ngoài mép mạch hoặc vùng dưới anten không có đồng ở <b>mọi lớp</b>.</li>
<li>Mạch nạp: CH340/CP2102 + 2 transistor tự động EN/GPIO0; header UART dự phòng.</li>
<li>Chân I/O ra ngoài (connector) có điện trở nối tiếp 100–330 Ω hoặc TVS chống tĩnh điện.</li></ul>"""),
    dict(h="Khối công suất", fig=figs.hbridge_loop(), html="""
<ul><li>Driver động cơ (L298N, TB6612, DRV8833, cầu H MOSFET): tụ bulk + tụ gốm sát nguồn driver; đường động cơ rộng theo dòng (xem bài 13).</li>
<li>Diode xả (flyback) song song cuộn relay/động cơ; transistor/MOSFET kích relay có điện trở kéo xuống ở cực G/B.</li>
<li>Điện áp cao (220 V): khoảng cách cách điện ≥ 3 mm, có khe phay (slot) giữa phần cao áp và hạ áp, dùng optocoupler/relay cách ly.</li></ul>"""),
  ],
  mistakes=["GND động cơ dùng chung đường mảnh với GND vi điều khiển → MCU reset khi động cơ khởi động.", "Thiếu diode flyback → đỉnh áp làm chết transistor.", "Đồng dưới anten WiFi."],
  exercises=["Thiết kế mạch điều khiển robot 2 động cơ DC dùng ESP32 + TB6612, nguồn pin 2S.", "Thiết kế mạch 4 relay điều khiển thiết bị 220 V có cách ly an toàn."],
  refs=[("Tài liệu khóa Altium 4 lớp & highspeed (Google Drive)", DRIVE["4lop"])],
)

L15 = dict(
  id="do-dong-ap", short="Mạch đo dòng & đo áp", title="Thiết kế mạch đo dòng và đo áp", icon="📈", time="2 giờ",
  goal="Thiết kế mạch đo điện áp và dòng điện chính xác cho vi điều khiển: phân áp, shunt, khuếch đại, lọc và layout Kelvin.",
  goals=["Tính cầu phân áp cho ADC", "Chọn điện trở shunt, bộ khuếch đại dòng (INA180/INA219), cảm biến Hall (ACS712)", "Lọc nhiễu RC trước ADC",
         "Layout Kelvin và đường analog sạch"],
  sections=[
    dict(h="Tính toán", code="06-do-dong-do-ap.py", after=CALC_DIV, notes=[
        "Cầu 100k/10k cho pin 6S: áp vào ADC tối đa 2.29 V — an toàn và nằm trong vùng ADC ESP32 tuyến tính tốt (khoảng 0.15–2.5 V).",
        "Shunt 10 mΩ + INA180 gain 50: 5 A cho 2.5 V, độ phân giải 1.6 mA/bước.",
        "Mạch đo áp ăn dòng liên tục 229 µA — với thiết bị chạy pin lâu ngày, dùng điện trở lớn hơn hoặc MOSFET ngắt cầu phân áp khi không đo."]),
    dict(h="Layout mạch đo", fig=figs.kelvin(), html="""
<ul><li><b>Kelvin 4 dây</b>: dây cảm biến nối riêng vào hai đầu shunt (footprint shunt 4 pad hoặc tách đường ngay tại pad).</li>
<li>Hai dây cảm biến đi song song, sát nhau như cặp vi sai, tới chân IN+/IN− của bộ khuếch đại.</li>
<li>Tụ lọc RC đặt sát chân ADC; đường analog tránh xa nguồn xung, thạch anh, đường PWM.</li>
<li>Low-side (shunt phía GND) dễ làm nhưng làm “nổi” GND của tải; high-side (phía nguồn) cần IC chịu được điện áp chung (common-mode) cao như INA180/INA226.</li></ul>"""),
  ],
  summary=["Khóa basic: nguyên lý → layout 2 lớp → xuất file → dự án mẫu.", "Thư viện: đọc datasheet, tính lỗ/pad THT, land pattern SMD theo IPC-7351.",
           "Nâng cao: stack-up 4 lớp, đường hồi dòng, trở kháng, chống nhiễu, dòng lớn, mạch điều khiển và đo lường."],
  exercises=["Thiết kế mạch đo điện áp pin 3S và dòng tải tối đa 3 A cho ESP32, kèm lọc RC.", "Vẽ footprint shunt 2512 có 4 pad Kelvin."],
  refs=[("Tài liệu khóa Altium 4 lớp & highspeed (Google Drive)", DRIVE["4lop"]), ("TI – Current sense amplifiers", "https://www.ti.com/amplifier-circuit/current-sense/overview.html")],
)

GROUPS = [
    ("basic", "Khóa Basic", "Logo, nguyên lý, layout, dự án mẫu", [L01, L02, L03, L04, L05, L06]),
    ("thu-vien", "Khóa thiết kế thư viện", "Thư viện, chân xuyên, chân dán, R/C", [L07, L08, L09, L10]),
    ("4-lop", "Khóa 4 lớp & highspeed", "Stack-up, chống nhiễu, dòng lớn, điều khiển, đo lường", [L11, L12, L13, L14, L15]),
]
