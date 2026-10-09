# -*- coding: utf-8 -*-
"""Hình minh hoạ cho khóa FreeRTOS."""
from svg import svg, box, text, arrow, path

CLS = {"a": "bx-a", "b": "bx-b", "c": "bx-c", "d": "bx-d", "e": "bx-e", "g": "bx-g"}


def gantt(rows, t_max, w=700, title=None, marks=()):
    """rows: [(tên, [(t0, t1, lớp, nhãn), ...])]  – biểu đồ thời gian chạy của các task."""
    x0, rh = 130, 34
    scale = (w - x0 - 20) / t_max
    b = []
    y = 10
    if title:
        b.append(text(10, 20, title, "s"))
        y = 44 if marks else 34
    top = y
    for name, segs in rows:
        b.append(text(10, y + 21, name, "s"))
        b.append(f'<line class="ln thin dash" x1="{x0}" y1="{y + rh - 4}" x2="{w - 20}" y2="{y + rh - 4}"/>')
        for t0, t1, c, lbl in segs:
            bw = max(2, (t1 - t0) * scale)
            b.append(box(x0 + t0 * scale, y + 6, bw, rh - 12, CLS[c], rx=3, text=lbl if bw >= len(lbl) * 6.2 + 6 else None, tcls="xs"))
        y += rh
    b.append(arrow(x0, y + 6, w - 14, y + 6))
    for t in range(0, t_max + 1, max(1, t_max // 10)):
        b.append(text(x0 + t * scale, y + 22, str(t), "xs mute", "middle"))
    b.append(text(w - 20, y - 2, "ms", "xs mute", "end"))
    for t, lbl in marks:
        b.append(f'<line class="ln thin dash" x1="{x0 + t * scale}" y1="{top - 8}" x2="{x0 + t * scale}" y2="{y + 6}"/>')
        b.append(text(x0 + t * scale + 3, top - 1, lbl, "xs"))
    return svg(w, y + 32, "".join(b), "Biểu đồ thời gian chạy của các task")


def superloop_vs_rtos():
    loop = gantt([("Siêu vòng lặp", [(0, 250, "b", "đọc DHT22"), (250, 450, "c", "LCD"), (450, 700, "b", "đọc DHT22"), (700, 900, "c", "LCD")])],
                 900, title="Không RTOS: nút nhấn lúc 120 ms phải chờ tới khi vòng lặp quay lại (nếu còn kịp)", marks=[(120, "nhấn nút")])
    rtos = gantt([("Task Nút (ƯT 3)", [(120, 135, "e", "")]),
                  ("Task LCD (ƯT 2)", [(250, 450, "c", "LCD"), (700, 900, "c", "LCD")]),
                  ("Task DHT (ƯT 1)", [(0, 120, "b", "đọc"), (135, 250, "b", "đọc"), (450, 700, "b", "đọc DHT22")])],
                 900, title="Có RTOS: task Nút ưu tiên cao chạy NGAY lúc 120 ms, các task khác tiếp tục sau đó", marks=[(120, "nhấn nút")])
    return loop + rtos


def task_states():
    b = [box(280, 20, 150, 50, "bx-d", text="Running", sub="đang chiếm CPU", tcls="t"),
         box(40, 150, 150, 50, "bx-a", text="Ready", sub="sẵn sàng, chờ tới lượt", tcls="t"),
         box(520, 150, 150, 50, "bx-b", text="Blocked", sub="chờ thời gian / sự kiện", tcls="t"),
         box(280, 290, 150, 50, "bx-g", text="Suspended", sub="bị tạm dừng", tcls="t")]
    b.append(path("M190,160 C220,110 250,70 280,52"))
    b.append(text(150, 100, "scheduler chọn", "xs mute"))
    b.append(path("M285,62 C240,95 215,125 190,170"))
    b.append(text(232, 140, "bị chiếm quyền / taskYIELD", "xs mute"))
    b.append(path("M430,52 C480,80 520,110 545,150"))
    b.append(text(500, 92, "vTaskDelay, xQueueReceive,", "xs mute"))
    b.append(text(500, 106, "xSemaphoreTake (chờ)...", "xs mute"))
    b.append(arrow(520, 185, 192, 185, label="hết thời gian / có sự kiện", ly=178))
    b.append(path("M355,70 L355,288"))
    b.append(text(362, 230, "vTaskSuspend()", "xs mute"))
    b.append(path("M280,320 C150,320 110,260 110,202"))
    b.append(text(70, 290, "vTaskResume()", "xs mute"))
    b.append(path("M600,200 C600,280 520,315 432,315"))
    b.append(text(540, 300, "vTaskSuspend()", "xs mute"))
    return svg(710, 350, "".join(b), "Sơ đồ trạng thái task")


def preemption():
    return gantt([("KhanCap (ƯT 3)", [(170, 172, "e", ""), (340, 342, "e", ""), (510, 512, "e", "")]),
                  ("ThamLam (ƯT 2)", [(700, 1000, "c", "chiếm CPU 300 ms")]),
                  ("Nen (ƯT 1)", [(0, 170, "b", "khối 1–2"), (172, 340, "b", "khối 2–4"), (342, 510, "b", ""), (512, 700, "b", "khối 5–7"), (1000, 1300, "b", "khối 7–10")]),
                  ("IDLE (ƯT 0)", [])], 1300, title="Kết quả ví dụ 03: chiếm quyền và hiện tượng “đói” CPU (vùng 700–1000 ms)")


def context_switch():
    b = [box(20, 30, 150, 120, "bx-a", rx=6), text(95, 50, "Task A", "t", "middle"), text(32, 74, "Stack A", "xs"),
         text(32, 92, "• thanh ghi R0..R12", "xs mute"), text(32, 108, "• PC, LR, xPSR", "xs mute"), text(32, 124, "• biến cục bộ", "xs mute"),
         box(540, 30, 150, 120, "bx-b", rx=6), text(615, 50, "Task B", "t", "middle"), text(552, 74, "Stack B", "xs"),
         text(552, 92, "• thanh ghi đã lưu", "xs mute"), text(552, 108, "  từ lần trước", "xs mute")]
    b.append(box(280, 40, 150, 100, "bx-c", rx=6, text="Kernel FreeRTOS", sub="ngắt tick / PendSV"))
    b.append(arrow(170, 70, 278, 70, label="1. lưu ngữ cảnh A"))
    b.append(arrow(430, 110, 538, 110, label="3. khôi phục B"))
    b.append(text(350, 168, "2. chọn task Ready có ưu tiên cao nhất (pxCurrentTCB = B)", "xs mute", "middle"))
    b.append(text(350, 190, "Mỗi task có TCB (Task Control Block): con trỏ stack, ưu tiên, trạng thái, tên, notification…", "xs mute", "middle"))
    return svg(700, 200, "".join(b), "Chuyển ngữ cảnh")


def queue_fig():
    b = [box(20, 50, 130, 50, "bx-a", text="Task gửi", sub="xQueueSend()")]
    b.append(arrow(150, 75, 220, 75))
    b.append(box(222, 40, 300, 70, "bx", rx=6))
    for i, v in enumerate(["283", "286", "289", "", ""]):
        b.append(box(232 + i * 57, 50, 50, 50, "bx-b" if v else "bx-g", rx=4, text=v or "–", tcls="s"))
    b.append(text(372, 128, "Hàng đợi 5 phần tử (FIFO) – dữ liệu được SAO CHÉP vào", "xs mute", "middle"))
    b.append(arrow(522, 75, 592, 75))
    b.append(box(594, 50, 130, 50, "bx-d", text="Task nhận", sub="xQueueReceive()"))
    b.append(text(232, 32, "đầu (ra trước)", "xs mute"))
    b.append(text(510, 32, "đuôi (vào sau)", "xs mute", "end"))
    b.append(text(20, 156, "Đầy → task gửi bị chặn (hoặc trả về lỗi nếu timeout = 0).  Rỗng → task nhận bị chặn, không tốn CPU.", "xs mute"))
    return svg(740, 166, "".join(b), "Hàng đợi queue")


def deferred_isr():
    return gantt([("ISR nút", [(250, 253, "e", ""), (520, 523, "e", "")]),
                  ("XuLyNut (ƯT 3)", [(253, 268, "d", "xử lý"), (523, 538, "d", "xử lý")]),
                  ("Nen (ƯT 1)", [(0, 250, "b", "tính toán"), (268, 520, "b", "tính toán"), (538, 700, "b", "")])],
                 700, title="ISR chỉ xSemaphoreGiveFromISR rồi thoát; task xử lý ưu tiên cao chạy ngay sau ngắt",
                 marks=[(250, "ngắt"), (520, "ngắt")])


def inversion():
    a = gantt([("Cao (ƯT 3)", [(10, 12, "e", "chờ"), (302, 310, "e", "")]),
               ("Vua (ƯT 2)", [(21, 221, "c", "chạy 200 ms")]),
               ("Thap (ƯT 1)", [(0, 21, "b", "giữ khoá"), (221, 302, "b", "giữ khoá")])], 450,
              title="Binary semaphore: Cao chờ 291 ms — bị Vua (không liên quan) chặn gián tiếp")
    b = gantt([("Cao (ƯT 3)", [(10, 12, "e", "chờ"), (100, 108, "e", "")]),
               ("Vua (ƯT 2)", [(101, 301, "c", "chạy 200 ms")]),
               ("Thap (ƯT 1→3)", [(0, 100, "d", "giữ khoá, được nâng ƯT 3")])], 450,
              title="Mutex: Thap được KẾ THỪA ưu tiên 3, trả khoá sớm — Cao chỉ chờ 90 ms")
    return a + b


def notify_fig():
    b = [box(20, 20, 260, 130, "bx-a", rx=8), text(150, 42, "TCB của task XuLy", "t", "middle")]
    for i, s in enumerate(["con trỏ stack", "ưu tiên, trạng thái", "tên task"]):
        b.append(text(40, 66 + i * 18, "• " + s, "xs mute"))
    b.append(box(36, 116, 228, 26, "bx-b", rx=4, text="notification: uint32_t value + state", tcls="xs"))
    ops = [("vTaskNotifyGive / ulTaskNotifyTake", "như semaphore"), ("xTaskNotify(..., eSetBits)", "như event group"),
           ("xTaskNotify(..., eSetValueWithOverwrite)", "như mailbox"), ("xTaskNotify(..., eIncrement)", "như counting semaphore")]
    for i, (o, k) in enumerate(ops):
        y = 30 + i * 32
        b.append(arrow(470, y + 6, 268, 128 - (3 - i) * 3, cls="ln thin"))
        b.append(text(480, y + 4, o, "mono"))
        b.append(text(480, y + 18, k, "xs mute"))
    b.append(text(20, 176, "Không cần tạo đối tượng riêng → nhanh hơn ~45% và không tốn thêm RAM. Giới hạn: chỉ MỘT task nhận.", "xs mute"))
    return svg(790, 186, "".join(b), "Task notification")


def event_group():
    b = [text(10, 20, "Event group = một biến bit, mỗi bit là một sự kiện", "s")]
    bits = [("bit 3", "LỖI", "g"), ("bit 2", "CẢM BIẾN", "d"), ("bit 1", "THẺ SD", "d"), ("bit 0", "WIFI", "d")]
    for i, (n, t, c) in enumerate(bits):
        x = 20 + i * 110
        b.append(text(x + 50, 42, n, "xs mute", "middle"))
        b.append(box(x, 48, 100, 40, CLS[c], rx=4, text=f"{t} = {0 if c == 'g' else 1}", tcls="xs"))
    b.append(text(20, 116, "xEventGroupWaitBits(eg, WIFI|SD|CẢM BIẾN, xoá?, chờ TẤT CẢ = pdTRUE, ...)  → AND", "mono"))
    b.append(text(20, 136, "xEventGroupWaitBits(eg, LỖI|...,           xoá?, chờ TẤT CẢ = pdFALSE, ...) → OR", "mono"))
    b.append(text(20, 158, "xEventGroupSync(): mỗi task đặt bit của mình rồi chờ đủ bit của tất cả → đồng bộ tại một điểm", "xs mute"))
    return svg(700, 168, "".join(b), "Event group")


def timer_daemon():
    b = [box(20, 30, 150, 50, "bx-a", text="Task ứng dụng", sub="xTimerStart / Reset / Stop"),
         arrow(170, 55, 245, 55, label="lệnh"),
         box(247, 35, 130, 40, "bx-b", rx=4, text="timer command queue", tcls="xs"),
         arrow(377, 55, 445, 55),
         box(447, 20, 200, 70, "bx-c", text="Timer daemon task", sub="tên \"Tmr Svc\""),
         arrow(547, 90, 547, 130, label="hết hạn → gọi", lx=600, ly=114),
         box(457, 132, 180, 46, "bx-d", text="callback(TimerHandle_t)", sub="KHÔNG được chặn")]
    b.append(text(20, 120, "One-shot: chạy 1 lần.", "s"))
    b.append(text(20, 140, "Auto-reload: lặp lại theo chu kỳ.", "s"))
    b.append(text(20, 160, "Không tốn task riêng cho mỗi timer.", "s"))
    return svg(670, 188, "".join(b), "Timer daemon")


def stream_vs_message():
    b = [text(10, 18, "Stream buffer: dòng byte liên tục – đọc bao nhiêu tuỳ ý", "s")]
    for i, ch in enumerate("$GPGGA,21.02"):
        b.append(box(20 + i * 30, 28, 28, 28, "bx-a", rx=2, text=ch, tcls="mono"))
    b.append(text(10, 86, "Message buffer: từng thông điệp kèm độ dài – luôn nhận TRỌN một thông điệp", "s"))
    x = 20
    for msg in ["LED ON", "SERVO 90", "STOP"]:
        b.append(box(x, 96, 30, 28, "bx-c", rx=2, text=str(len(msg)), tcls="xs"))
        b.append(box(x + 32, 96, len(msg) * 13 + 10, 28, "bx-b", rx=2, text=msg, tcls="mono"))
        x += 32 + len(msg) * 13 + 22
    b.append(text(10, 150, "Cả hai: đúng MỘT bên ghi và MỘT bên đọc, rất nhẹ – dùng cho ISR → task (UART, ADC/DMA) và giữa hai nhân CPU.", "xs mute"))
    return svg(720, 160, "".join(b), "Stream buffer và message buffer")


def project_arch():
    b = [box(20, 30, 150, 52, "bx-a", text="CamBien (ƯT 3)", sub="mỗi 200 ms – DelayUntil"),
         arrow(170, 56, 238, 56, label="queue"),
         box(240, 30, 160, 52, "bx-b", text="XuLy (ƯT 2)", sub="lọc TB3, cập nhật LCD"),
         arrow(400, 46, 478, 30, label="mutex"),
         box(480, 10, 150, 40, "bx-g", text="LCD (tài nguyên chung)", tcls="xs"),
         arrow(400, 70, 478, 92, label="event group"),
         box(480, 72, 150, 44, "bx-e", text="CanhBao (ƯT 4)", sub="còi + SMS"),
         box(20, 130, 150, 44, "bx-g", text="ISR nút MODE", tcls="s"),
         arrow(170, 152, 238, 152, label="notification"),
         box(240, 130, 160, 44, "bx-c", text="GiaoDien (ƯT 2)", sub="đổi chế độ hiển thị"),
         box(480, 130, 150, 44, "bx-d", text="Software timer", sub="heartbeat 500 ms")]
    return svg(650, 186, "".join(b), "Kiến trúc dự án trạm thời tiết")


def source_tree():
    rows = [("FreeRTOS-Kernel/", ""), ("├─ tasks.c", "lập lịch, quản lý task"), ("├─ queue.c", "queue, semaphore, mutex"),
            ("├─ list.c", "danh sách liên kết dùng nội bộ"), ("├─ timers.c", "software timer (tuỳ chọn)"),
            ("├─ event_groups.c", "event group (tuỳ chọn)"), ("├─ stream_buffer.c", "stream & message buffer (tuỳ chọn)"),
            ("├─ include/", "FreeRTOS.h, task.h, queue.h, semphr.h…"),
            ("└─ portable/", "phần phụ thuộc chip + trình biên dịch"), ("   ├─ GCC/ARM_CM4F/", "port.c, portmacro.h cho STM32F4"),
            ("   ├─ MSVC-MingW/", "port mô phỏng trên Windows (khóa này dùng)"), ("   └─ MemMang/", "heap_1.c … heap_5.c")]
    b = []
    for i, (a, d) in enumerate(rows):
        b.append(text(20, 24 + i * 20, a, "mono"))
        b.append(text(250, 24 + i * 20, d, "xs mute"))
    b.append(text(20, 24 + len(rows) * 20 + 8, "+ FreeRTOSConfig.h do ỨNG DỤNG cung cấp: bật/tắt tính năng, tần số tick, kích thước heap…", "s"))
    return svg(640, 24 + len(rows) * 20 + 22, "".join(b), "Cấu trúc mã nguồn FreeRTOS")
