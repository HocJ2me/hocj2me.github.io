# -*- coding: utf-8 -*-
"""12 bài của khóa FreeRTOS."""
import figs

ESP = "<b>ESP32 (Arduino / ESP-IDF)</b>"

L01 = dict(
  id="gioi-thieu", short="RTOS là gì?", title="Giới thiệu RTOS và FreeRTOS", icon="⏱", time="2 giờ",
  goal="Hiểu vì sao firmware cần hệ điều hành thời gian thực, FreeRTOS gồm những gì và chuẩn bị môi trường thực hành.",
  goals=["Phân biệt siêu vòng lặp (super loop) và đa nhiệm với RTOS", "Hiểu “thời gian thực” nghĩa là đúng hạn, không phải chạy nhanh",
         "Biết các khối xây dựng của FreeRTOS và cấu trúc mã nguồn", "Cài môi trường: ESP32 (Arduino/ESP-IDF), STM32CubeIDE hoặc bản mô phỏng trên PC"],
  sections=[
    dict(h="Vấn đề của siêu vòng lặp", code="00-sieu-vong-lap.cpp", fig=figs.superloop_vs_rtos(),
         figcap="So sánh cùng một chương trình viết kiểu siêu vòng lặp và kiểu RTOS.", html="""
<p>Chương trình Arduino thông thường là <b>siêu vòng lặp</b>: <code>loop()</code> làm lần lượt từng việc. Khi một việc dùng <code>delay()</code> hoặc chạy lâu (đọc cảm biến 250 ms, vẽ màn hình 200 ms), mọi việc khác phải chờ — nút nhấn bị bỏ lỡ, động cơ phản hồi chậm.</p>""",
         notes=["Ví dụ này KHÔNG dùng FreeRTOS: chỉ mô phỏng thời gian để thấy 3/4 lần nhấn nút bị bỏ lỡ.",
                "Có thể vá bằng <code>millis()</code> (bài 4 khóa C++), nhưng khi số việc tăng, code thành “mì ống” khó bảo trì — đó là lúc cần RTOS."]),
    dict(h="RTOS và FreeRTOS", html="""
<p><b>RTOS</b> (Real-Time Operating System) là hệ điều hành nhỏ cho vi điều khiển, cho phép chia chương trình thành nhiều <b>task</b> chạy “song song”. <b>Thời gian thực</b> nghĩa là <b>đảm bảo phản hồi trong một hạn định</b> (deterministic) — không nhất thiết là nhanh nhất.</p>
<div class="grid2"><div class="card"><h5>Hard real-time</h5><p>Trễ hạn = hỏng: túi khí ô tô, điều khiển động cơ, máy trợ tim.</p></div>
<div class="card"><h5>Soft real-time</h5><p>Trễ hạn = giảm chất lượng: phát nhạc, cập nhật màn hình, gửi dữ liệu IoT.</p></div></div>
<p><b>FreeRTOS</b> (Richard Barry, 2003; Amazon tiếp quản 2017) là RTOS phổ biến nhất thế giới: mã nguồn mở <b>MIT</b>, nhân chỉ vài file C, chạy trên hơn 40 kiến trúc (ARM Cortex-M, ESP32 Xtensa/RISC-V, AVR, PIC, RISC-V…). <b>ESP32 chạy FreeRTOS ngay cả khi bạn viết Arduino</b> — <code>setup()</code>/<code>loop()</code> chính là một task.</p>
<table class="tbl"><tr><th>Khối xây dựng</th><th>Vai trò</th><th>Bài</th></tr>
<tr><td>Task</td><td>đơn vị thực thi độc lập, có stack và ưu tiên riêng</td><td>2–4</td></tr>
<tr><td>Queue</td><td>gửi dữ liệu giữa các task / từ ngắt</td><td>5</td></tr>
<tr><td>Semaphore, Mutex</td><td>báo hiệu sự kiện, bảo vệ tài nguyên chung</td><td>6–7</td></tr>
<tr><td>Task notification</td><td>báo hiệu trực tiếp tới task, nhẹ nhất</td><td>8</td></tr>
<tr><td>Event group</td><td>chờ nhiều sự kiện, đồng bộ nhiều task</td><td>9</td></tr>
<tr><td>Stream/Message buffer</td><td>truyền dòng byte / thông điệp</td><td>10</td></tr>
<tr><td>Software timer</td><td>gọi hàm sau một khoảng thời gian / định kỳ</td><td>11</td></tr></table>"""),
    dict(h="Cấu trúc mã nguồn và cấu hình", fig=figs.source_tree(), html="""
<p>Ứng dụng tự cung cấp file <code>FreeRTOSConfig.h</code> — nơi bật/tắt mọi tính năng. Các tuỳ chọn quan trọng:</p>
<table class="tbl"><tr><th>Tuỳ chọn</th><th>Ý nghĩa</th><th>Giá trị hay dùng</th></tr>
<tr><td><code>configTICK_RATE_HZ</code></td><td>số ngắt tick mỗi giây</td><td>1000 (1 tick = 1 ms); ESP32 Arduino: 1000</td></tr>
<tr><td><code>configMAX_PRIORITIES</code></td><td>số mức ưu tiên</td><td>5–25 (ESP32: 25)</td></tr>
<tr><td><code>configUSE_PREEMPTION</code></td><td>cho phép chiếm quyền</td><td>1</td></tr>
<tr><td><code>configTOTAL_HEAP_SIZE</code></td><td>heap cho FreeRTOS</td><td>tuỳ RAM chip</td></tr>
<tr><td><code>configMINIMAL_STACK_SIZE</code></td><td>stack tối thiểu (đơn vị word*)</td><td>128 trên Cortex-M</td></tr>
<tr><td><code>INCLUDE_vTaskDelete</code>…</td><td>bật các hàm API tuỳ chọn</td><td>1</td></tr></table>
<p class="callout warn">⚠️ *Trên FreeRTOS gốc, kích thước stack tính bằng <b>word</b> (4 byte trên chip 32 bit). Trên <b>ESP-IDF/Arduino-ESP32</b>, <code>xTaskCreate</code> nhận kích thước bằng <b>byte</b>.</p>"""),
    dict(h="Chuẩn bị môi trường", html=f"""
<table class="tbl"><tr><th>Môi trường</th><th>Cách bắt đầu</th></tr>
<tr><td>{ESP}</td><td>Cài board ESP32 trong Arduino IDE → dùng ngay <code>xTaskCreate</code>, <code>xQueueCreate</code>… không cần include gì thêm. ESP-IDF: <code>#include "freertos/FreeRTOS.h"</code>, <code>"freertos/task.h"</code>.</td></tr>
<tr><td><b>STM32</b></td><td>STM32CubeIDE → Middleware → FREERTOS (CMSIS-RTOS v2), hoặc thêm FreeRTOS-Kernel thủ công.</td></tr>
<tr><td><b>Mô phỏng trên PC</b> (khóa này)</td><td>FreeRTOS-Kernel + port <code>MSVC-MingW</code> (Windows) hoặc <code>ThirdParty/GCC/Posix</code> (Linux/macOS). Toàn bộ ví dụ trong khóa đã chạy thật trên bản mô phỏng, có in mốc thời gian (ms) để quan sát lập lịch.</td></tr></table>
<p>Lệnh build một ví dụ trên Windows (MinGW): <code>g++ -std=c++17 -Isim -Ikernel/include -Ikernel/portable/MSVC-MingW vi_du.cpp libfreertos.a -lwinmm -o app</code>. File <code>sim.h</code> cung cấp <code>LOG()</code> (in kèm thời gian) và hàm giả lập ngắt; trên board thật thay <code>LOG</code> bằng <code>Serial.printf</code>/<code>ESP_LOGI</code>.</p>"""),
  ],
  embedded=["Trên ESP32-Arduino, <code>loop()</code> chạy trong task <code>loopTask</code> ưu tiên 1, stack 8 KB, trên nhân 1. WiFi/Bluetooth chạy ở các task riêng trên nhân 0.",
            "Không nên dùng <code>delay()</code> dài trong task — dùng <code>vTaskDelay()</code> (trên ESP32 Arduino, <code>delay()</code> thực chất gọi <code>vTaskDelay</code>).",
            "Bản quyền MIT cho phép dùng FreeRTOS trong sản phẩm thương mại mà không phải công bố mã nguồn."],
  exercises=["Liệt kê 3 thiết bị quanh bạn cần hard real-time và 3 thiết bị soft real-time.",
             "Mở <code>FreeRTOSConfig.h</code> trong ví dụ của khóa và giải thích 5 tuỳ chọn bất kỳ.",
             "Cài board ESP32 trong Arduino IDE, in <code>uxTaskGetNumberOfTasks()</code> trong <code>setup()</code> — có bao nhiêu task đang chạy dù bạn chưa tạo task nào?"],
  refs=[("FreeRTOS – Getting Started", "https://www.freertos.org/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview"),
        ("Mastering the FreeRTOS Real Time Kernel (sách miễn phí)", "https://github.com/FreeRTOS/FreeRTOS-Kernel-Book")],
)

L02 = dict(
  id="task", short="Task", title="Task: tạo, tham số, stack, xoá", icon="🧵", time="2 giờ",
  goal="Viết và tạo task đúng cách, truyền tham số, chọn kích thước stack và quản lý task bằng handle.",
  goals=["Viết hàm task với vòng lặp vô hạn", "Dùng <code>xTaskCreate</code> và <code>xTaskCreateStatic</code>", "Truyền tham số qua <code>void*</code>",
         "Đo stack còn trống, xoá task, truy vấn trạng thái"],
  sections=[
    dict(h="Task đầu tiên", code="01-hello-task.cpp", html="""
<p>Một task là một hàm <code>void tenTask(void* thamSo)</code> chứa <b>vòng lặp vô hạn</b> và <b>không bao giờ return</b> (muốn kết thúc thì gọi <code>vTaskDelete(NULL)</code>).</p>
<p><code>xTaskCreate(hàm, "tên", stack, thamSo, ưuTiên, &amp;handle)</code> tạo task; <code>vTaskStartScheduler()</code> trao quyền điều khiển CPU cho FreeRTOS.</p>""",
         notes=["Hai task có chu kỳ 500 ms và 300 ms chạy độc lập — không task nào phải chờ task kia.",
                "<code>vTaskDelay(pdMS_TO_TICKS(500))</code> đưa task vào trạng thái <i>Blocked</i>, CPU được nhường cho task khác. Đây là điểm khác biệt quyết định so với <code>delay()</code>.",
                "Tham số phải còn sống khi task chạy — dùng biến <code>static</code>/toàn cục, không dùng biến cục bộ của <code>main()</code>/<code>setup()</code>.",
                "Trên ESP32: <code>setup()</code> tạo task rồi kết thúc; scheduler đã được khởi động sẵn, không gọi <code>vTaskStartScheduler()</code>."]),
    dict(h="Tham số, task tĩnh, handle và stack", code="02-task-tham-so-stack.cpp", html="""
<table class="tbl"><tr><th>Hàm</th><th>Dùng để</th></tr>
<tr><td><code>xTaskCreate</code></td><td>tạo task, cấp stack + TCB từ heap của FreeRTOS</td></tr>
<tr><td><code>xTaskCreateStatic</code></td><td>tạo task với stack + TCB do bạn cấp sẵn (không heap — hợp với hệ thống an toàn)</td></tr>
<tr><td><code>vTaskDelete(handle)</code></td><td>xoá task (NULL = chính nó); bộ nhớ được idle task giải phóng</td></tr>
<tr><td><code>uxTaskGetStackHighWaterMark</code></td><td>stack còn trống ít nhất từ trước tới giờ — dùng để chỉnh kích thước stack</td></tr>
<tr><td><code>eTaskGetState</code>, <code>uxTaskGetNumberOfTasks</code></td><td>truy vấn trạng thái, đếm số task</td></tr></table>""",
         notes=["Cùng một hàm <code>taskCamBien</code> tạo được nhiều task nhờ tham số khác nhau (struct cấu hình).",
                "Stack mỗi task trên chip thật thường 1–4 KB. Chạy thử, đọc high water mark, rồi đặt kích thước = dùng thật + 20–30% dự phòng.",
                "Số task cuối cùng là 3 vì FreeRTOS tự tạo thêm <b>IDLE</b> và <b>Tmr Svc</b> (timer daemon)."]),
  ],
  embedded=["ESP32: <code>xTaskCreatePinnedToCore(ham, \"ten\", 4096, NULL, 1, &amp;h, 1)</code> — chọn nhân 0 hoặc 1 để chạy task.",
            "Tràn stack là lỗi phổ biến nhất: biến cục bộ lớn (mảng 1 KB), <code>printf</code> số thực, đệ quy. Bật <code>configCHECK_FOR_STACK_OVERFLOW 2</code> khi phát triển.",
            "Không tạo/xoá task liên tục lúc chạy — tạo hết ở lúc khởi động để tránh phân mảnh heap."],
  mistakes=["Hàm task chạy hết rồi <code>return</code> → crash.", "Truyền con trỏ tới biến cục bộ của hàm tạo task.", "Stack quá nhỏ → hành vi kỳ lạ, reset ngẫu nhiên."],
  exercises=["Tạo 3 task nháy 3 LED với chu kỳ 200/300/500 ms từ CÙNG một hàm task.",
             "In stack high water mark của một task có mảng cục bộ <code>char buf[300]</code> và so sánh.",
             "Viết task “giám sát” mỗi giây in số task đang chạy."],
)

L03 = dict(
  id="lap-lich", short="Lập lịch & ưu tiên", title="Lập lịch, trạng thái task và ưu tiên", icon="📅", time="2 giờ",
  goal="Hiểu scheduler chọn task nào chạy, các trạng thái của task và cách điều khiển chúng.",
  goals=["Nắm 4 trạng thái Running/Ready/Blocked/Suspended", "Hiểu chiếm quyền (preemption), chia lượt (time slicing), hiện tượng “đói” CPU",
         "Hiểu chuyển ngữ cảnh (context switch) và ngắt tick", "Dùng <code>vTaskDelayUntil</code>, <code>vTaskSuspend/Resume</code>, <code>vTaskPrioritySet</code>"],
  sections=[
    dict(h="Trạng thái task", fig=figs.task_states(), figcap="Một task chỉ ở MỘT trong bốn trạng thái tại mỗi thời điểm.", html="""
<p>Trên CPU một nhân, tại mỗi thời điểm chỉ <b>một</b> task ở trạng thái <b>Running</b>. Task chờ thời gian (<code>vTaskDelay</code>) hay chờ sự kiện (queue, semaphore) ở trạng thái <b>Blocked</b> — không tốn chút CPU nào. Đây là lý do RTOS hiệu quả: phần lớn thời gian các task ngủ chờ sự kiện.</p>"""),
    dict(h="Thuật toán lập lịch", fig=figs.preemption(), html="""
<p>FreeRTOS dùng lập lịch <b>ưu tiên cố định, có chiếm quyền</b>:</p>
<ol><li>Luôn chạy task <b>Ready có ưu tiên cao nhất</b> (số càng lớn càng ưu tiên; 0 là idle).</li>
<li>Khi task ưu tiên cao hơn chuyển sang Ready (hết delay, nhận được dữ liệu), nó <b>chiếm quyền</b> ngay lập tức.</li>
<li>Các task <b>cùng ưu tiên</b> chia lượt mỗi tick (time slicing).</li></ol>
<p>Nếu task ưu tiên cao không bao giờ Blocked (vòng lặp bận), mọi task thấp hơn bị <b>đói CPU</b> (starvation). Quy tắc vàng: <b>task ưu tiên cao phải ngắn và phải chờ sự kiện</b>.</p>""",
         code="03-uu-tien-preemption.cpp", notes=["KhanCap chạy đúng các mốc 170/340/510 ms dù task Nen đang tính toán.",
                                                  "Từ 701 đến 1001 ms task Nen im lặng hoàn toàn vì ThamLam (ưu tiên 2) chiếm CPU mà không nhường."]),
    dict(h="Chuyển ngữ cảnh và ngắt tick", fig=figs.context_switch(), html="""
<p>Một bộ timer phần cứng tạo <b>ngắt tick</b> (thường 1 ms). Trong ngắt, kernel tăng bộ đếm tick, đánh thức task hết hạn delay và quyết định có cần đổi task không. <b>Chuyển ngữ cảnh</b> = lưu toàn bộ thanh ghi của task cũ vào stack của nó, nạp thanh ghi của task mới — mất vài micro giây trên Cortex-M.</p>"""),
    dict(h="Điều khiển task", code="04-delay-until-suspend.cpp", html="""
<table class="tbl"><tr><th>Hàm</th><th>Tác dụng</th></tr>
<tr><td><code>vTaskDelay(n)</code></td><td>ngủ n tick tính từ <b>lúc gọi</b></td></tr>
<tr><td><code>vTaskDelayUntil(&amp;moc, n)</code></td><td>ngủ tới <b>moc + n</b> → chu kỳ chính xác, không trôi (lấy mẫu cảm biến, vòng điều khiển PID)</td></tr>
<tr><td><code>vTaskSuspend / vTaskResume</code></td><td>tạm dừng / tiếp tục một task</td></tr>
<tr><td><code>vTaskPrioritySet / uxTaskPriorityGet</code></td><td>đổi / đọc ưu tiên lúc chạy</td></tr>
<tr><td><code>taskYIELD()</code></td><td>tự nhường CPU cho task cùng ưu tiên</td></tr></table>""",
         notes=["Với <code>vTaskDelay</code>, chu kỳ thực = 100 + 30 = 130 ms và bị trôi. Với <code>vTaskDelayUntil</code> các mốc đúng 521, 621, 721, 821.",
                "Trong lúc bị Suspend (1321–1721 ms) NhayLed không in gì."]),
  ],
  embedded=["Gợi ý phân ưu tiên: điều khiển động cơ/an toàn &gt; giao tiếp (UART, CAN) &gt; xử lý dữ liệu &gt; hiển thị &gt; ghi log.",
            "ESP32 có 2 nhân: scheduler chạy riêng trên mỗi nhân (SMP), nên hai task có thể chạy THỰC SỰ song song.",
            "Vòng điều khiển (PID, cân bằng robot) luôn dùng <code>vTaskDelayUntil</code> để chu kỳ lấy mẫu ổn định."],
  mistakes=["Đặt mọi task cùng ưu tiên cao nhất “cho chắc”.", "Vòng lặp bận chờ (<code>while(!co){}</code>) trong task ưu tiên cao.",
            "Dùng <code>vTaskSuspend</code> để đồng bộ dữ liệu thay vì semaphore/queue."],
  exercises=["Vẽ biểu đồ thời gian (Gantt) cho 3 task: A(ƯT 3, chạy 10 ms mỗi 50 ms), B(ƯT 2, 20 ms mỗi 100 ms), C(ƯT 1, luôn bận).",
             "Sửa ví dụ 03 để task ThamLam không làm đói task Nen.", "Viết task lấy mẫu chính xác 50 Hz bằng <code>vTaskDelayUntil</code>."],
)

L04 = dict(
  id="idle-tien-ich", short="Idle task & tiện ích", title="Idle task, idle hook và các hàm tiện ích của kernel", icon="😴", time="1,5 giờ",
  goal="Hiểu idle task, dùng idle hook để đo tải CPU/tiết kiệm điện, và các API điều khiển kernel.",
  goals=["Biết idle task làm gì và vì sao không được chặn", "Viết idle hook đo CPU rảnh", "Dùng vùng găng và tạm dừng scheduler đúng chỗ",
         "Dùng <code>vTaskList</code>, <code>pcTaskGetName</code>… để gỡ lỗi"],
  sections=[
    dict(h="Idle task và idle hook", html="""
<p><b>Idle task</b> (ưu tiên 0) được tạo tự động khi khởi động scheduler, chạy khi không còn task nào Ready. Nó giải phóng bộ nhớ của task đã bị xoá. <b>Idle hook</b> (<code>vApplicationIdleHook</code>, bật <code>configUSE_IDLE_HOOK</code>) là hàm của bạn được idle task gọi liên tục — dùng để đo tải CPU, cho chip ngủ (<code>__WFI()</code>), nuôi watchdog. Idle hook <b>không bao giờ được chặn</b>.</p>
<p>Tiết kiệm năng lượng nâng cao: <b>tickless idle</b> (<code>configUSE_TICKLESS_IDLE</code>) tắt ngắt tick khi rảnh lâu — ESP32 dùng cho chế độ light sleep tự động.</p>"""),
    dict(h="Kernel control và tiện ích", code="05-idle-hook-tien-ich.cpp", html="""
<table class="tbl"><tr><th>Hàm</th><th>Ý nghĩa</th></tr>
<tr><td><code>taskENTER_CRITICAL / taskEXIT_CRITICAL</code></td><td>vùng găng: tắt ngắt (tới mức cho phép) — giữ thật ngắn</td></tr>
<tr><td><code>vTaskSuspendAll / xTaskResumeAll</code></td><td>tạm dừng scheduler, ngắt vẫn chạy</td></tr>
<tr><td><code>vTaskList</code>, <code>uxTaskGetSystemState</code></td><td>liệt kê task, trạng thái, stack còn trống</td></tr>
<tr><td><code>xTaskGetTickCount</code>, <code>pcTaskGetName</code>, <code>xTaskGetHandle</code></td><td>đọc tick, tên task, tìm task theo tên</td></tr></table>""",
         notes=["Tải CPU đo được ~27%: khớp với task bận 60 ms trên mỗi chu kỳ ~200 ms.",
                "Bảng <code>vTaskList</code>: X = đang chạy, R = Ready, B = Blocked. Cột Stack là high water mark.",
                "Trên board thật, idle hook tính tải CPU bằng cách đếm số vòng lặp trong một giây rồi so với lúc hệ thống rảnh hoàn toàn."]),
  ],
  embedded=["ESP32: Task Watchdog theo dõi idle task — nếu một task ưu tiên cao chạy bận quá lâu làm idle không chạy được, chip báo lỗi \"Task watchdog got triggered\".",
            "Vùng găng trên ESP32 đa nhân dùng <code>portENTER_CRITICAL(&amp;spinlock)</code>."],
  mistakes=["Gọi <code>vTaskDelay</code> trong idle hook.", "Làm việc nặng (in, chờ) trong vùng găng.", "Quên gọi <code>xTaskResumeAll</code> sau <code>vTaskSuspendAll</code>."],
  exercises=["Sửa idle hook để in tải CPU mỗi giây.", "Viết lệnh Serial “ps” in bảng <code>vTaskList</code> để gỡ lỗi."],
)

L05 = dict(
  id="queue", short="Queue", title="Queue – hàng đợi truyền dữ liệu giữa các task", icon="📬", time="2 giờ",
  goal="Truyền dữ liệu an toàn giữa các task và từ ngắt tới task bằng queue.",
  goals=["Tạo queue, gửi/nhận có chờ và không chờ", "Gửi struct, gửi lên đầu hàng đợi, peek", "Gửi từ ISR bằng <code>xQueueSendFromISR</code>",
         "Xử lý khi hàng đợi đầy"],
  sections=[
    dict(h="Queue cơ bản", fig=figs.queue_fig(), code="06-queue-co-ban.cpp", html="""
<p>Queue là hàng đợi FIFO có kích thước cố định, an toàn khi nhiều task/ngắt dùng chung. Dữ liệu được <b>sao chép</b> vào queue (không phải con trỏ) — task gửi có thể dùng lại biến ngay.</p>
<table class="tbl"><tr><th>API</th><th>Ghi chú</th></tr>
<tr><td><code>xQueueCreate(soPhanTu, kichThuoc)</code></td><td>tạo hàng đợi</td></tr>
<tr><td><code>xQueueSend(q, &amp;x, timeout)</code></td><td>gửi vào cuối; chờ tối đa timeout nếu đầy</td></tr>
<tr><td><code>xQueueReceive(q, &amp;x, timeout)</code></td><td>lấy từ đầu; chờ nếu rỗng (<code>portMAX_DELAY</code> = chờ mãi)</td></tr>
<tr><td><code>uxQueueMessagesWaiting</code></td><td>số phần tử đang chờ</td></tr></table>""",
         notes=["Phần 1: HienThi nhận ngay khi DocCamBien gửi — task nhận ngủ trong lúc chờ.",
                "Phần 2: hàng đợi 3 phần tử đầy, các giá trị 5, 7, 8 bị bỏ (timeout = 0). Chọn kích thước queue theo tốc độ gửi/nhận tệ nhất."]),
    dict(h="Queue chứa struct, nhiều nguồn, từ ngắt", code="07-queue-struct.cpp", html="""
<p>Mẫu thiết kế phổ biến: <b>nhiều task nguồn → một queue → một task xử lý</b> (ghi log, gửi MQTT). Mỗi phần tử là một struct mô tả nguồn và giá trị.</p>
<ul><li><code>xQueueSendToFront</code>: chen lên đầu — cho tin khẩn.</li><li><code>xQueuePeek</code>: xem mà không lấy ra.</li>
<li>Trong ISR chỉ dùng hàm có hậu tố <b>FromISR</b>: không bao giờ chờ, trả về cờ “cần chuyển ngữ cảnh”.</li></ul>""",
         notes=["Tin khói (khẩn) được xử lý trước dù gửi sau các tin nhiệt độ/độ ẩm.",
                "Struct nên nhỏ (ở đây 6 byte). Dữ liệu lớn: gửi con trỏ tới bộ đệm trong một Object Pool thay vì sao chép cả khối.",
                "Ngắt nút nhấn gửi thẳng vào cùng queue bằng <code>xQueueSendFromISR</code>."]),
  ],
  embedded=["UART RX (ESP-IDF): driver UART đẩy sự kiện vào một queue; task của bạn <code>xQueueReceive</code> để xử lý.",
            "ISR trên ESP32 Arduino: <code>BaseType_t w = pdFALSE; xQueueSendFromISR(q, &amp;v, &amp;w); if (w) portYIELD_FROM_ISR();</code>",
            "ISR trên ESP32 phải có thuộc tính <code>IRAM_ATTR</code>."],
  mistakes=["Gọi <code>xQueueSend</code> (không FromISR) trong ngắt.", "Gửi con trỏ tới biến cục bộ đã chết qua queue.", "Queue quá nhỏ làm mất dữ liệu mà không biết."],
  exercises=["Task đọc 3 cảm biến gửi struct vào queue; task khác tính trung bình mỗi loại và in ra mỗi giây.",
             "Thêm bộ đếm số bản tin bị bỏ khi queue đầy.", "Thiết kế queue lệnh cho robot: ký tự lệnh từ Serial → task điều khiển động cơ."],
)

L06 = dict(
  id="semaphore", short="Semaphore", title="Binary semaphore và counting semaphore", icon="🚦", time="2 giờ",
  goal="Dùng semaphore để báo hiệu sự kiện (đặc biệt từ ngắt) và quản lý nhóm tài nguyên.",
  goals=["Hiểu kỹ thuật xử lý ngắt trì hoãn (deferred interrupt processing)", "Dùng binary semaphore ISR → task",
         "Dùng counting semaphore quản lý N tài nguyên và đếm sự kiện"],
  sections=[
    dict(h="Binary semaphore: báo hiệu từ ngắt", fig=figs.deferred_isr(), code="08-binary-semaphore-isr.cpp", html="""
<p>Binary semaphore giống một lá cờ 0/1. Mẫu kinh điển: <b>ISR thật ngắn</b> — chỉ <code>xSemaphoreGiveFromISR</code> — rồi một <b>task ưu tiên cao</b> đang chờ <code>xSemaphoreTake</code> thức dậy làm phần việc nặng (đọc I2C, chống dội, tính toán). Nhờ vậy ngắt khoá hệ thống trong thời gian cực ngắn.</p>""",
         notes=["Mỗi lần ngắt, XuLyNut chạy ngay tại thời điểm ngắt (251, 521, 902 ms) dù task Nen đang bận.",
                "<code>xSemaphoreCreateBinary()</code> tạo ra ở trạng thái rỗng — lần take đầu sẽ chờ.",
                "Nếu nhiều ngắt tới trước khi task kịp take, binary semaphore chỉ nhớ 1 lần — dùng counting semaphore hoặc queue nếu cần đếm."]),
    dict(h="Counting semaphore", code="09-counting-semaphore.cpp", html="""
<p>Counting semaphore có bộ đếm 0…max. Hai cách dùng:</p>
<ul><li><b>Quản lý tài nguyên</b>: khởi tạo = số tài nguyên; take = mượn, give = trả (2 kênh DMA, 3 slot bộ đệm, 4 chỗ sạc).</li>
<li><b>Đếm sự kiện</b>: khởi tạo = 0; ISR give mỗi lần có sự kiện, task take để xử lý từng cái — không mất sự kiện.</li></ul>""",
         notes=["Task C, D phải chờ tới khi A, B trả kênh (301 ms).", "5 xung encoder dồn dập đều được đếm đủ."]),
  ],
  embedded=["Ngắt GPIO, ngắt UART, ngắt “DMA xong”, ngắt timer đều nên dùng mẫu deferred processing.",
            "Trên STM32: gọi <code>xSemaphoreGiveFromISR</code> trong <code>HAL_GPIO_EXTI_Callback</code>; ưu tiên ngắt phải ≥ <code>configMAX_SYSCALL_INTERRUPT_PRIORITY</code> (số lớn hơn = ưu tiên thấp hơn trên Cortex-M) mới được gọi API FreeRTOS.",
            "Task notification (bài 8) là cách nhẹ hơn để làm việc tương tự khi chỉ có một task nhận."],
  mistakes=["Dùng semaphore để bảo vệ tài nguyên chung (nên dùng mutex — bài 7).", "Xử lý nặng ngay trong ISR.", "Quên kiểm tra giá trị trả về khi take có timeout."],
  exercises=["Nút nhấn → binary semaphore → task đảo trạng thái LED (có chống dội 50 ms trong task).",
             "Bãi đỗ xe 3 chỗ, 6 ô tô (task) vào/ra ngẫu nhiên — dùng counting semaphore, in số chỗ trống."],
)

L07 = dict(
  id="mutex", short="Mutex", title="Mutex, đảo ưu tiên, mutex đệ quy", icon="🔐", time="2 giờ",
  goal="Bảo vệ tài nguyên dùng chung bằng mutex, hiểu đảo ưu tiên và tránh deadlock.",
  goals=["Nhận biết race condition trên tài nguyên chung (LCD, UART, I2C, biến toàn cục)", "Dùng mutex đúng: take/give trong cùng task",
         "Hiểu đảo ưu tiên và cơ chế kế thừa ưu tiên", "Dùng recursive mutex; tránh deadlock"],
  sections=[
    dict(h="Mutex bảo vệ tài nguyên", code="10-mutex-race.cpp", html="""
<p><b>Mutex</b> (mutual exclusion) là “chìa khoá” duy nhất của một tài nguyên: task nào lấy được (<code>xSemaphoreTake</code>) mới được dùng, dùng xong phải trả (<code>xSemaphoreGive</code>). Khác semaphore: mutex <b>có chủ sở hữu</b> — chỉ task đã lấy mới được trả — và có <b>kế thừa ưu tiên</b>.</p>""",
         notes=["Không mutex: dòng 2 của LCD bị lẫn “Do am : 61%  g” — chữ “g” còn sót từ “Khoi vuot nguong”.",
                "Có mutex: mỗi task ghi trọn vẹn 2 dòng rồi mới tới task khác."]),
    dict(h="Đảo ưu tiên và kế thừa ưu tiên", fig=figs.inversion(), code="11-priority-inversion.cpp", html="""
<p><b>Đảo ưu tiên</b>: task Cao chờ khoá do task Thap giữ; task Vua (không liên quan) chiếm CPU của Thap → Cao bị Vua chặn gián tiếp. Sự cố nổi tiếng: robot <b>Mars Pathfinder</b> (1997) liên tục reset vì lỗi này.</p>
<p>Mutex của FreeRTOS có <b>kế thừa ưu tiên</b>: khi Cao chờ, Thap tạm được nâng lên ưu tiên của Cao, làm xong nhanh rồi trả khoá; sau đó trở lại ưu tiên cũ.</p>""",
         notes=["Binary semaphore: Cao chờ 291 ms. Mutex: chỉ 90 ms.", "Dòng “ưu tiên hiện tại = 3” chứng minh Thap đã được nâng ưu tiên."]),
    dict(h="Mutex đệ quy và deadlock", code="12-recursive-mutex.cpp", html="""
<p><b>Recursive mutex</b> cho phép cùng một task lấy khoá nhiều lần (hàm gọi lồng nhau cùng bảo vệ một tài nguyên); phải trả đủ số lần đã lấy. <b>Deadlock</b> xảy ra khi các task chờ nhau mãi mãi — ví dụ A giữ khoá 1 chờ khoá 2, B giữ khoá 2 chờ khoá 1. Phòng tránh: luôn lấy các khoá theo <b>cùng một thứ tự</b>, dùng timeout, giữ khoá thật ngắn.</p>""",
         notes=["Mutex thường bị lấy lần 2 trong cùng task: chờ chính mình → thất bại sau 200 ms (với portMAX_DELAY sẽ treo vĩnh viễn)."]),
  ],
  embedded=["Mọi bus dùng chung (I2C, SPI, UART log) cần một mutex nếu nhiều task truy cập.",
            "Không dùng mutex trong ISR (mutex có chủ sở hữu, ISR không phải task) — dùng semaphore hoặc notification.",
            "Arduino-ESP32: <code>Serial.print</code> từ nhiều task có thể bị lẫn chữ — bọc bằng mutex hoặc gom log về một task."],
  mistakes=["Take mutex ở task này, give ở task khác.", "Giữ mutex trong lúc <code>vTaskDelay</code> dài.", "Lấy hai mutex theo thứ tự khác nhau ở hai task → deadlock."],
  exercises=["Hai task cùng in qua Serial: chứng minh bị lẫn, rồi sửa bằng mutex.",
             "Tạo cố ý một deadlock với 2 mutex, sau đó sửa bằng cách thống nhất thứ tự lấy khoá."],
)

L08 = dict(
  id="notification", short="Task notification", title="Direct-to-task notification", icon="🔔", time="1,5 giờ",
  goal="Dùng notification — cơ chế báo hiệu nhẹ và nhanh nhất của FreeRTOS — thay cho semaphore, event group, mailbox khi chỉ có một task nhận.",
  goals=["Hiểu notification nằm sẵn trong TCB của mỗi task", "Dùng như binary/counting semaphore", "Dùng như event group (bit) và mailbox (ghi đè)"],
  sections=[
    dict(h="Notification thay semaphore", fig=figs.notify_fig(), code="13-notify-semaphore.cpp", html="""
<p>Mỗi task có sẵn một giá trị 32 bit + trạng thái “đang chờ”. Bên gửi tác động trực tiếp lên task nhận (cần handle), không qua đối tượng trung gian → <b>nhanh hơn</b> và <b>không tốn RAM</b>. Giới hạn: chỉ <b>một</b> task nhận; không thể “phát” cho nhiều task.</p>""",
         notes=["<code>ulTaskNotifyTake(pdTRUE, ...)</code>: xoá về 0 khi nhận → giống binary semaphore.",
                "<code>ulTaskNotifyTake(pdFALSE, ...)</code>: giảm 1 → giống counting semaphore, 3 ngắt dồn lại được xử lý đủ 3 lần."]),
    dict(h="Notification như event group và mailbox", code="14-notify-bits-mailbox.cpp", html="""
<table class="tbl"><tr><th>eAction trong <code>xTaskNotify</code></th><th>Hành vi</th><th>Tương đương</th></tr>
<tr><td><code>eSetBits</code></td><td>OR bit vào giá trị</td><td>event group</td></tr>
<tr><td><code>eIncrement</code></td><td>tăng 1</td><td>counting semaphore</td></tr>
<tr><td><code>eSetValueWithOverwrite</code></td><td>ghi đè giá trị</td><td>mailbox (chỉ cần giá trị mới nhất)</td></tr>
<tr><td><code>eSetValueWithoutOverwrite</code></td><td>chỉ ghi nếu giá trị cũ đã được đọc</td><td>queue 1 phần tử</td></tr></table>""",
         notes=["Hai sự kiện Nút + Pin yếu tới gần như cùng lúc được gộp thành bits = 0x6 trong một lần nhận.",
                "Mailbox: LCD chậm chỉ hiển thị giá trị mới nhất (288, 296), các giá trị trung gian bị ghi đè — đúng ý muốn."]),
  ],
  embedded=["ESP-IDF dùng notification rất nhiều trong driver. Trên ESP32 Arduino: <code>xTaskNotifyGive(handle)</code> từ task, <code>vTaskNotifyGiveFromISR</code> từ ngắt.",
            "Chọn: chỉ 1 task nhận → notification; nhiều task cùng chờ → semaphore/event group; cần đệm nhiều dữ liệu → queue."],
  mistakes=["Gửi notification trước khi có handle của task nhận (handle còn NULL).", "Dùng notification khi có nhiều task cần nhận cùng sự kiện."],
  exercises=["Viết lại bài 08 (nút nhấn → task) bằng notification thay cho binary semaphore.",
             "Task WiFi, MQTT, SD báo trạng thái về task chính bằng 3 bit; task chính in trạng thái tổng hợp."],
)

L09 = dict(
  id="event-group", short="Event group", title="Event group – chờ nhiều sự kiện, đồng bộ nhiều task", icon="🎌", time="1,5 giờ",
  goal="Chờ tổ hợp nhiều sự kiện (AND/OR) và đồng bộ nhiều task tại một điểm.",
  goals=["Đặt/xoá/chờ bit với <code>xEventGroupSetBits</code>, <code>xEventGroupWaitBits</code>", "Phân biệt chờ tất cả (AND) và chờ bất kỳ (OR)",
         "Dùng <code>xEventGroupSync</code> để đồng bộ (rendezvous)"],
  sections=[
    dict(h="Event group", fig=figs.event_group(), code="15-event-group.cpp", html="""
<p>Event group là tập các bit sự kiện (24 bit dùng được trên chip 32 bit). Khác notification: <b>nhiều task</b> có thể cùng chờ một event group. Tham số của <code>xEventGroupWaitBits</code>: bit cần chờ, có xoá bit khi thoát không, chờ tất cả hay bất kỳ, timeout.</p>""",
         notes=["Ứng dụng chỉ chạy khi cả WiFi, SD, cảm biến đều sẵn sàng (301 ms) — dù chúng xong theo thứ tự khác nhau.",
                "<code>xEventGroupSync</code>: ba động cơ hiệu chỉnh xong ở 871/941/1011 ms nhưng cùng XUẤT PHÁT lúc 1011 ms."]),
  ],
  embedded=["ESP-IDF dùng event group cho WiFi: <code>WIFI_CONNECTED_BIT</code>, <code>WIFI_FAIL_BIT</code> — ví dụ station chuẩn chờ bằng <code>xEventGroupWaitBits</code>.",
            "Không đặt bit từ ISR trực tiếp: dùng <code>xEventGroupSetBitsFromISR</code> (nó chuyển việc cho timer daemon)."],
  mistakes=["Quên xoá bit sau khi xử lý → task chạy lặp vô hạn.", "Dùng nhiều hơn 24 bit trên chip 32 bit."],
  exercises=["Hệ thống tưới: chỉ bơm khi (đất khô) AND (có nước trong bồn) AND NOT (đang mưa).",
             "Đồng bộ 4 task đọc 4 cảm biến để lấy mẫu cùng một thời điểm."],
)

L10 = dict(
  id="stream-message", short="Stream & message buffer", title="Stream buffer và message buffer", icon="🌊", time="1,5 giờ",
  goal="Truyền dòng byte (UART, âm thanh) và thông điệp độ dài thay đổi từ ngắt tới task, giữa hai nhân CPU.",
  goals=["Dùng stream buffer cho dữ liệu byte liên tục, hiểu trigger level", "Dùng message buffer cho thông điệp có độ dài thay đổi",
         "Biết giới hạn: một bên ghi, một bên đọc"],
  sections=[
    dict(h="Stream buffer: ISR → task", fig=figs.stream_vs_message(), code="16-stream-buffer.cpp", html="""
<p>Stream buffer chuyên chở <b>dòng byte</b>: ghi bao nhiêu byte cũng được, đọc bao nhiêu tuỳ ý. <b>Trigger level</b>: task đang chờ chỉ được đánh thức khi buffer có ít nhất N byte — giảm số lần chuyển ngữ cảnh.</p>""",
         notes=["Ngắt UART mỗi 10 ms đẩy 4 byte; task được đánh thức theo khối 12 byte (trigger level).",
                "Khối đầu chỉ 4 byte vì dữ liệu đã có sẵn khi task gọi receive; khối cuối 6 byte nhận được sau khi chờ hết timeout 200 ms.",
                "Task tự ghép byte thành câu NMEA hoàn chỉnh khi gặp ký tự xuống dòng."]),
    dict(h="Message buffer: thông điệp nguyên vẹn", code="17-message-buffer.cpp", html="""
<p>Message buffer xây trên stream buffer, mỗi thông điệp được lưu kèm độ dài (<code>sizeof(size_t)</code> byte) → bên nhận luôn nhận <b>trọn một</b> thông điệp. FreeRTOS gợi ý dùng message buffer để trao đổi dữ liệu <b>giữa hai nhân</b> trên chip đa nhân không đối xứng (AMP).</p>""",
         notes=["4 lệnh có độ dài 6, 8, 39, 4 byte được nhận nguyên vẹn đúng thứ tự.",
                "Buffer 200 byte còn trống 111 byte sau 4 thông điệp (57 byte dữ liệu + 4 × 8 byte độ dài)."]),
  ],
  embedded=["Nhận dữ liệu GPS, RS485/Modbus, mic I2S: ISR/DMA ghi vào stream buffer, task xử lý.",
            "Chỉ đúng MỘT task/ISR ghi và MỘT task đọc; nhiều bên ghi phải tự bảo vệ bằng vùng găng/mutex."],
  mistakes=["Nhiều task cùng ghi vào một stream buffer không bảo vệ.", "Đọc message buffer với bộ đệm nhỏ hơn thông điệp → không lấy được gì."],
  exercises=["Mô phỏng nhận lệnh AT qua UART bằng stream buffer, tách theo <code>\\r\\n</code>.",
             "Gửi các gói dữ liệu cảm biến độ dài khác nhau (có/không có GPS) qua message buffer."],
)

L11 = dict(
  id="software-timer", short="Software timer", title="Software timer", icon="⏲", time="1,5 giờ",
  goal="Gọi hàm sau một khoảng thời gian hoặc định kỳ mà không cần tạo task riêng.",
  goals=["Hiểu timer daemon task và hàng đợi lệnh timer", "Tạo timer one-shot và auto-reload, dùng timer ID",
         "Đổi chu kỳ, dừng, reset timer — mẫu “timeout không hoạt động”"],
  sections=[
    dict(h="Timer daemon và các loại timer", fig=figs.timer_daemon(), code="18-software-timer.cpp", html="""
<p>Software timer không chạy trong ngắt: mọi callback được gọi bởi <b>timer daemon task</b> (“Tmr Svc”). Lệnh <code>xTimerStart/Stop/Reset/ChangePeriod</code> được gửi qua <b>timer command queue</b>. Cấu hình: <code>configUSE_TIMERS</code>, <code>configTIMER_TASK_PRIORITY</code>, <code>configTIMER_QUEUE_LENGTH</code>, <code>configTIMER_TASK_STACK_DEPTH</code>.</p>
<table class="tbl"><tr><th>Loại</th><th>Hành vi</th><th>Ví dụ</th></tr>
<tr><td>One-shot</td><td>gọi callback một lần</td><td>tắt bơm sau 5 phút, timeout kết nối</td></tr>
<tr><td>Auto-reload</td><td>gọi lặp lại theo chu kỳ</td><td>nháy LED, gửi heartbeat, lấy mẫu chậm</td></tr></table>""",
         notes=["Callback chạy trong task “Tmr Svc” — được in ra bằng <code>pcTaskGetName(NULL)</code>.",
                "Timer ID lưu bộ đếm riêng cho từng timer (đếm ngược 3, 2, 1, 0).",
                "Callback không được chặn: không <code>vTaskDelay</code>, không chờ queue lâu — nếu không mọi timer khác cũng bị trễ."]),
    dict(h="Reset timer: timeout không hoạt động", code="19-timer-reset.cpp", html="<p><code>xTimerReset</code> khởi động lại thời gian đếm. Mỗi thao tác của người dùng gọi reset → timer chỉ hết hạn khi người dùng ngừng thao tác đủ lâu. Đây là cách làm tắt đèn nền, chế độ ngủ, đăng xuất tự động.</p>",
         notes=["Các lần nhấn 100/600/1100/1500 ms liên tục đẩy lùi thời điểm tắt; đèn chỉ tắt lúc 2501 ms = 1500 + 1000."]),
  ],
  embedded=["ESP32 Arduino cũng có <code>esp_timer</code> (độ phân giải µs) và lớp <code>Ticker</code> — software timer của FreeRTOS phù hợp khi độ phân giải ms là đủ.",
            "Dùng timer one-shot làm watchdog mềm: mỗi lần nhận gói tin thì reset; hết hạn = mất kết nối."],
  mistakes=["Gọi hàm chặn trong callback.", "Đặt ưu tiên timer daemon quá thấp → callback bị trễ.", "Gọi <code>xTimerStart</code> trong ISR (phải dùng bản FromISR)."],
  exercises=["Nút nhấn giữ 2 giây mới bật thiết bị (dùng one-shot timer khi nhấn, dừng khi nhả).",
             "Chống dội nút bằng software timer 30 ms."],
)

L12 = dict(
  id="nang-cao-du-an", short="Nâng cao & dự án", title="Queue set, chủ đề nâng cao và dự án tổng hợp", icon="🏁", time="3 giờ",
  goal="Hoàn thiện kiến thức (queue set, quản lý bộ nhớ, co-routine, MPU, chất lượng mã) và ghép tất cả vào một firmware hoàn chỉnh.",
  goals=["Chờ đồng thời nhiều queue/semaphore bằng queue set", "Chọn mô hình heap (heap_1…heap_5)", "Biết co-routine, MPU, tiêu chuẩn chất lượng và quy ước code của FreeRTOS",
         "Thiết kế kiến trúc task cho một dự án thật"],
  sections=[
    dict(h="Queue set", code="20-queue-set.cpp", html="<p>Queue set cho phép một task chờ trên <b>nhiều</b> queue/semaphore cùng lúc và biết cái nào vừa có dữ liệu (<code>xQueueSelectFromSet</code>). Tuy vậy FreeRTOS khuyên ưu tiên thiết kế đơn giản hơn (gộp về một queue chứa struct có trường “nguồn”).</p>",
         notes=["Dữ liệu từ 3 nguồn khác nhau được xử lý đúng thứ tự thời gian tới."]),
    dict(h="Quản lý bộ nhớ, co-routine, MPU, chất lượng", html="""
<table class="tbl"><tr><th>Mô hình heap</th><th>Đặc điểm</th><th>Dùng khi</th></tr>
<tr><td>heap_1</td><td>chỉ cấp phát, không giải phóng</td><td>hệ thống tạo mọi thứ lúc khởi động (an toàn nhất)</td></tr>
<tr><td>heap_2</td><td>có giải phóng, không gộp khối trống (cũ)</td><td>ít dùng</td></tr>
<tr><td>heap_3</td><td>bọc malloc/free của thư viện C</td><td>đã có malloc an toàn luồng</td></tr>
<tr><td><b>heap_4</b></td><td>có giải phóng + gộp khối trống</td><td><b>phổ biến nhất</b> (khóa này dùng)</td></tr>
<tr><td>heap_5</td><td>như heap_4, trải trên nhiều vùng RAM rời rạc</td><td>chip có RAM trong + RAM ngoài</td></tr></table>
<ul>
<li><b>Co-routine</b>: dạng “task” siêu nhẹ dùng chung một stack, dành cho chip cực ít RAM; đã lỗi thời và bị loại bỏ trong các bản FreeRTOS mới — thay bằng task + notification.</li>
<li><b>FreeRTOS-MPU</b>: dùng bộ bảo vệ bộ nhớ của Cortex-M để task chỉ truy cập vùng nhớ được phép (task “không đặc quyền”), lỗi một task không làm hỏng cả hệ thống.</li>
<li><b>Chất lượng</b>: kernel tuân thủ phần lớn <b>MISRA C</b>, có bộ kiểm thử phủ mã; bản <b>SAFERTOS</b> được chứng nhận IEC 61508 SIL3 cho ứng dụng an toàn.</li>
<li><b>Quy ước code</b>: tiền tố kiểu trong tên biến (<code>x</code> BaseType_t/struct, <code>ul</code> uint32_t, <code>pv</code> void*, <code>pc</code> char*), tên hàm có tiền tố file (<code>xTaskCreate</code> trong tasks.c, <code>vQueueDelete</code> trong queue.c) và kiểu trả về (<code>v</code> void, <code>x</code> BaseType_t, <code>pv</code> con trỏ).</li></ul>"""),
    dict(h="Dự án: firmware trạm thời tiết đa nhiệm", fig=figs.project_arch(), figcap="Kiến trúc task và cơ chế liên lạc của dự án.", code="21-du-an-tram-thoi-tiet.cpp", html="""
<p>Dự án dùng gần như mọi cơ chế của khóa: task chu kỳ (<code>vTaskDelayUntil</code>), queue, mutex, event group, task notification từ ngắt, software timer auto-reload và one-shot.</p>""",
         notes=["Cảnh báo bật khi nhiệt độ trung bình 3 mẫu ≥ 31.0 °C và nhắc lại mỗi 400 ms cho tới khi hết quá nhiệt.",
                "Nút MODE (ngắt) đổi màn hình giữa nhiệt độ và độ ẩm mà không làm gián đoạn việc lấy mẫu.",
                "Bảng cuối cho thấy mọi task đều đang Blocked (B) — hệ thống phần lớn thời gian ngủ, CPU rảnh để tiết kiệm năng lượng."]),
  ],
  summary=["Task + ưu tiên + chờ sự kiện thay cho delay → hệ thống phản hồi đúng hạn.",
           "Truyền dữ liệu: queue (nhiều phần tử), stream/message buffer (byte/thông điệp), notification mailbox (giá trị mới nhất).",
           "Báo hiệu: notification (1 task nhận) → semaphore → event group (nhiều sự kiện / nhiều task).",
           "Bảo vệ tài nguyên: mutex (có kế thừa ưu tiên), vùng găng ngắn.", "Hẹn giờ: software timer thay vì tạo task chỉ để chờ."],
  exercises=["Mở rộng dự án: thêm task gửi dữ liệu MQTT mỗi 5 giây, dùng mutex bảo vệ WiFi.",
             "Port dự án lên ESP32 thật với DHT22, LCD I2C, nút nhấn, còi.",
             "Đo stack high water mark của mọi task và chỉnh lại kích thước stack."],
  refs=[("FreeRTOS API reference", "https://www.freertos.org/Documentation/02-Kernel/04-API-references/01-Task-creation/00-TaskHandle"),
        ("ESP-IDF FreeRTOS", "https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos.html")],
)

GROUPS = [
    ("co-ban", "Nền tảng RTOS", "Khái niệm, task, lập lịch", [L01, L02, L03, L04]),
    ("lien-lac", "Liên lạc & đồng bộ", "Queue, semaphore, mutex, notification, event group", [L05, L06, L07, L08, L09]),
    ("nang-cao", "Nâng cao & dự án", "Buffer, timer, queue set, dự án tổng hợp", [L10, L11, L12]),
]
