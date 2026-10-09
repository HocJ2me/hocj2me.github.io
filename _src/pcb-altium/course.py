# -*- coding: utf-8 -*-
"""Khóa Thiết kế mạch PCB với Altium Designer.  Build: python -X utf8 course.py"""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "common")]
import coursekit
from lessons import GROUPS, DRIVE

CODE = os.path.join(HERE, "code")
_runner = coursekit.Runner(os.path.join(HERE, "out", "run-cache.json"))


def run(path, stdin):
    def go():
        r = subprocess.run([sys.executable, "-I", "-X", "utf8", path], capture_output=True, cwd=tempfile.mkdtemp())
        if r.returncode:
            sys.exit(f"Lỗi khi chạy {path}:\n{r.stderr.decode('utf-8', 'replace')}")
        print("  chạy", os.path.basename(path))
        return r.stdout.decode("utf-8").replace("\r\n", "\n").rstrip()
    return f"python {os.path.basename(path)}", _runner.run([open(path, "rb").read()], go)


_all = [L for g in GROUPS for L in g[3]]
_idx = {L["id"]: i + 1 for i, L in enumerate(_all)}
_map = [
    ("Khóa basic", "Thiết kế logo", "logo"), ("", "Thiết kế mạch nguyên lý", "nguyen-ly"), ("", "Thiết kế mạch layout", "layout-2-lop"),
    ("", "Thực hành dự án PCB mẫu", "xuat-file-du-an"),
    ("Khóa Altium 4 lớp highspeed", "Thiết kế 4 lớp và highspeed", "4-lop"), ("", "Sử dụng Altium 18", "tong-quan"), ("", "Thiết kế chống nhiễu", "chong-nhieu"),
    ("", "Mạch điều khiển", "mach-dieu-khien"), ("", "Mạch đo dòng và đo áp", "do-dong-ap"),
    ("Khóa Altium thiết kế thư viện", "Sử dụng thư viện", "su-dung-thu-vien"), ("", "Thiết kế thư viện chân xuyên", "thu-vien-chan-xuyen"),
    ("", "Các thành phần và layer trên mạch PCB", "lop-pcb"), ("", "Sửa lỗi thắt cổ chai và layout đường ống nước", "that-co-chai"),
    ("", "Thiết kế IC chân dán", "thu-vien-chan-dan"), ("", "Tính toán thiết kế thư viện điện trở", "thu-vien-dien-tro"),
]
_title = {L["id"]: L["title"] for L in _all}
_rows = "".join(f'<tr><td>{a}</td><td>{b}</td><td><a href="#{c}">Bài {_idx[c]}: {_title[c]}</a></td></tr>' for a, b, c in _map)
_road = "".join(f'<div class="road"><div class="rb">Buổi {i + 1}</div><div><a href="#{L["id"]}">{L["title"]}</a><br><small>{L["time"]}</small></div></div>' for i, L in enumerate(_all))

OVERVIEW = f"""
<h3><span class="n">?</span>Khóa học này dành cho ai?</h3>
<div class="prose"><p>Học sinh, sinh viên đã làm dự án Arduino/ESP32 trên testboard và muốn biến nó thành <b>mạch in hoàn chỉnh</b>: gọn, chắc chắn, đem đi thi và trình diễn được — tiến tới thiết kế mạch 4 lớp, mạch điều khiển công suất và mạch đo lường như kỹ sư phần cứng.</p></div>
<div class="grid3">
<div class="card"><h5>📖 3 khóa con</h5><p>Basic → Thiết kế thư viện → Mạch 4 lớp &amp; highspeed, đúng như giáo trình.</p></div>
<div class="card"><h5>🖼️ Hình minh hoạ kỹ thuật</h5><p>Mặt cắt lớp mạch, via, pad, land pattern, đường hồi dòng, thắt cổ chai, Kelvin, cặp vi sai…</p></div>
<div class="card"><h5>🧮 Tính toán chạy thật</h5><p>6 script Python theo chuẩn IPC + 3 máy tính tương tác ngay trên trang.</p></div>
</div>
<h3><span class="n">📁</span>Tài liệu gốc (Google Drive)</h3>
<table class="tbl"><tr><th>Khóa</th><th>Tài liệu</th></tr>
<tr><td>Khóa basic</td><td><a href="{DRIVE['basic']}" target="_blank" rel="noopener">Thư mục tài liệu khóa basic</a></td></tr>
<tr><td>Khóa Altium 4 lớp highspeed</td><td><a href="{DRIVE['4lop']}" target="_blank" rel="noopener">Thư mục tài liệu 4 lớp &amp; highspeed</a></td></tr>
<tr><td>Khóa Altium thiết kế thư viện</td><td><a href="{DRIVE['thuvien']}" target="_blank" rel="noopener">Thư mục tài liệu thư viện</a></td></tr>
<tr><td>Thắt cổ chai &amp; đường ống nước</td><td><a href="{DRIVE['thatco']}" target="_blank" rel="noopener">Thư mục tài liệu bổ sung</a></td></tr></table>
<h3><span class="n">⚙</span>Chuẩn bị</h3>
<div class="prose"><ul><li><b>Altium Designer 18</b> trở lên (bản dùng thử 15 ngày, hoặc giấy phép giáo dục miễn phí cho học sinh/sinh viên). Có thể học song song bằng <b>KiCad</b> (miễn phí) — khái niệm giống hệt.</li>
<li>Python 3 để chạy các script tính toán (không bắt buộc — đã có sẵn kết quả và máy tính tương tác).</li>
<li>Datasheet của linh kiện dùng trong dự án; thước kẹp để đo linh kiện thật.</li></ul></div>
<h3><span class="n">≡</span>Đối chiếu với giáo trình</h3>
<table class="tbl"><tr><th>Khóa</th><th>Bài trong giáo trình</th><th>Học ở bài</th></tr>{_rows}</table>
<h3><span class="n">⌚</span>Lộ trình gợi ý — {len(_all)} buổi</h3>
<div class="roadmap">{_road}</div>
"""

COURSE = dict(
    slug="pcb-altium", title="Thiết kế mạch PCB với Altium Designer", short_title="Thiết kế mạch PCB", icon="🖥", lang="py",
    badge=f"{len(_all)} bài · 3 khóa con", tagline="Từ mạch nguyên lý, layout 2 lớp, thư viện linh kiện chuẩn IPC tới mạch 4 lớp, chống nhiễu, dòng lớn, mạch điều khiển và đo lường.",
    stats=[("bài học", str(len(_all))), ("khóa con", "3"), ("công cụ tính", "9")],
    header_sub=f"Khóa học: 🖥 Thiết kế mạch PCB với Altium Designer · Basic – Thư viện – 4 lớp &amp; highspeed · {len(_all)} buổi",
    gradient=["#14532d", "#15803d", "#0d9488"], storage="pcb", overview=OVERVIEW, groups=GROUPS, code_dir=CODE, runner=run,
)

if __name__ == "__main__":
    coursekit.build(COURSE, os.path.abspath(os.path.join(HERE, "..", "..", "training", "pcb-altium.html")))
