# -*- coding: utf-8 -*-
"""Khóa FreeRTOS cho lập trình nhúng.  Build: python -X utf8 course.py
Ví dụ chạy trên FreeRTOS-Kernel V11.1.0 (thư mục kernel/, giấy phép MIT) với port mô phỏng MSVC-MingW."""
import glob, hashlib, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "common")]
import coursekit
from lessons import GROUPS

CODE = os.path.join(HERE, "code")
K = os.path.join(HERE, "kernel")
SIM = os.path.join(HERE, "sim")
LIB = os.path.join(HERE, "out", "libfreertos.a")
INC = [SIM, os.path.join(K, "include"), os.path.join(K, "portable", "MSVC-MingW")]
_runner = coursekit.Runner(os.path.join(HERE, "out", "run-cache.json"))


def build_lib():
    srcs = [os.path.join(K, f) for f in ("tasks.c", "queue.c", "list.c", "timers.c", "event_groups.c", "stream_buffer.c")]
    srcs += [os.path.join(K, "portable", "MSVC-MingW", "port.c"), os.path.join(K, "portable", "MemMang", "heap_4.c"),
             os.path.join(SIM, "hook_idle.c"), os.path.join(SIM, "hook_misc.c")]
    objdir = os.path.join(HERE, "out", "obj")
    os.makedirs(objdir, exist_ok=True)
    objs = []
    for s in srcs:
        o = os.path.join(objdir, os.path.basename(s)[:-2] + ".o")
        subprocess.run(["gcc", "-O1", "-w", *[f"-I{i}" for i in INC], "-c", s, "-o", o], check=True)
        objs.append(o)
    if os.path.exists(LIB):
        os.remove(LIB)
    subprocess.run(["ar", "rcs", LIB, *objs], check=True)
    print("  đã build libfreertos.a")


def _ver():
    h = hashlib.sha1()
    for f in sorted(glob.glob(os.path.join(SIM, "*"))):
        h.update(open(f, "rb").read())
    return h.hexdigest()[:10]


def run(path, stdin):
    name = os.path.basename(path)
    src = open(path, encoding="utf-8").read()
    if '"sim.h"' not in src:                       # ví dụ C++ thuần (không FreeRTOS)
        return f"g++ -std=c++17 {name} -o app && ./app", coursekit.run_cpp(path, stdin, runner=_runner)
    if not os.path.exists(LIB):
        build_lib()
    out = coursekit.run_cpp(path, stdin, sources=(LIB, "-lwinmm"), flags=(f"-DSIM_VER_{_ver()}",), include=INC, runner=_runner)
    return f"g++ -std=c++17 -Isim -Ikernel/include -Ikernel/portable/MSVC-MingW {name} libfreertos.a -lwinmm -o app && ./app", out


_all = [L for g in GROUPS for L in g[3]]
_idx = {L["id"]: i + 1 for i, L in enumerate(_all)}
_map = [
    ("1–12", "Getting Started, Kernel Overview, Supported Devices, Multitasking/Scheduling Basics, Context Switching, Real Time Applications/Scheduling, Implementation, Building Blocks, Detailed Example, Source Code Organization", "gioi-thieu, lap-lich"),
    ("13–17", "Task States, Task Priorities, Implementing a Task, Idle Task and Idle Hook", "task, lap-lich, idle-tien-ich"),
    ("18–24", "Co-Routines (status, implementing, priorities, scheduling, limitations)", "nang-cao-du-an"),
    ("25–26, 51", "Queues", "queue"),
    ("27–28", "Binary Semaphores, Counting Semaphores", "semaphore"),
    ("29–30, 55", "Mutexes, Recursive Mutexes, Semaphore/Mutex API", "mutex"),
    ("31–36, 50", "Direct To Task Notifications (as binary/counting semaphore, event group, mailbox)", "notification"),
    ("37–39, 53–54", "Stream &amp; Message Buffers (ISR → task, core → core)", "stream-message"),
    ("40–45, 56", "Software Timers (daemon task, configuration, one-shot vs auto-reload, resetting)", "software-timer"),
    ("46–49", "Task Creation, Task Control, Task Utilities, RTOS Kernel Control", "task, lap-lich, idle-tien-ich"),
    ("52", "Queue Sets", "nang-cao-du-an"),
    ("57", "Event Groups (flags)", "event-group"),
    ("58–62", "FreeRTOS-MPU, Co-routines API, Quality Management, Coding/Testing/Style Guide", "nang-cao-du-an"),
]
_title = {L["id"]: L["title"] for L in _all}
_rows = "".join(f'<tr><td>{a}</td><td>{b}</td><td>' + "<br>".join(f'<a href="#{c.strip()}">Bài {_idx[c.strip()]}: {_title[c.strip()]}</a>' for c in cs.split(",")) + "</td></tr>" for a, b, cs in _map)
_road = "".join(f'<div class="road"><div class="rb">Buổi {i + 1}</div><div><a href="#{L["id"]}">{L["title"]}</a><br><small>{L["time"]}</small></div></div>' for i, L in enumerate(_all))

OVERVIEW = f"""
<h3><span class="n">?</span>Khóa học này dành cho ai?</h3>
<div class="prose"><p>Học sinh, sinh viên đã biết C/C++ cơ bản (xem khóa <a href="cpp-co-ban.html">C++ cơ bản → nâng cao</a>) và đã làm vài dự án Arduino, muốn viết firmware <b>đa nhiệm, phản hồi đúng hạn</b> cho ESP32, STM32: robot, trạm quan trắc, thiết bị IoT, dự án thi Khoa học kỹ thuật.</p></div>
<div class="grid3">
<div class="card"><h5>📖 Lý thuyết theo tài liệu chính thức</h5><p>Bám theo 62 mục của trang freertos.org, giải thích bằng tiếng Việt kèm ví dụ phần cứng.</p></div>
<div class="card"><h5>📊 Biểu đồ thời gian</h5><p>Sơ đồ trạng thái, biểu đồ Gantt lập lịch, đảo ưu tiên, ISR → task… vẽ trực quan.</p></div>
<div class="card"><h5>▶ 23 ví dụ chạy thật</h5><p>Chạy trên FreeRTOS thật (bản mô phỏng trên PC), in mốc thời gian từng ms — kết quả có thể kiểm chứng.</p></div>
</div>
<h3><span class="n">⚙</span>Chạy ví dụ trên máy tính và trên board</h3>
<div class="prose"><ul>
<li><b>Trên PC (Windows)</b>: tải <a href="https://github.com/FreeRTOS/FreeRTOS-Kernel" target="_blank" rel="noopener">FreeRTOS-Kernel</a>, dùng port <code>portable/MSVC-MingW</code> + <code>heap_4.c</code>, file cấu hình và <code>sim.h</code> như trong khóa; biên dịch bằng MinGW g++. Linux/macOS dùng port <code>ThirdParty/GCC/Posix</code>.</li>
<li><b>Trên ESP32 (Arduino IDE)</b>: chép thân các hàm task, bỏ <code>vTaskStartScheduler()</code> (đã chạy sẵn), tạo task trong <code>setup()</code>, thay <code>LOG(...)</code> bằng <code>Serial.printf(...)</code>, thay ngắt giả lập bằng <code>attachInterrupt</code>. Lưu ý: ESP32 tính stack bằng <b>byte</b>.</li>
<li><b>Trên STM32</b>: STM32CubeIDE → bật FREERTOS (CMSIS v2), có thể gọi trực tiếp API gốc <code>xTaskCreate</code>…</li>
</ul></div>
<h3><span class="n">≡</span>Đối chiếu với giáo trình (62 mục)</h3>
<table class="tbl"><tr><th>STT</th><th>Chủ đề trong giáo trình</th><th>Học ở bài</th></tr>{_rows}</table>
<h3><span class="n">⌚</span>Lộ trình gợi ý — {len(_all)} buổi</h3>
<div class="roadmap">{_road}</div>
<h3><span class="n">→</span>Khóa liên quan</h3>
<div class="grid2">
<div class="card"><h5><a href="cpp-co-ban.html">💻 C++ cơ bản → nâng cao</a></h5><p>Nền tảng ngôn ngữ: con trỏ, struct, hàm callback, đa luồng.</p></div>
<div class="card"><h5><a href="design-pattern.html">🧩 Design Pattern</a></h5><p>Observer, State, Command, Object Pool… — rất hợp để tổ chức firmware RTOS.</p></div>
</div>
"""

COURSE = dict(
    slug="freertos", title="FreeRTOS cho lập trình nhúng", short_title="FreeRTOS", icon="⏱",
    badge=f"{len(_all)} bài · 23 ví dụ chạy thật", tagline="Đa nhiệm thời gian thực trên ESP32 / STM32: task, lập lịch, queue, semaphore, mutex, notification, event group, buffer, software timer — và một firmware hoàn chỉnh.",
    stats=[("bài học", str(len(_all))), ("ví dụ chạy thật", "23"), ("mục giáo trình", "62")],
    header_sub=f"Khóa học: ⏱ FreeRTOS cho lập trình nhúng (ESP32 / STM32) · {len(_all)} buổi",
    gradient=["#7c2d12", "#c2410c", "#d97706"], storage="frtos", overview=OVERVIEW, groups=GROUPS, code_dir=CODE, runner=run,
)

if __name__ == "__main__":
    if "--rebuild-lib" in sys.argv or not os.path.exists(LIB):
        build_lib()
    coursekit.build(COURSE, os.path.abspath(os.path.join(HERE, "..", "..", "training", "freertos.html")))
