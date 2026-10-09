# -*- coding: utf-8 -*-
"""Sinh trang khóa học Design Pattern: training/design-pattern.html

Chạy:  python -X utf8 build.py [--out ĐƯỜNG_DẪN_HTML]
- Biên dịch & chạy từng ví dụ (C++ g++, Python, Java) để lấy kết quả thật (có cache theo nội dung file).
- Tô màu cú pháp, vẽ UML thành SVG và ghép vào template.
"""
import argparse, hashlib, json, os, subprocess, sys, tempfile
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from content_creational import PATTERNS as CRE
from content_structural import PATTERNS as STR
from content_behavioral import PATTERNS as BEH
from content_lang import LANG
from highlight import highlight
import uml, illus

GROUPS = [
    ("cre", "Nhóm Creational", "Khởi tạo đối tượng", CRE),
    ("str", "Nhóm Structural", "Cấu trúc, kết hợp đối tượng", STR),
    ("beh", "Nhóm Behavioral", "Hành vi, tương tác giữa đối tượng", BEH),
]
LANGS = [("cpp", "C++17", "cpp"), ("py", "Python 3", "python"), ("java", "Java 17+", "java")]
EXT = {"cpp": ".cpp", "py": ".py", "java": ".java"}

# ---------------------------------------------------------------- chạy ví dụ
CACHE_FILE = os.path.join(HERE, "out", "run-cache.json")


def run_example(lang, path):
    src = open(path, "rb").read()
    key = f"{lang}:{os.path.basename(path)}:{hashlib.sha1(src).hexdigest()}"
    cache = json.load(open(CACHE_FILE, encoding="utf-8")) if os.path.exists(CACHE_FILE) else {}
    if key in cache:
        return cache[key]
    tmp = tempfile.mkdtemp()
    if lang == "cpp":
        exe = os.path.join(tmp, "a.exe")
        c = subprocess.run(["g++", "-std=c++17", "-static", "-O1", "-Wall", "-Wextra", path, "-o", exe], capture_output=True)
        if c.returncode:
            sys.exit(f"Lỗi biên dịch {path}:\n{c.stderr.decode('utf-8', 'replace')}")
        r = subprocess.run([exe], capture_output=True, cwd=tmp)
    elif lang == "py":
        r = subprocess.run([sys.executable, "-I", "-X", "utf8", path], capture_output=True, cwd=tmp)
    else:
        r = subprocess.run(["java", "-Dstdout.encoding=UTF-8", "-Dfile.encoding=UTF-8", path], capture_output=True, cwd=tmp)
    if r.returncode:
        sys.exit(f"Lỗi khi chạy {path}:\n{r.stderr.decode('utf-8', 'replace')}")
    out = r.stdout.decode("utf-8").replace("\r\n", "\n").rstrip()
    cache[key] = out
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    json.dump(cache, open(CACHE_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("  chạy", lang, os.path.basename(path))
    return out


# ---------------------------------------------------------------- render 1 bài
def li(items):
    return "".join(f"<li>{x}</li>" for x in items)


def stars(n):
    return f'<span class="stars" title="Mức độ phổ biến {n}/5">{"★" * n}<span class="off">{"★" * (5 - n)}</span></span>'


def render_lesson(p, idx, total, gkey, gname, prev, nxt):
    base = p["code"].rsplit(".", 1)[0]
    L = LANG[p["id"]]
    notes = {"cpp": L["cpp"], "py": L["py"], "java": p["java_notes"]}
    run_cmd = {
        "cpp": f"g++ -std=c++17 {base}.cpp -o app && ./app",
        "py": f"python {base}.py",
        "java": f"java {base}.java",
    }
    tabs, panes = [], []
    for i, (lk, lname, folder) in enumerate(LANGS):
        path = os.path.join(HERE, folder, base + EXT[lk])
        code = open(path, encoding="utf-8").read().rstrip() + "\n"
        output = run_example(lk, path)
        lines = code.count("\n")
        tabs.append(f'<button class="ltab" role="tab" data-lang="{lk}">{lname}</button>')
        panes.append(f'''
<div class="lpane" data-lang="{lk}">
  <div class="codebox">
    <div class="codebar"><span class="fname">{base}{EXT[lk]}</span><span class="lines">{lines} dòng</span>
      <button class="cbtn" data-act="copy">Sao chép</button><button class="cbtn" data-act="dl" data-name="{base}{EXT[lk]}">Tải file</button></div>
    <pre class="code"><code>{highlight(code, lk)}</code></pre>
  </div>
  <div class="runcmd"><span>▶ Chạy thử:</span> <code>{escape(run_cmd[lk])}</code></div>
  <div class="outbox"><div class="outbar">Kết quả khi chạy (đã chạy thật lúc soạn bài)</div><pre class="out">{escape(output)}</pre></div>
  <h4 class="sub">Giải thích code {lname}</h4>
  <ul class="notes">{li(notes[lk])}</ul>
</div>''')

    parts = "".join(f"<tr><td><b>{escape(n)}</b></td><td>{escape(r)}</td></tr>" for n, r in p["participants"])
    fig = uml.render(p["uml"], p["name"])
    cap = p["uml"].get("caption", "")
    extra = ""
    if p.get("extra"):
        extra = f'<figure class="fig">{illus.EXTRA[p["extra"]]()}<figcaption>{illus.EXTRA_CAPTION[p["extra"]]}</figcaption></figure>'
    nav_prev = f'<a class="pn" href="#{prev[0]}">← {escape(prev[1])}</a>' if prev else "<span></span>"
    nav_next = f'<a class="pn next" href="#{nxt[0]}">{escape(nxt[1])} →</a>' if nxt else "<span></span>"
    emoji, analogy = p["analogy"]
    real_cols = (f'<div><h5>C++ / nhúng</h5><ul>{li(L["cpp_real"])}</ul></div>'
                 f'<div><h5>Python</h5><ul>{li(L["py_real"])}</ul></div>'
                 f'<div><h5>Java</h5><ul>{li(p["realworld"])}</ul></div>')
    ex = "".join(f'<li><label><input type="checkbox" data-ex="{p["id"]}-{k}"> <span>{e}</span></label></li>' for k, e in enumerate(p["exercises"]))
    return f'''
<section class="lesson" id="{p["id"]}" data-title="{escape(p["name"])}" hidden>
  <div class="hero hero-{gkey}">
    <div class="crumbs"><span class="gchip g-{gkey}">{gname}</span><span>Bài {idx}/{total}</span>{stars(p["freq"])}</div>
    <h2><span class="hicon">{p["icon"]}</span> {escape(p["name"])} <small>— {escape(p["vn"])}</small></h2>
    <p class="intent"><b>Mục đích:</b> {p["intent"]}</p>
  </div>

  <div class="analogy"><div class="aemoji">{emoji}</div><div><b>Ví dụ đời thường.</b> {analogy}</div></div>

  <h3><span class="n">1</span>Vấn đề cần giải quyết</h3>
  <div class="prose">{p["problem"]}</div>

  <h3><span class="n">2</span>Giải pháp</h3>
  <div class="prose">{p["solution"]}</div>

  <h3><span class="n">3</span>Sơ đồ lớp UML</h3>
  <figure class="fig">{fig}<figcaption>Sơ đồ lớp của ví dụ.{(" " + escape(cap)) if cap else ""} Tên phương thức theo kiểu C++/Java; bản Python dùng <code>snake_case</code>. <a href="#overview" data-goto="legend">Xem bảng ký hiệu UML</a></figcaption></figure>
  {extra}

  <h3><span class="n">4</span>Các thành phần tham gia</h3>
  <table class="tbl parts"><tr><th>Thành phần</th><th>Vai trò</th></tr>{parts}</table>

  <h3><span class="n">5</span>Code ví dụ chi tiết</h3>
  <p class="hint">Cùng một kịch bản, cùng tên lớp, viết bằng 3 ngôn ngữ — chọn tab để so sánh. C++ là ngôn ngữ chính của khóa (gần với lập trình nhúng nhất).</p>
  <div class="ltabs" role="tablist">{"".join(tabs)}</div>
  {"".join(panes)}

  <h3><span class="n">6</span>Áp dụng trong lập trình nhúng</h3>
  <div class="emb"><div class="embicon">🔧</div><ul>{li(L["emb"])}</ul></div>

  <h3><span class="n">7</span>Ưu điểm và nhược điểm</h3>
  <div class="pc"><div class="pros"><h5>✔ Ưu điểm</h5><ul>{li(p["pros"])}</ul></div><div class="cons"><h5>✘ Nhược điểm</h5><ul>{li(p["cons"])}</ul></div></div>

  <h3><span class="n">8</span>Khi nào nên dùng</h3>
  <ul class="when">{li(p["when"])}</ul>

  <h3><span class="n">9</span>Gặp ở đâu trong thực tế</h3>
  <div class="real">{real_cols}</div>

  <h3><span class="n">10</span>Liên hệ với các mẫu khác</h3>
  <p class="prose">{p["related"]}</p>

  <h3><span class="n">11</span>Bài tập thực hành</h3>
  <ol class="ex">{ex}</ol>

  <div class="refs">📚 Đọc thêm: <a href="{p["ref"]}" target="_blank" rel="noopener">Hướng dẫn {escape(p["name"])} (gpcoder.com)</a> ·
    {"" if p["id"] in ("object-pool", "interpreter") else f'<a href="https://refactoring.guru/vi/design-patterns/{p["id"]}" target="_blank" rel="noopener">refactoring.guru (minh hoạ)</a> ·'}
    <a href="https://viblo.asia/p/tong-hop-cac-bai-huong-dan-ve-design-pattern-23-mau-co-ban-cua-gof-3P0lPQPG5ox" target="_blank" rel="noopener">Tổng hợp 23 mẫu GoF (Viblo)</a></div>

  <div class="donebar"><button class="donebtn" data-done="{p["id"]}">☐ Đánh dấu đã học xong bài này</button></div>
  <nav class="pnav">{nav_prev}{nav_next}</nav>
</section>'''


# ---------------------------------------------------------------- trang tổng quan
SCHEDULE = [
    ("1", "Khởi động", "Design Pattern là gì · UML · SOLID · ôn OOP trong C++ (virtual, con trỏ thông minh)", []),
    ("2", "Creational", "", ["singleton", "factory-method"]),
    ("3", "Creational", "", ["abstract-factory", "builder"]),
    ("4", "Creational", "Không cấp phát động trong firmware", ["prototype", "object-pool"]),
    ("5", "Structural", "Bọc thư viện cảm biến, tách driver", ["adapter", "bridge"]),
    ("6", "Structural", "Menu LCD nhiều cấp, bộ lọc tín hiệu", ["composite", "decorator"]),
    ("7", "Structural", "", ["facade", "flyweight", "proxy"]),
    ("8", "Behavioral", "Xử lý lệnh UART/Bluetooth", ["chain-of-responsibility", "command"]),
    ("9", "Behavioral", "", ["interpreter", "iterator", "mediator"]),
    ("10", "Behavioral", "Lưu cấu hình EEPROM, sự kiện cảm biến", ["memento", "observer"]),
    ("11", "Behavioral", "Máy trạng thái robot, thuật toán điều khiển", ["state", "strategy"]),
    ("12", "Tổng kết", "Dự án: firmware trạm thời tiết ESP32 kết hợp Singleton + Observer + State + Strategy + Command", ["template-method", "visitor"]),
]


def render_overview(allp, names):
    rows = []
    for gkey, gname, gsub, plist in GROUPS:
        for p in plist:
            rows.append(f'<tr><td>{allp.index(p) + 1}</td><td><a href="#{p["id"]}">{p["icon"]} {escape(p["name"])}</a></td>'
                        f'<td>{escape(p["vn"])}</td><td><span class="gchip g-{gkey}">{gname.replace("Nhóm ", "")}</span></td><td>{stars(p["freq"])}</td></tr>')
    sched = []
    for b, kind, note, ids in SCHEDULE:
        links = " · ".join(f'<a href="#{i}">{escape(names[i])}</a>' for i in ids)
        sched.append(f'<div class="road"><div class="rb">Buổi {b}</div><div><b>{kind}</b> {links}'
                     f'{("<br><small>" + escape(note) + "</small>") if note else ""}</div></div>')
    gm = illus.groups_map([(k, n, s, [(p["id"], f'{allp.index(p) + 1}. {p["name"]}') for p in pl]) for k, n, s, pl in GROUPS])
    return f'''
<section class="lesson" id="overview" data-title="Tổng quan" hidden>
  <div class="hero hero-ov">
    <div class="crumbs"><span class="gchip">Bài mở đầu</span><span>24 mẫu · 3 ngôn ngữ · 12 buổi</span></div>
    <h2>🧩 Design Pattern — Mẫu thiết kế phần mềm</h2>
    <p class="intent">Khóa học tổng hợp <b>23 mẫu kinh điển của GoF</b> và mẫu <b>Object Pool</b>. Mỗi bài có lý thuyết đầy đủ, sơ đồ UML minh hoạ, và code ví dụ chạy được bằng <b>C++</b> (ngôn ngữ chính, định hướng lập trình nhúng), <b>Python</b> và <b>Java</b>.</p>
    <div class="ovstats"><div><b>24</b><span>mẫu thiết kế</span></div><div><b>72</b><span>chương trình mẫu</span></div><div><b>3</b><span>ngôn ngữ</span></div><div><b id="ovDone">0</b><span>bài đã học</span></div></div>
    <a class="startbtn" href="#singleton">Bắt đầu bài 1: Singleton →</a>
  </div>

  <h3><span class="n">?</span>Design Pattern là gì?</h3>
  <div class="prose">
    <p><b>Design Pattern (mẫu thiết kế)</b> là những <b>giải pháp đã được kiểm chứng</b> cho các vấn đề lặp đi lặp lại trong thiết kế phần mềm hướng đối tượng. Nó không phải một đoạn code để chép, mà là một <b>“bản thiết kế” tổng quát</b> — bạn hiểu ý tưởng rồi áp dụng vào bài toán của mình, bằng ngôn ngữ của mình.</p>
    <p>Năm 1994, bốn tác giả Erich Gamma, Richard Helm, Ralph Johnson và John Vlissides — thường gọi là <b>“Gang of Four” (GoF)</b> — xuất bản cuốn <i>Design Patterns: Elements of Reusable Object-Oriented Software</i>, mô tả 23 mẫu, chia thành 3 nhóm.</p>
    <p>Mỗi mẫu thường được mô tả bằng 4 yếu tố: <b>tên</b> · <b>vấn đề</b> (khi nào dùng) · <b>giải pháp</b> (các thành phần và quan hệ) · <b>hệ quả</b> (ưu nhược điểm). Các bài trong khóa đều theo đúng cấu trúc này.</p>
  </div>
  <div class="pc3">
    <div><h5>🗣️ Ngôn ngữ chung</h5><p>Nói “dùng Observer cho cảm biến” là cả nhóm hiểu ngay thiết kế, không cần giải thích dài.</p></div>
    <div><h5>🧱 Code dễ mở rộng</h5><p>Thêm cảm biến, thêm chế độ, đổi phần cứng mà không phải sửa lại code cũ đang chạy ổn.</p></div>
    <div><h5>🎓 Đọc hiểu thư viện</h5><p>Arduino, ESP-IDF, Qt, STL, Python stdlib… đều dùng các mẫu này. Biết mẫu là đọc code nhanh hơn nhiều.</p></div>
  </div>

  <h3><span class="n">▦</span>Ba nhóm mẫu thiết kế</h3>
  <figure class="fig">{gm}<figcaption>Bấm vào tên mẫu để mở bài học.</figcaption></figure>
  <table class="tbl">
    <tr><th>Nhóm</th><th>Trả lời câu hỏi</th><th>Ví dụ trong nhúng</th></tr>
    <tr><td><span class="gchip g-cre">Creational</span></td><td>Tạo đối tượng <b>như thế nào</b> cho linh hoạt, che giấu lớp cụ thể?</td><td>Một driver UART duy nhất (Singleton), pool buffer tĩnh (Object Pool)</td></tr>
    <tr><td><span class="gchip g-str">Structural</span></td><td>Ghép các lớp/đối tượng thành cấu trúc lớn hơn <b>ra sao</b>?</td><td>Bọc thư viện cảm biến (Adapter), tách logic và driver màn hình (Bridge)</td></tr>
    <tr><td><span class="gchip g-beh">Behavioral</span></td><td>Các đối tượng <b>giao tiếp và phân chia trách nhiệm</b> thế nào?</td><td>Máy trạng thái robot (State), sự kiện cảm biến (Observer), hàng đợi lệnh (Command)</td></tr>
  </table>

  <h3 id="legend"><span class="n">⇢</span>Cách đọc sơ đồ lớp UML</h3>
  <div class="prose"><p>Mỗi bài đều có <b>sơ đồ lớp UML</b>. Một ô chữ nhật là một lớp: phần trên là tên (kèm <code>«interface»</code> hoặc <code>«abstract»</code> nếu có), phần giữa là thuộc tính, phần dưới là phương thức. Các đường nối thể hiện quan hệ:</p></div>
  <figure class="fig">{illus.uml_legend()}</figure>

  <h3><span class="n">S</span>Năm nguyên lý SOLID — nền tảng của mọi mẫu</h3>
  <table class="tbl">
    <tr><th></th><th>Nguyên lý</th><th>Ý nghĩa ngắn gọn</th><th>Ví dụ nhúng</th></tr>
    <tr><td><b>S</b></td><td>Single Responsibility</td><td>Mỗi lớp chỉ có một lý do để thay đổi.</td><td>Lớp đọc cảm biến không lo việc gửi MQTT.</td></tr>
    <tr><td><b>O</b></td><td>Open/Closed</td><td>Mở để mở rộng, đóng để sửa đổi.</td><td>Thêm loại cảm biến mới mà không sửa vòng <code>loop()</code>.</td></tr>
    <tr><td><b>L</b></td><td>Liskov Substitution</td><td>Lớp con thay được lớp cha mà chương trình vẫn đúng.</td><td>Mọi <code>ISensor</code> đều trả về đơn vị °C như hợp đồng.</td></tr>
    <tr><td><b>I</b></td><td>Interface Segregation</td><td>Nhiều interface nhỏ tốt hơn một interface “to đùng”.</td><td>Tách <code>IReadable</code> và <code>ICalibratable</code>.</td></tr>
    <tr><td><b>D</b></td><td>Dependency Inversion</td><td>Phụ thuộc vào trừu tượng, không phụ thuộc vào cụ thể.</td><td>Logic robot phụ thuộc <code>IMotor</code>, không phụ thuộc <code>L298N</code>.</td></tr>
  </table>

  <h3><span class="n">C</span>Vì sao học bằng C++ — và lưu ý khi dùng trong nhúng</h3>
  <div class="prose">
    <p>Firmware cho Arduino, ESP32, STM32 phần lớn được viết bằng <b>C/C++</b>. C++ cho phép dùng các mẫu hướng đối tượng mà vẫn kiểm soát chặt bộ nhớ và hiệu năng. Python (và MicroPython) giúp thử ý tưởng nhanh, viết công cụ trên PC; Java giúp đối chiếu với phần lớn tài liệu Design Pattern trên mạng.</p>
  </div>
  <div class="emb"><div class="embicon">⚠️</div><ul>
    <li><b>Hạn chế cấp phát động lúc chạy</b> (<code>new</code>, <code>malloc</code>, <code>std::vector</code> tăng kích thước): heap nhỏ dễ phân mảnh. Ưu tiên đối tượng tĩnh, <code>std::array</code>, Object Pool.</li>
    <li><b>Hàm ảo</b> tốn thêm một con trỏ <i>vtable</i> mỗi đối tượng và một lần gọi gián tiếp — thường chấp nhận được; khi cần tối ưu tuyệt đối, dùng <b>template</b> để chọn lúc biên dịch (xem bài Strategy, Visitor).</li>
    <li>Nhiều trình biên dịch nhúng tắt <b>exception</b> và <b>RTTI</b> (<code>-fno-exceptions -fno-rtti</code>) → trả lỗi bằng <code>bool</code>/<code>std::optional</code>, tránh <code>dynamic_cast</code>.</li>
    <li>Arduino AVR (Uno, Nano) <b>không có STL</b> đầy đủ; ESP32 và STM32 (GCC) hỗ trợ C++17 tốt. Các ví dụ dùng <code>std::cout</code> để chạy trên PC — trên board hãy thay bằng <code>Serial.println()</code>.</li>
    <li>Luôn khai báo <code>virtual ~Base() = default;</code> cho lớp cơ sở có hàm ảo; ưu tiên <code>std::unique_ptr</code> thay cho con trỏ thô sở hữu.</li>
  </ul></div>

  <h3><span class="n">⚙</span>Chuẩn bị môi trường thực hành</h3>
  <table class="tbl">
    <tr><th>Ngôn ngữ</th><th>Cài đặt</th><th>Chạy một ví dụ</th></tr>
    <tr><td><b>C++17</b></td><td>Windows: MinGW-w64 / MSYS2 (g++) hoặc Visual Studio; macOS/Linux: g++ hoặc clang++</td><td><code>g++ -std=c++17 01-singleton.cpp -o app &amp;&amp; ./app</code></td></tr>
    <tr><td><b>Python 3.10+</b></td><td>python.org (tick “Add to PATH”)</td><td><code>python 01-singleton.py</code></td></tr>
    <tr><td><b>Java 17+</b></td><td>Eclipse Temurin / Oracle JDK</td><td><code>java 01-singleton.java</code> (chạy thẳng file nguồn)</td></tr>
  </table>
  <p class="hint">Không muốn cài gì? Dán code vào <a href="https://godbolt.org" target="_blank" rel="noopener">godbolt.org</a> (C++), <a href="https://www.online-python.com" target="_blank" rel="noopener">online-python.com</a> hoặc <a href="https://www.jdoodle.com" target="_blank" rel="noopener">jdoodle.com</a>. Trên Windows, nếu chữ tiếng Việt bị lỗi trong cửa sổ dòng lệnh, chạy <code>chcp 65001</code> trước.</p>

  <h3><span class="n">⌚</span>Lộ trình gợi ý — 12 buổi × 2 giờ</h3>
  <div class="roadmap">{"".join(sched)}</div>

  <h3><span class="n">≡</span>Danh sách 24 mẫu</h3>
  <table class="tbl list"><tr><th>#</th><th>Mẫu</th><th>Tên tiếng Việt</th><th>Nhóm</th><th>Độ phổ biến</th></tr>{"".join(rows)}</table>

  <nav class="pnav"><span></span><a class="pn next" href="#singleton">Singleton →</a></nav>
</section>'''


# ---------------------------------------------------------------- ghép trang
def build(out_path):
    allp = [p for _, _, _, pl in GROUPS for p in pl]
    names = {p["id"]: p["name"] for p in allp}
    order = [("overview", "Tổng quan")] + [(p["id"], p["name"]) for p in allp]
    lessons = [render_overview(allp, names)]
    side = ['<a class="sitem" href="#overview" data-id="overview"><span class="sn">★</span>Tổng quan &amp; lộ trình</a>']
    for gkey, gname, gsub, plist in GROUPS:
        side.append(f'<div class="sgroup g-{gkey}">{gname}<small>{gsub}</small></div>')
        for p in plist:
            i = allp.index(p) + 1
            k = order.index((p["id"], p["name"]))
            lessons.append(render_lesson(p, i, len(allp), gkey, gname, order[k - 1], order[k + 1] if k + 1 < len(order) else None))
            side.append(f'<a class="sitem" href="#{p["id"]}" data-id="{p["id"]}"><span class="sn">{i}</span>{escape(p["name"])}<span class="tick">✓</span></a>')

    tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    html = (tpl.replace("{{SIDEBAR}}", "\n".join(side))
               .replace("{{LESSONS}}", "\n".join(lessons))
               .replace("{{TOTAL}}", str(len(allp)))
               .replace("{{ORDER}}", json.dumps([o[0] for o in order])))
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"Đã ghi {out_path} ({len(html) // 1024} KB)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "..", "..", "training", "design-pattern.html"))
    build(os.path.abspath(ap.parse_args().out))
