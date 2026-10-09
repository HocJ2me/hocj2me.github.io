# -*- coding: utf-8 -*-
"""Khóa C++ cơ bản → nâng cao (hướng lập trình nhúng).  Build: python -X utf8 course.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "common")]
import coursekit
from lessons_a import LESSONS
from lessons_b import LESSONS_OOP, LESSONS_ADV, LESSONS_PRACTICE

CODE = os.path.join(HERE, "code")
_runner = coursekit.Runner(os.path.join(HERE, "out", "run-cache.json"))


def run(path, stdin):
    name = os.path.basename(path)
    out = coursekit.run_cpp(path, stdin, runner=_runner)
    return f"g++ -std=c++17 {name} -o app && ./app", out


GROUPS = [
    ("nen-tang", "Nền tảng", "Cú pháp, kiểu dữ liệu, điều khiển, hàm, mảng", LESSONS[:6]),
    ("con-tro", "Con trỏ & bộ nhớ", "Địa chỉ, con trỏ, tham chiếu, struct", LESSONS[6:]),
    ("oop", "Hướng đối tượng", "Lớp, kế thừa, đa hình, trừu tượng", LESSONS_OOP),
    ("nang-cao", "C++ nâng cao", "File, ngoại lệ, bộ nhớ, template, đa luồng, STL", LESSONS_ADV),
    ("luyen-tap", "Luyện tập", "12 bài tập có lời giải", LESSONS_PRACTICE),
]

_all = [L for g in GROUPS for L in g[3]]
_map = [  # chủ đề trong file Excel -> bài
    ("1–3", "Cơ bản về C++, giới thiệu, cài đặt, build, cú pháp, comment", "gioi-thieu"),
    ("4–8", "Kiểu dữ liệu, các kiểu biến, phạm vi biến, hằng, modifier", "kieu-du-lieu"),
    ("9–10", "Lớp lưu trữ, toán tử", "toan-tu"),
    ("11–12", "Vòng lặp, if/else/switch", "dieu-khien"),
    ("13–14", "Hàm, Number", "ham"),
    ("15–16", "Mảng, chuỗi", "mang-chuoi"),
    ("17", "Con trỏ: con trỏ với địa chỉ, địa chỉ vs con trỏ, con trỏ với con trỏ", "con-tro"),
    ("18–19", "Con trỏ: ép kiểu con trỏ (int ↔ char…), con trỏ hàm", "con-tro-2"),
    ("20–23", "Tham chiếu, Date &amp; Time, Input/Output, Struct", "tham-chieu-struct"),
    ("24–25, 30", "Hướng đối tượng, lớp &amp; đối tượng, tính bao đóng", "lop-doi-tuong"),
    ("26–27", "Tính kế thừa, nạp chồng", "ke-thua"),
    ("28–29, 31", "Đa hình, trừu tượng, interface", "da-hinh"),
    ("32–35", "Con trỏ lớp: Singleton, thay đổi đối tượng, Adapter, Abstract", "con-tro-lop"),
    ("36–39", "C++ nâng cao: File I/O &amp; stream, xử lý ngoại lệ, bộ nhớ động", "file-ngoai-le-bo-nho"),
    ("40–43", "Namespace, template, preprocessor, xử lý tín hiệu", "namespace-template"),
    ("44–49", "Đa luồng, lập trình web, STL, thư viện chuẩn, tài liệu tham khảo", "da-luong-stl"),
    ("50", "12 bài tập C phổ biến", "bai-tap"),
]
_title = {L["id"]: L["title"] for L in _all}
_rows = "".join(f'<tr><td>{a}</td><td>{b}</td><td><a href="#{c}">Bài {[L["id"] for L in _all].index(c) + 1}: {_title[c]}</a></td></tr>' for a, b, c in _map)
_road = "".join(f'<div class="road"><div class="rb">Buổi {i + 1}</div><div><a href="#{L["id"]}">{L["title"]}</a><br><small>{L["goal"][:110]}{"…" if len(L["goal"]) > 110 else ""}</small></div></div>' for i, L in enumerate(_all))

OVERVIEW = f"""
<h3><span class="n">?</span>Khóa học này dành cho ai?</h3>
<div class="prose">
<p>Học sinh, sinh viên muốn học <b>C++ bài bản từ con số 0</b> để lập trình <b>vi điều khiển</b> (Arduino, ESP32, STM32), robot, IoT — hoặc làm nền tảng cho thi Tin học, Khoa học kỹ thuật. Không cần biết lập trình trước.</p>
<p>Khác với các khóa C++ thông thường, mọi ví dụ đều gắn với phần cứng: đọc cảm biến, điều khiển LED, động cơ, phân tích lệnh UART, thao tác thanh ghi, lọc nhiễu, đóng gói dữ liệu truyền thông.</p>
</div>
<div class="grid3">
<div class="card"><h5>📖 Lý thuyết đầy đủ</h5><p>Mỗi bài có mục tiêu, giải thích, bảng so sánh, lỗi thường gặp và tóm tắt.</p></div>
<div class="card"><h5>🖼️ Hình minh hoạ</h5><p>Bộ nhớ, con trỏ, thanh ghi, endian, vtable, data race… được vẽ trực quan.</p></div>
<div class="card"><h5>▶ Code chạy thật</h5><p>45 chương trình hoàn chỉnh, kèm kết quả chạy thật — tải về chạy ngay được.</p></div>
</div>
<h3><span class="n">⚙</span>Chuẩn bị</h3>
<div class="prose"><ul>
<li>Máy tính cài <b>g++</b> (MinGW-w64/MSYS2 trên Windows, sẵn trên Linux/macOS) và <b>VS Code</b>. Xem chi tiết ở Bài 1.</li>
<li>Chạy một ví dụ: <code>g++ -std=c++17 01-hello.cpp -o app &amp;&amp; ./app</code> (Windows: <code>app.exe</code>). Chữ tiếng Việt lỗi trong cửa sổ lệnh Windows: chạy <code>chcp 65001</code> trước.</li>
<li>Không có máy? Dán code vào <a href="https://godbolt.org" target="_blank" rel="noopener">godbolt.org</a> hoặc <a href="https://www.onlinegdb.com" target="_blank" rel="noopener">onlinegdb.com</a>.</li>
<li>Các ví dụ in bằng <code>std::cout</code> để chạy trên máy tính; khi đưa lên board, thay bằng <code>Serial.print()</code>.</li>
</ul></div>
<h3><span class="n">≡</span>Đối chiếu với giáo trình (50 chủ đề)</h3>
<table class="tbl"><tr><th>STT</th><th>Chủ đề trong giáo trình</th><th>Học ở bài</th></tr>{_rows}</table>
<h3><span class="n">⌚</span>Lộ trình gợi ý — {len(_all)} buổi × 2 giờ</h3>
<div class="roadmap">{_road}</div>
<h3><span class="n">→</span>Học tiếp</h3>
<div class="grid2">
<div class="card"><h5><a href="freertos.html">⏱ FreeRTOS cho lập trình nhúng</a></h5><p>Đa nhiệm thời gian thực trên ESP32/STM32: task, queue, semaphore, mutex, timer.</p></div>
<div class="card"><h5><a href="design-pattern.html">🧩 Design Pattern</a></h5><p>24 mẫu thiết kế với C++ hướng nhúng — tổ chức firmware lớn cho gọn và dễ mở rộng.</p></div>
</div>
"""

COURSE = dict(
    slug="cpp-co-ban", title="Lập trình C++ cơ bản → nâng cao (hướng nhúng)", short_title="C++ cơ bản → nâng cao", icon="💻",
    badge=f"{len(_all)} bài · 45 chương trình", tagline="Từ biến, vòng lặp tới con trỏ, hướng đối tượng, template, đa luồng — học C++ để lập trình vi điều khiển, robot và IoT.",
    stats=[("bài học", str(len(_all))), ("chương trình mẫu", "45"), ("chủ đề giáo trình", "50")],
    header_sub="Khóa học: 💻 Lập trình C++ cơ bản → nâng cao, hướng lập trình nhúng · 17 buổi × 2 giờ",
    gradient=["#0f766e", "#0891b2", "#2563eb"], storage="cpp", overview=OVERVIEW, groups=GROUPS, code_dir=CODE, runner=run,
)

if __name__ == "__main__":
    out = os.path.join(HERE, "..", "..", "training", "cpp-co-ban.html")
    coursekit.build(COURSE, os.path.abspath(out))
