# -*- coding: utf-8 -*-
"""Khóa Python cơ bản (THCS – THPT, chưa biết lập trình).  Build: python -X utf8 course.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "common")]
import coursekit
import figs

CODE = os.path.join(HERE, "code")
_runner = coursekit.Runner(os.path.join(HERE, "out", "run-cache.json"))


def run(path, stdin):
    return f"python {os.path.basename(path)}", coursekit.run_py(path, stdin, runner=_runner)


def sin(name):
    return open(os.path.join(CODE, name), encoding="utf-8").read()


L = []
L.append(dict(
  id="gioi-thieu", short="Làm quen Python", title="Làm quen với Python", icon="🐍", time="1,5 giờ",
  goal="Biết Python là gì, cài đặt và chạy chương trình đầu tiên; dùng Python như một máy tính bỏ túi.",
  goals=["Cài Python và trình soạn thảo (Thonny / VS Code)", "Viết, lưu và chạy file .py", "Dùng print(), chú thích và các phép tính cơ bản"],
  sections=[
    dict(h="Python là gì, dùng để làm gì?", fig=figs.python_where(), html="""
<p><b>Python</b> là ngôn ngữ lập trình do Guido van Rossum tạo ra năm 1991. Cú pháp gần với tiếng Anh, ít ký hiệu rườm rà nên rất hợp cho người mới — nhưng cũng là ngôn ngữ số 1 cho <b>AI, khoa học dữ liệu</b> và tự động hoá. Python là ngôn ngữ <b>thông dịch</b>: chạy từng dòng, không cần biên dịch trước.</p>"""),
    dict(h="Cài đặt", html="""
<table class="tbl"><tr><th>Cách</th><th>Phù hợp</th></tr>
<tr><td><b>Thonny</b> (thonny.org) – cài một lần có sẵn Python</td><td>học sinh mới bắt đầu, có chế độ chạy từng bước; nạp được MicroPython cho ESP32</td></tr>
<tr><td><b>python.org</b> + <b>VS Code</b> (extension Python)</td><td>học lâu dài, làm dự án. Khi cài nhớ tick <i>Add python.exe to PATH</i></td></tr>
<tr><td>Chạy trên web: <a href="https://www.online-python.com" target="_blank" rel="noopener">online-python.com</a>, Google Colab</td><td>không cài gì, dùng máy trường</td></tr></table>
<p>Hai cách chạy: gõ từng lệnh trong <b>chế độ tương tác</b> (dấu nhắc <code>&gt;&gt;&gt;</code>) hoặc lưu thành file <code>bai1.py</code> rồi chạy <code>python bai1.py</code>.</p>"""),
    dict(h="Chương trình đầu tiên", code="01-xin-chao.py", notes=[
      "<code>print(...)</code> in ra màn hình; nhiều giá trị cách nhau bởi dấu phẩy sẽ được in cách một dấu cách.",
      "<code>/</code> luôn ra số thực, <code>//</code> chia lấy phần nguyên, <code>%</code> lấy dư, <code>**</code> lũy thừa.",
      "Số nguyên trong Python không giới hạn độ lớn — <code>2 ** 100</code> vẫn chính xác.",
      "<code>\\n</code> xuống dòng, <code>\\t</code> tab; <code>\"=\" * 30</code> lặp chuỗi 30 lần."]),
  ],
  mistakes=["Gõ <code>Print</code> (chữ P hoa) — Python phân biệt chữ hoa, chữ thường.", "Quên dấu ngoặc kép quanh chữ: <code>print(Xin chao)</code> → lỗi NameError.", "Thụt lề đầu dòng lung tung — Python dùng thụt lề để hiểu cấu trúc."],
  exercises=["In ra thông tin giới thiệu bản thân trên 4 dòng, có một dòng kẻ bằng 40 dấu “-”.", "Tính và in: số giây trong một năm; 2 mũ 64; phần dư của 2026 chia 7."],
))
L.append(dict(
  id="bien-kieu", short="Biến & kiểu dữ liệu", title="Biến, kiểu dữ liệu và toán tử", icon="📦", time="1,5 giờ",
  goal="Lưu dữ liệu vào biến, phân biệt các kiểu cơ bản và chuyển đổi giữa chúng.",
  goals=["Đặt tên biến đúng quy tắc", "Hiểu int, float, str, bool và hàm type()", "Ép kiểu với int(), float(), str()", "Dùng toán tử số học, so sánh, logic"],
  sections=[
    dict(h="Biến", fig=figs.bien_hop(), html="""
<p>Biến là tên dùng để giữ một giá trị: <code>tuoi = 12</code>. Python <b>tự biết kiểu</b> dựa vào giá trị, không cần khai báo trước.</p>
<p>Quy tắc đặt tên: chữ cái, chữ số, dấu gạch dưới; không bắt đầu bằng số; không dùng từ khoá (<code>if</code>, <code>for</code>…); phân biệt hoa thường. Quy ước: chữ thường nối bằng gạch dưới — <code>diem_trung_binh</code>.</p>"""),
    dict(h="Kiểu dữ liệu, ép kiểu, toán tử", code="02-bien-kieu-du-lieu.py", html="""
<table class="tbl"><tr><th>Kiểu</th><th>Ví dụ</th><th>Ghi chú</th></tr>
<tr><td><code>int</code></td><td><code>12</code>, <code>-5</code></td><td>số nguyên</td></tr><tr><td><code>float</code></td><td><code>1.52</code>, <code>3e8</code></td><td>số thực (có sai số nhỏ)</td></tr>
<tr><td><code>str</code></td><td><code>"An"</code>, <code>'7A'</code></td><td>chuỗi ký tự</td></tr><tr><td><code>bool</code></td><td><code>True</code>, <code>False</code></td><td>đúng / sai</td></tr></table>""",
         notes=["<code>\"25\" + \"25\"</code> là nối chuỗi; muốn cộng số phải <code>int()</code> trước.",
                "<code>int(9.99)</code> cắt bỏ phần lẻ, <code>round()</code> mới làm tròn.",
                "<code>a, b = b, a</code> — cách hoán đổi hai biến đặc trưng của Python.",
                "Số thực lưu dạng nhị phân nên <code>0.1 + 0.2</code> hơi lệch; dùng <code>round()</code> khi in."]),
  ],
  exercises=["Đổi nhiệt độ 37°C sang độ F (F = C × 9/5 + 32).", "Cho số giây 3725, in ra dạng giờ:phút:giây bằng <code>//</code> và <code>%</code>."],
))
L.append(dict(
  id="nhap-xuat", short="Nhập & xuất", title="Nhập dữ liệu và in kết quả đẹp", icon="⌨️", time="1 giờ",
  goal="Nhận dữ liệu từ bàn phím bằng input() và trình bày kết quả gọn gàng bằng f-string.",
  goals=["Dùng input() và ép kiểu kết quả", "Dùng f-string, định dạng số chữ số thập phân, căn lề", "Nhập nhiều giá trị trên một dòng"],
  sections=[dict(h="input() và f-string", code="03-nhap-xuat.py", stdin=sin("03-nhap-xuat.stdin"), notes=[
      "<code>input()</code> luôn trả về <b>chuỗi</b> → muốn tính toán phải <code>int()</code>/<code>float()</code>.",
      "f-string: <code>f\"{bien:.1f}\"</code> 1 chữ số thập phân, <code>{x:&gt;8}</code> căn phải rộng 8, <code>{x:.0%}</code> phần trăm.",
      "<code>map(int, input().split())</code> tách dòng theo dấu cách rồi đổi từng phần sang số."])],
  mistakes=["Cộng trực tiếp hai giá trị input() → bị nối chuỗi.", "Nhập số thập phân bằng dấu phẩy (1,55) → lỗi; Python dùng dấu chấm."],
  exercises=["Nhập bán kính, in chu vi và diện tích hình tròn với 2 chữ số thập phân.", "Nhập giá một món hàng và số lượng, in hoá đơn có căn lề."],
))
L.append(dict(
  id="dieu-kien", short="Rẽ nhánh", title="Câu lệnh điều kiện", icon="🔀", time="1,5 giờ",
  goal="Cho chương trình ra quyết định với if / elif / else và match-case.",
  goals=["Viết if – elif – else và hiểu thụt lề", "Kết hợp điều kiện bằng and, or, not", "Dùng biểu thức điều kiện một dòng và match-case"],
  sections=[dict(h="if / elif / else", code="04-dieu-kien.py", stdin=sin("04-dieu-kien.stdin"), html="""
<p>Khối lệnh thuộc <code>if</code> được nhận biết bằng <b>dấu hai chấm</b> và <b>thụt lề 4 dấu cách</b>. Các nhánh <code>elif</code> được xét lần lượt; gặp nhánh đúng đầu tiên thì bỏ qua các nhánh còn lại.</p>""",
      notes=["Thứ tự elif quan trọng: kiểm tra điểm từ cao xuống thấp.",
             "Năm nhuận là bài tập kinh điển về kết hợp <code>and</code>/<code>or</code>.",
             "<code>.strip().lower()</code> chuẩn hoá chữ người dùng gõ (bỏ khoảng trắng, chữ thường) trước khi so sánh."])],
  mistakes=["Dùng <code>=</code> thay vì <code>==</code> trong điều kiện.", "Quên dấu <code>:</code> cuối dòng if.", "Thụt lề không đều (trộn tab và dấu cách)."],
  exercises=["Nhập 3 cạnh, kiểm tra có phải tam giác không và là tam giác gì (đều, cân, vuông, thường).", "Tính tiền điện bậc thang theo số kWh nhập vào."],
))
L.append(dict(
  id="vong-lap", short="Vòng lặp", title="Vòng lặp for và while", icon="🔁", time="2 giờ",
  goal="Lặp lại công việc với for/while, điều khiển vòng lặp bằng break/continue và viết trò chơi đoán số.",
  goals=["Dùng for với range()", "Dùng while khi chưa biết trước số lần lặp", "Dùng break, continue, vòng lặp lồng nhau"],
  sections=[dict(h="for, while và trò chơi đoán số", fig=figs.vong_lap(), code="05-vong-lap.py", stdin=sin("05-vong-lap.stdin"),
      notes=["<code>range(a, b, buoc)</code> chạy từ a tới <b>trước</b> b.", "<code>print(..., end=\" \")</code> in không xuống dòng.",
             "Trò chơi dùng <code>random.seed(7)</code> để số bí mật cố định — bỏ dòng này để mỗi lần chơi một số khác.",
             "Chiến lược đoán tốt nhất là chia đôi khoảng (50 → 25 → 37…): tối đa 7 lần cho 100 số — đây là ý tưởng của <b>tìm kiếm nhị phân</b>."])],
  mistakes=["while quên cập nhật biến điều kiện → lặp vô hạn (bấm Ctrl+C để dừng).", "Nhầm range(1, 10) có cả số 10."],
  exercises=["In các số nguyên tố nhỏ hơn 100.", "Vẽ tam giác sao * có n dòng bằng vòng lặp lồng nhau.", "Sửa trò chơi: giới hạn 7 lần đoán và cho chơi lại."],
))
L.append(dict(
  id="chuoi", short="Chuỗi", title="Xử lý chuỗi (string)", icon="🔤", time="1,5 giờ",
  goal="Cắt, tìm, thay thế, tách và ghép chuỗi — xử lý văn bản và dữ liệu cảm biến.",
  goals=["Dùng chỉ số và cắt lát", "Dùng các phương thức upper, find, replace, split, join, strip", "Duyệt từng ký tự"],
  sections=[dict(h="Thao tác với chuỗi", code="06-chuoi.py", fig=figs.list_chi_so(), figcap="Chỉ số dương và âm dùng giống nhau cho chuỗi và list.",
      notes=["<code>s[::-1]</code> đảo ngược chuỗi.", "Chuỗi là bất biến: mọi phương thức trả về chuỗi <b>mới</b>.",
             "Phân tích chuỗi <code>\"T:28.5;H:61\"</code> là kỹ năng dùng hằng ngày khi đọc dữ liệu từ Arduino/ESP32 qua Serial."])],
  exercises=["Đếm số chữ hoa, chữ thường, chữ số trong một câu.", "Chuẩn hoá họ tên: “  nGuyEn   vAn  an ” → “Nguyen Van An”."],
))
L.append(dict(
  id="list-tuple", short="List & tuple", title="Danh sách (list) và tuple", icon="📋", time="2 giờ",
  goal="Lưu nhiều giá trị trong một biến, thêm/xoá/sắp xếp, dùng list comprehension.",
  goals=["Tạo, truy cập, sửa list", "append, insert, remove, pop, sort, sorted", "len, sum, min, max, enumerate", "List comprehension; tuple"],
  sections=[dict(h="Làm việc với list", code="07-list-tuple.py", notes=[
      "<code>sort()</code> sửa ngay list; <code>sorted()</code> tạo list mới.", "<code>[x*x for x in range(1, 8)]</code> — list comprehension, gọn hơn vòng for + append.",
      "<code>b = a</code> không sao chép: a và b là <b>cùng một</b> list. Dùng <code>a.copy()</code>.", "Tuple dùng cho dữ liệu không đổi như toạ độ, ngày tháng."])],
  exercises=["Nhập điểm 10 bạn, in điểm cao nhất, thấp nhất, trung bình và số bạn trên trung bình.", "Xoá các phần tử trùng trong list nhưng giữ nguyên thứ tự."],
))
L.append(dict(
  id="dict-set", short="Dict & set", title="Từ điển (dict) và tập hợp (set)", icon="📖", time="1,5 giờ",
  goal="Tổ chức dữ liệu theo khoá – giá trị, đếm tần suất, dùng phép toán tập hợp.",
  goals=["Tạo, đọc, sửa dict; duyệt items()", "Đếm tần suất bằng dict", "List các dict như một bảng dữ liệu", "Set và phép giao, hợp, hiệu"],
  sections=[dict(h="Dict và set", fig=figs.dict_fig(), code="08-dict-set.py", notes=[
      "<code>d.get(k, mac_dinh)</code> không lỗi khi khoá chưa có — rất hợp để đếm.", "<code>max(dem, key=dem.get)</code> tìm khoá có giá trị lớn nhất.",
      "<code>key=lambda h: h[\"diem\"]</code> sắp xếp danh sách học sinh theo điểm.", "Set tự bỏ phần tử trùng; <code>&amp;</code> giao, <code>|</code> hợp, <code>-</code> hiệu."])],
  exercises=["Từ điển Anh – Việt mini: nhập từ, in nghĩa hoặc “chưa có”.", "Đếm số lần mỗi chữ cái xuất hiện trong tên của cả lớp."],
))
L.append(dict(
  id="ham", short="Hàm", title="Hàm (function)", icon="🧩", time="2 giờ",
  goal="Chia chương trình thành các hàm nhỏ, dễ đọc, dùng lại được.",
  goals=["def, tham số, return", "Tham số mặc định, gọi theo tên, *args", "Phạm vi biến, global", "lambda và đệ quy"],
  sections=[dict(h="Định nghĩa và gọi hàm", fig=figs.ham_may(), code="09-ham.py", notes=[
      "Hàm không có <code>return</code> sẽ trả về <code>None</code>.", "<code>return a, b, c</code> trả về một tuple, nhận bằng <code>x, y, z = ham()</code>.",
      "Biến tạo trong hàm là biến cục bộ; tránh dùng <code>global</code> khi không cần — truyền tham số và trả kết quả thì rõ ràng hơn.",
      "Docstring (chuỗi ngay dưới def) mô tả hàm; xem bằng <code>help(ten_ham)</code>."])],
  exercises=["Viết hàm <code>la_nguyen_to(n)</code> và dùng nó in các số nguyên tố tới 200.", "Viết hàm <code>doi_tien(so_tien)</code> trả về số tờ 500k, 200k, 100k, 50k cần dùng."],
))
L.append(dict(
  id="module-file", short="Module & file", title="Module và đọc/ghi file", icon="💾", time="1,5 giờ",
  goal="Dùng thư viện có sẵn và lưu dữ liệu ra file để không mất khi tắt chương trình.",
  goals=["import module: math, random, datetime, statistics, csv, json", "Đọc/ghi file văn bản với with open()", "Làm việc với file CSV", "Cài thư viện ngoài bằng pip"],
  sections=[dict(h="Module có sẵn và file", code="10-module-file.py", html="""
<p><code>import ten_module</code> rồi dùng <code>ten_module.ham()</code>; hoặc <code>from module import ham</code>. Tự tạo module: lưu các hàm vào <code>tien_ich.py</code>, ở file khác viết <code>import tien_ich</code>. Thư viện ngoài cài bằng lệnh <code>pip install ten_thu_vien</code> (ví dụ <code>pip install numpy</code>).</p>
<table class="tbl"><tr><th>Chế độ open()</th><th>Ý nghĩa</th></tr><tr><td><code>"r"</code></td><td>đọc (mặc định)</td></tr><tr><td><code>"w"</code></td><td>ghi mới (xoá nội dung cũ)</td></tr><tr><td><code>"a"</code></td><td>ghi thêm vào cuối</td></tr></table>""",
      notes=["<code>with open(...) as f:</code> tự đóng file khi xong, kể cả khi có lỗi.", "Luôn ghi <code>encoding=\"utf-8\"</code> để tiếng Việt không bị lỗi.",
             "File CSV mở được bằng Excel — cách lưu dữ liệu cảm biến, điểm số đơn giản nhất."])],
  exercises=["Ghi bảng cửu chương 2–9 ra file <code>cuu_chuong.txt</code>.", "Đọc file CSV điểm, ghi ra file mới chỉ gồm học sinh có điểm trung bình ≥ 8."],
))
L.append(dict(
  id="loi-oop", short="Lỗi & lớp", title="Xử lý lỗi và lập trình hướng đối tượng", icon="🛡️", time="2 giờ",
  goal="Viết chương trình không “sập” khi người dùng nhập sai, và làm quen với lớp/đối tượng.",
  goals=["Đọc traceback để tìm lỗi", "try / except / else / finally, raise", "Tạo lớp với __init__, phương thức, __str__", "Kế thừa và ghi đè"],
  sections=[
    dict(h="Xử lý lỗi", code="11a-xu-ly-loi.py", html="<p>Đọc traceback từ <b>dưới lên</b>: dòng cuối cho biết loại lỗi và lý do, dòng phía trên cho biết file và số dòng gây lỗi.</p>",
         notes=["Chỉ bắt loại lỗi bạn biết cách xử lý; <code>except Exception</code> chung chung dễ che giấu lỗi thật.",
                "Dòng cuối cố ý gây lỗi để thấy traceback thật trông thế nào — chương trình dừng ngay tại đó."]),
    dict(h="Lớp và đối tượng", fig=figs.lop_doi_tuong(), code="11b-lop-doi-tuong.py", notes=[
      "<code>self</code> là đối tượng hiện tại; mọi phương thức đều nhận <code>self</code> là tham số đầu tiên.",
      "<code>__str__</code> quy định nội dung khi <code>print(doi_tuong)</code>.", "<code>super()</code> gọi phương thức của lớp cha."]),
  ],
  exercises=["Bọc bài tính BMI bằng try/except để nhập sai thì hỏi lại.", "Viết lớp <code>TaiKhoan</code> có nạp tiền, rút tiền (báo lỗi khi không đủ tiền) và in số dư."],
))
L.append(dict(
  id="du-an", short="Dự án sổ điểm", title="Dự án: chương trình sổ điểm có menu", icon="🏁", time="2–3 giờ",
  goal="Tổng hợp toàn bộ kiến thức trong một chương trình hoàn chỉnh có menu, kiểm tra dữ liệu và lưu file.",
  goals=["Thiết kế chương trình theo các hàm nhỏ", "Dùng dict lưu dữ liệu, json lưu file", "Xử lý mọi trường hợp nhập sai"],
  sections=[dict(h="Sổ điểm", code="12-du-an-so-diem.py", stdin=sin("12-du-an-so-diem.stdin"), notes=[
      "Menu là một dict: phím → (tên chức năng, hàm). Thêm chức năng mới chỉ cần thêm một dòng.",
      "Dữ liệu nhập mẫu cố tình có lỗi (trùng tên, điểm 11, học sinh không tồn tại) để thấy chương trình xử lý đúng.",
      "<code>json.dump(..., ensure_ascii=False)</code> lưu tiếng Việt đọc được trong file."])],
  summary=["Biến, kiểu, nhập/xuất, điều kiện, vòng lặp là nền tảng của mọi ngôn ngữ.", "list, dict, set giúp tổ chức dữ liệu; hàm và lớp giúp tổ chức chương trình.",
           "Học tiếp: <b>AI cơ bản</b> (Python + numpy, scikit-learn) hoặc <b>Arduino &amp; ESP32</b> (có thể lập trình bằng MicroPython)."],
  exercises=["Thêm chức năng: xoá học sinh, sửa điểm, đọc lại file khi khởi động.", "Viết trò chơi “Oẳn tù tì” với máy, lưu tỉ số vào file."],
))

GROUPS = [("nen-tang", "Nền tảng", "Biến, nhập xuất, điều kiện, vòng lặp", L[:5]),
          ("du-lieu", "Dữ liệu & hàm", "Chuỗi, list, dict, hàm, file", L[5:10]),
          ("nang-cao", "Hoàn thiện", "Xử lý lỗi, lớp, dự án", L[10:])]

_road = "".join(f'<div class="road"><div class="rb">Buổi {i + 1}</div><div><a href="#{x["id"]}">{x["title"]}</a><br><small>{x["time"]}</small></div></div>' for i, x in enumerate(L))
OVERVIEW = f"""
<h3><span class="n">?</span>Khóa học dành cho ai?</h3>
<div class="prose"><p>Học sinh từ <b>lớp 6</b> trở lên chưa từng lập trình (hoặc mới học kéo thả Scratch, Micro:bit) muốn bước sang lập trình bằng chữ. Python là cửa ngõ tới <b>AI</b>, khoa học dữ liệu và cả lập trình vi điều khiển (MicroPython).</p></div>
<div class="grid3"><div class="card"><h5>📖 12 bài ngắn gọn</h5><p>Mỗi bài một chủ đề, có mục tiêu, giải thích, lỗi hay gặp, bài tập.</p></div>
<div class="card"><h5>▶ Code chạy thật</h5><p>14 chương trình kèm dữ liệu nhập mẫu và kết quả chạy thật.</p></div>
<div class="card"><h5>🏁 Dự án cuối khóa</h5><p>Chương trình sổ điểm có menu, kiểm tra dữ liệu, lưu file.</p></div></div>
<h3><span class="n">⌚</span>Lộ trình gợi ý — {len(L)} buổi</h3><div class="roadmap">{_road}</div>
<h3><span class="n">→</span>Học tiếp</h3>
<div class="grid3"><div class="card"><h5><a href="ai-co-ban.html">🤖 AI cơ bản</a></h5><p>Hồi quy, phân loại, mạng nơ-ron với numpy và scikit-learn.</p></div>
<div class="card"><h5><a href="arduino-esp32.html">🔌 Arduino &amp; ESP32</a></h5><p>Điều khiển LED, cảm biến, động cơ, WiFi.</p></div>
<div class="card"><h5><a href="cpp-co-ban.html">💻 C++ cơ bản → nâng cao</a></h5><p>Ngôn ngữ chính của lập trình nhúng.</p></div></div>
"""

COURSE = dict(
    slug="python-co-ban", title="Python cơ bản", short_title="Python cơ bản", icon="🐍", lang="py",
    badge=f"{len(L)} bài · lớp 6+", tagline="Học lập trình bằng Python từ con số 0: biến, điều kiện, vòng lặp, chuỗi, list, dict, hàm, file, xử lý lỗi, lớp — và một dự án hoàn chỉnh.",
    stats=[("bài học", str(len(L))), ("chương trình mẫu", "14"), ("dự án", "1")],
    header_sub=f"Khóa học: 🐍 Python cơ bản cho học sinh · {len(L)} buổi",
    gradient=["#1e3a8a", "#2563eb", "#eab308"], storage="py", overview=OVERVIEW, groups=GROUPS, code_dir=CODE, runner=run,
)

if __name__ == "__main__":
    coursekit.build(COURSE, os.path.abspath(os.path.join(HERE, "..", "..", "training", "python-co-ban.html")))
