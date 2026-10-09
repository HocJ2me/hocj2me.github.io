# -*- coding: utf-8 -*-
"""Bài 1–9: nền tảng C++, con trỏ, tham chiếu, struct."""
import figs

L01 = dict(
  id="gioi-thieu", short="Giới thiệu & cài đặt", title="Giới thiệu C++, cài đặt và quá trình build", icon="🚀", time="2 giờ",
  goal="Hiểu C++ là gì, vì sao dùng cho lập trình nhúng, cài môi trường và viết – biên dịch – chạy chương trình đầu tiên.",
  goals=["Biết C++ ra đời thế nào và được dùng ở đâu", "Cài được trình biên dịch và chạy chương trình đầu tiên",
         "Hiểu 4 bước biến mã nguồn thành chương trình chạy được", "Nắm cú pháp cơ bản: câu lệnh, khối lệnh, chú thích, hàm main"],
  sections=[
    dict(h="C++ là gì?", html="""
<p><b>C++</b> do Bjarne Stroustrup phát triển từ năm 1979 tại Bell Labs, ban đầu tên là “C with Classes” — tức ngôn ngữ C cộng thêm lập trình hướng đối tượng. C++ là ngôn ngữ <b>biên dịch</b> (compiled): mã nguồn được dịch một lần thành mã máy, nên chạy rất nhanh và kiểm soát được từng byte bộ nhớ.</p>
<table class="tbl"><tr><th>Phiên bản</th><th>Năm</th><th>Điểm mới đáng chú ý</th></tr>
<tr><td>C++98/03</td><td>1998</td><td>Chuẩn đầu tiên, STL</td></tr>
<tr><td><b>C++11</b></td><td>2011</td><td><code>auto</code>, lambda, <code>nullptr</code>, con trỏ thông minh, <code>std::thread</code> — “C++ hiện đại”</td></tr>
<tr><td>C++14</td><td>2014</td><td>Số nhị phân <code>0b1010</code>, dấu phân cách <code>1'000'000</code></td></tr>
<tr><td><b>C++17</b></td><td>2017</td><td><code>std::optional</code>, <code>std::variant</code>, structured binding — <b>khóa học dùng chuẩn này</b></td></tr>
<tr><td>C++20/23</td><td>2020+</td><td>concepts, ranges, modules</td></tr></table>
<div class="grid3">
<div class="card"><h5>🔌 Lập trình nhúng</h5><p>Arduino, ESP32, STM32, Raspberry Pi Pico đều lập trình bằng C/C++.</p></div>
<div class="card"><h5>🎮 Game & đồ hoạ</h5><p>Unreal Engine, các engine game, phần mềm đồ hoạ 3D.</p></div>
<div class="card"><h5>⚙️ Hệ thống</h5><p>Trình duyệt, hệ điều hành, cơ sở dữ liệu, robot (ROS), AI (TensorFlow lõi C++).</p></div>
</div>"""),
    dict(h="Cài đặt môi trường", html="""
<table class="tbl"><tr><th>Hệ điều hành</th><th>Trình biên dịch</th><th>Kiểm tra</th></tr>
<tr><td>Windows</td><td>MSYS2 → <code>pacman -S mingw-w64-ucrt-x86_64-gcc</code>, hoặc Visual Studio Community</td><td rowspan="3"><code>g++ --version</code></td></tr>
<tr><td>macOS</td><td><code>xcode-select --install</code> (clang++)</td></tr>
<tr><td>Linux</td><td><code>sudo apt install g++</code></td></tr></table>
<p>Trình soạn thảo gợi ý: <b>VS Code</b> + extension C/C++. Với vi điều khiển: <b>Arduino IDE</b> hoặc <b>PlatformIO</b> (trong VS Code). Không muốn cài gì: dùng <a href="https://godbolt.org" target="_blank" rel="noopener">godbolt.org</a> hoặc <a href="https://www.onlinegdb.com" target="_blank" rel="noopener">onlinegdb.com</a>.</p>"""),
    dict(h="Chương trình đầu tiên", code="01-hello.cpp", notes=[
      "<code>#include &lt;iostream&gt;</code> chèn thư viện vào/ra. Dòng bắt đầu bằng <code>#</code> do <b>bộ tiền xử lý</b> xử lý trước khi biên dịch.",
      "<code>int main()</code> là điểm bắt đầu của mọi chương trình C++ trên máy tính. Trên Arduino, <code>main()</code> được viết sẵn và gọi <code>setup()</code> một lần rồi <code>loop()</code> mãi mãi.",
      "<code>std::cout &lt;&lt; ...</code> in ra màn hình; <code>std::endl</code> hoặc <code>\"\\n\"</code> để xuống dòng. <code>std::</code> là namespace của thư viện chuẩn.",
      "Mỗi câu lệnh kết thúc bằng <code>;</code>. Chú thích một dòng <code>//</code>, nhiều dòng <code>/* ... */</code>.",
      "<code>return 0;</code> báo cho hệ điều hành chương trình kết thúc thành công.",
    ]),
    dict(h="C++ được build như thế nào?", fig=figs.build_pipeline(), figcap="Bốn bước từ mã nguồn tới chương trình chạy được.", html="""
<ol>
<li><b>Tiền xử lý</b> (preprocessor): thay <code>#include</code> bằng nội dung file, thay các <code>#define</code>, xử lý <code>#if</code>.</li>
<li><b>Biên dịch</b> (compile): kiểm tra cú pháp, kiểu dữ liệu, dịch sang hợp ngữ. <b>Lỗi biên dịch</b> (thiếu <code>;</code>, sai kiểu…) xuất hiện ở bước này.</li>
<li><b>Hợp dịch</b> (assemble): hợp ngữ → mã máy, tạo file đối tượng <code>.o</code>.</li>
<li><b>Liên kết</b> (link): ghép các file <code>.o</code> và thư viện thành một chương trình. Lỗi “undefined reference” xuất hiện ở bước này (khai báo hàm nhưng quên định nghĩa).</li>
</ol>
<p>Dự án lớn có nhiều file: <code>g++ main.cpp cambien.cpp -o app</code>. Mỗi file <code>.cpp</code> được biên dịch riêng rồi liên kết lại; file <code>.h</code> chứa <b>khai báo</b> để các file khác biết hàm/lớp tồn tại.</p>"""),
  ],
  embedded=["Arduino IDE thực hiện đúng 4 bước trên khi bạn bấm Verify/Upload, dùng trình biên dịch chéo <code>avr-g++</code> (Uno) hoặc <code>xtensa-esp32-elf-g++</code> (ESP32).",
            "Kết quả là file <code>.hex</code>/<code>.bin</code> nạp vào bộ nhớ Flash của chip qua USB-UART.",
            "Khác máy tính: chương trình nhúng <b>không bao giờ kết thúc</b> — <code>loop()</code> chạy mãi tới khi mất điện."],
  mistakes=["Quên dấu <code>;</code> cuối câu lệnh → lỗi biên dịch báo ở dòng KẾ TIẾP.",
            "Viết <code>Main()</code> hoặc <code>main</code> sai chính tả → lỗi liên kết “undefined reference to main”.",
            "Quên <code>std::</code> trước <code>cout</code> mà không có <code>using</code>."],
  exercises=["Viết chương trình in tên, lớp và sở thích của bạn trên 3 dòng.",
             "Chạy <code>g++ -E 01-hello.cpp | wc -l</code> để xem sau tiền xử lý file dài bao nhiêu dòng. Giải thích vì sao.",
             "Cố tình xoá một dấu <code>;</code> và đọc thông báo lỗi của trình biên dịch."],
  refs=[("Lộ trình C++ (vietjack)", "https://vietjack.com/cplusplus/"), ("cppreference.com", "https://en.cppreference.com/w/cpp")],
)

L02 = dict(
  id="kieu-du-lieu", short="Kiểu dữ liệu & biến", title="Kiểu dữ liệu, biến, phạm vi, hằng và modifier", icon="🔢", time="2 giờ",
  goal="Biết chọn đúng kiểu dữ liệu cho từng loại giá trị, hiểu phạm vi sống của biến và cách khai báo hằng.",
  goals=["Phân biệt các kiểu số nguyên, số thực, ký tự, logic và kích thước của chúng",
         "Dùng kiểu cố định độ rộng <code>uint8_t</code>, <code>int16_t</code>… như dân nhúng",
         "Hiểu biến cục bộ, toàn cục, phạm vi khối", "Khai báo hằng bằng <code>const</code>/<code>constexpr</code>, viết literal hệ 2/8/16"],
  sections=[
    dict(h="Các kiểu dữ liệu cơ bản", fig=figs.type_sizes(), figcap="Kích thước phổ biến trên máy tính 32/64 bit và ESP32/STM32.", html="""
<table class="tbl"><tr><th>Kiểu</th><th>Dùng cho</th><th>Ví dụ</th></tr>
<tr><td><code>bool</code></td><td>đúng/sai</td><td><code>bool denBat = true;</code></td></tr>
<tr><td><code>char</code></td><td>một ký tự (thực chất là số 8 bit)</td><td><code>char lenh = 'F';</code></td></tr>
<tr><td><code>int</code>, <code>short</code>, <code>long</code>, <code>long long</code></td><td>số nguyên</td><td><code>int dem = 0;</code></td></tr>
<tr><td><code>float</code>, <code>double</code></td><td>số thực (có sai số)</td><td><code>float t = 28.5f;</code></td></tr>
<tr><td><code>void</code></td><td>“không có kiểu” (hàm không trả về)</td><td><code>void setup()</code></td></tr></table>
<div class="callout warn">⚠️ Kích thước <code>int</code> <b>phụ thuộc phần cứng</b>: 2 byte trên Arduino Uno (AVR 8 bit), 4 byte trên ESP32/PC. Vì vậy code nhúng dùng kiểu trong <code>&lt;cstdint&gt;</code>: <code>uint8_t</code>, <code>int16_t</code>, <code>uint32_t</code>… luôn đúng số bit trên mọi chip.</div>"""),
    dict(h="Ví dụ: kích thước, giới hạn, tràn số", code="02a-kieu-du-lieu.cpp", notes=[
      "<code>std::numeric_limits&lt;T&gt;::max()</code> cho biết giá trị lớn nhất của kiểu <code>T</code>.",
      "Dấu <code>+</code> trước biến <code>uint8_t</code> để in ra <b>số</b>; nếu không, <code>cout</code> coi nó là ký tự.",
      "<b>Tràn số</b>: <code>uint8_t</code> chỉ chứa 0–255, nên 255 + 1 quay vòng về 0 — lỗi kinh điển khi đếm xung, đếm thời gian.",
      "Số thực lưu dạng nhị phân nên <code>0.1 + 0.2</code> không đúng bằng <code>0.3</code>. So sánh số thực bằng sai số nhỏ (xem bài 5).",
    ]),
    dict(h="Biến, phạm vi, hằng, literal và modifier", html="""
<ul>
<li><b>Biến</b> là một vùng nhớ có tên và kiểu. Khai báo: <code>kiểu tên = giá_trị;</code>. Luôn khởi tạo — biến cục bộ chưa khởi tạo chứa “rác”.</li>
<li><b>Phạm vi (scope)</b>: biến khai báo trong <code>{ }</code> chỉ sống trong khối đó (cục bộ); khai báo ngoài mọi hàm là toàn cục.</li>
<li><b>Hằng</b>: <code>const</code> (không đổi sau khi khởi tạo) và <code>constexpr</code> (tính được ngay lúc biên dịch → không tốn RAM, rất hợp cho số chân, tốc độ baud).</li>
<li><b>Literal</b>: <code>255</code>, <code>0xFF</code> (hệ 16), <code>0b11111111</code> (hệ 2), <code>0377</code> (hệ 8), <code>3.14f</code>, <code>'A'</code>, <code>"chuỗi"</code>, <code>1'000'000UL</code>.</li>
<li><b>Modifier</b>: <code>signed</code>/<code>unsigned</code> (có/không dấu), <code>short</code>/<code>long</code> (ngắn/dài).</li>
</ul>""", code="02b-bien-hang.cpp", notes=[
      "Biến <code>cucBo</code> được tạo lại mỗi lần gọi hàm nên luôn bằng 1; biến toàn cục <code>soLanKhoiDong</code> giữ giá trị.",
      "Đặt tên biến trong khối trùng với biến bên ngoài (shadowing) là hợp lệ nhưng rất dễ gây nhầm lẫn.",
      "<code>unsigned 0 - 1</code> thành 4 294 967 295 — đây là lỗi hay gặp khi đếm lùi với biến không dấu.",
      "<code>auto</code> để trình biên dịch tự suy kiểu: <code>28.5</code> là <code>double</code> (8 byte), muốn <code>float</code> phải viết <code>28.5f</code>.",
    ]),
  ],
  embedded=["Dùng <code>uint8_t</code> cho giá trị 0–255 (PWM, độ sáng, byte giao tiếp), <code>uint16_t</code> cho ADC (10–12 bit), <code>uint32_t</code> cho <code>millis()</code>.",
            "Trên AVR, <code>double</code> chỉ là <code>float</code> 4 byte; ESP32 có FPU cho <code>float</code> nhưng <code>double</code> chạy chậm hơn nhiều.",
            "Hằng nên khai báo <code>constexpr</code>/<code>const</code> thay vì biến thường để trình biên dịch đặt vào Flash, tiết kiệm RAM."],
  mistakes=["Dùng <code>int</code> để chứa <code>millis()</code> trên Arduino Uno → tràn sau 32 giây.",
            "So sánh <code>float</code> bằng <code>==</code>.", "Viết <code>0123</code> tưởng là 123 nhưng thực ra là số hệ 8 (= 83)."],
  exercises=["Khai báo biến phù hợp cho: nhiệt độ (có số lẻ), số lần nhấn nút, độ sáng LED 0–255, trạng thái relay.",
             "Viết chương trình chứng minh <code>int16_t</code> 32767 + 1 thành bao nhiêu.",
             "Đổi 0b10110011 sang hệ 10 và hệ 16 bằng tay rồi kiểm tra bằng chương trình."],
)

L03 = dict(
  id="toan-tu", short="Lớp lưu trữ & toán tử", title="Lớp lưu trữ và toán tử (đặc biệt là toán tử bit)", icon="➗", time="2 giờ",
  goal="Hiểu static/extern/volatile và dùng thành thạo mọi nhóm toán tử, nhất là thao tác bit trên thanh ghi.",
  goals=["Phân biệt biến tự động, <code>static</code>, <code>extern</code>, <code>volatile</code>, <code>mutable</code>",
         "Nắm toán tử số học, so sánh, logic, gán, ba ngôi", "Đặt, xoá, đảo, đọc bit bằng <code>| &amp; ^ ~ &lt;&lt; &gt;&gt;</code>"],
  sections=[
    dict(h="Lớp lưu trữ (storage class)", html="""
<table class="tbl"><tr><th>Từ khoá</th><th>Ý nghĩa</th><th>Khi nào dùng</th></tr>
<tr><td>(mặc định)</td><td>biến tự động, sống trong khối</td><td>hầu hết biến cục bộ</td></tr>
<tr><td><code>static</code> trong hàm</td><td>khởi tạo 1 lần, giữ giá trị giữa các lần gọi</td><td>đếm số lần gọi, trạng thái trước của nút nhấn</td></tr>
<tr><td><code>static</code> ngoài hàm</td><td>chỉ thấy trong file .cpp hiện tại</td><td>giấu biến/hàm nội bộ của một module</td></tr>
<tr><td><code>extern</code></td><td>khai báo biến được định nghĩa ở file khác</td><td>chia sẻ biến toàn cục giữa nhiều file</td></tr>
<tr><td><code>mutable</code></td><td>cho phép sửa trong hàm <code>const</code></td><td>bộ đếm, cache bên trong lớp</td></tr>
<tr><td><code>thread_local</code></td><td>mỗi luồng một bản</td><td>chương trình đa luồng</td></tr></table>
<div class="callout">💡 <b>volatile</b> không phải lớp lưu trữ nhưng cực kỳ quan trọng trong nhúng: báo cho trình biên dịch rằng biến có thể bị thay đổi “sau lưng” chương trình (bởi ngắt, DMA, phần cứng), nên phải đọc lại bộ nhớ mỗi lần dùng, không được tối ưu bỏ qua.</div>""",
         code="03a-lop-luu-tru.cpp", notes=[
      "<code>lanGoi</code> là <code>static</code> cục bộ: lần gọi thứ 3 đã là 3, trong khi <code>tam</code> luôn là 1.",
      "Biến dùng chung giữa hàm ngắt (ISR) và <code>loop()</code> phải khai báo <code>volatile</code>.",
    ]),
    dict(h="Toán tử", fig=figs.register_bits(), figcap="Bốn thao tác bit cơ bản — nền tảng của mọi driver phần cứng.", html="""
<table class="tbl"><tr><th>Nhóm</th><th>Toán tử</th><th>Ghi chú</th></tr>
<tr><td>Số học</td><td><code>+ - * / % ++ --</code></td><td>chia hai số nguyên sẽ bỏ phần lẻ</td></tr>
<tr><td>So sánh</td><td><code>== != &lt; &gt; &lt;= &gt;=</code></td><td>kết quả là <code>bool</code></td></tr>
<tr><td>Logic</td><td><code>&amp;&amp; || !</code></td><td>tính “ngắn mạch” (short-circuit)</td></tr>
<tr><td>Bit</td><td><code>&amp; | ^ ~ &lt;&lt; &gt;&gt;</code></td><td>làm việc trên từng bit</td></tr>
<tr><td>Gán</td><td><code>= += -= *= /= |= &amp;= ^= &lt;&lt;=</code></td><td></td></tr>
<tr><td>Khác</td><td><code>?:</code> <code>sizeof</code> <code>,</code> <code>-&gt;</code> <code>::</code></td><td>ba ngôi: <code>đk ? a : b</code></td></tr></table>""",
         code="03b-toan-tu.cpp", notes=[
      "<code>i++</code> dùng giá trị cũ rồi mới tăng; <code>++i</code> tăng trước. Tránh dùng cả hai trên cùng biến trong một biểu thức.",
      "<code>(1 &lt;&lt; 5)</code> tạo “mặt nạ” chỉ có bit 5 bằng 1. <code>|=</code> bật, <code>&amp;= ~</code> tắt, <code>^=</code> đảo.",
      "<code>giaTri &gt;&gt; 8</code> và <code>giaTri &amp; 0xFF</code> tách một số 16 bit thành 2 byte để gửi qua UART/I2C.",
      "Toán tử <code>==</code> ưu tiên cao hơn <code>&amp;</code>, nên phải viết <code>(reg &amp; 4) == 4</code>.",
    ]),
  ],
  embedded=["Trên AVR: <code>PORTB |= (1 &lt;&lt; PB5);</code> nhanh hơn <code>digitalWrite(13, HIGH)</code> hàng chục lần.",
            "Trên STM32: <code>GPIOA-&gt;BSRR = (1 &lt;&lt; 5);</code> đặt chân PA5 lên mức cao.",
            "Gói dữ liệu cảm biến 16 bit thường được gửi thành 2 byte: <code>hi = v &gt;&gt; 8; lo = v &amp; 0xFF;</code> và ghép lại: <code>v = (hi &lt;&lt; 8) | lo;</code>."],
  mistakes=["Viết <code>&amp;</code> thay vì <code>&amp;&amp;</code> (và ngược lại) trong điều kiện if.", "Quên <code>volatile</code> cho biến cờ ngắt → vòng lặp chờ cờ không bao giờ thoát khi bật tối ưu.",
            "Dịch bit vượt độ rộng kiểu (<code>1 &lt;&lt; 32</code> với int 32 bit) là hành vi không xác định."],
  exercises=["Viết hàm <code>bool docBit(uint8_t reg, int n)</code>, <code>uint8_t datBit(uint8_t reg, int n)</code>, <code>uint8_t xoaBit(...)</code>.",
             "Ghép 2 byte <code>0x01</code>, <code>0x2C</code> thành số 16 bit và in ra hệ 10.",
             "Dùng toán tử ba ngôi in “Chẵn”/“Lẻ” cho các số từ 1 đến 10."],
)

L04 = dict(
  id="dieu-khien", short="Rẽ nhánh & vòng lặp", title="Câu lệnh rẽ nhánh và vòng lặp", icon="🔀", time="2 giờ",
  goal="Điều khiển luồng chạy của chương trình bằng if/else, switch và các loại vòng lặp — kể cả vòng lặp không chặn kiểu Arduino.",
  goals=["Viết if / else if / else và switch đúng cách", "Chọn đúng for / while / do-while / range-for", "Dùng break, continue",
         "Viết vòng <code>loop()</code> không chặn bằng <code>millis()</code> thay cho <code>delay()</code>"],
  sections=[
    dict(h="Rẽ nhánh: if – else if – else và switch", fig=figs.flow_if(), figcap="Lưu đồ của chuỗi if – else if – else trong ví dụ.", html="""
<p><b>if</b> kiểm tra điều kiện bất kỳ; các nhánh <b>else if</b> được xét lần lượt từ trên xuống, gặp nhánh đúng đầu tiên thì dừng. <b>switch</b> so sánh một giá trị nguyên/ký tự/enum với nhiều hằng — gọn và nhanh hơn chuỗi if khi có nhiều lựa chọn.</p>
<div class="callout warn">⚠️ Mỗi <code>case</code> cần <code>break;</code>. Thiếu break, chương trình “rơi” xuống case tiếp theo (fall-through) — đôi khi cố ý (nhiều case chung xử lý), nhưng thường là lỗi.</div>""",
         code="04a-re-nhanh.cpp", notes=[
      "<code>enum class</code> đặt tên cho các trạng thái — dễ đọc hơn số 0, 1, 2.",
      "C++17 cho phép <code>if (khởi_tạo; điều_kiện)</code> để biến chỉ sống trong if.",
      "<code>if (x = 5)</code> là phép GÁN, luôn đúng. Bật <code>-Wall</code> để trình biên dịch cảnh báo (xem dòng cảnh báo khi biên dịch).",
    ]),
    dict(h="Vòng lặp", fig=figs.millis_timeline(), figcap="delay() làm “đóng băng” chương trình; millis() cho phép làm nhiều việc cùng lúc.", html="""
<table class="tbl"><tr><th>Vòng lặp</th><th>Dùng khi</th></tr>
<tr><td><code>for (khởi tạo; điều kiện; bước)</code></td><td>biết trước số lần lặp</td></tr>
<tr><td><code>while (điều kiện)</code></td><td>lặp tới khi điều kiện sai, có thể không chạy lần nào</td></tr>
<tr><td><code>do { } while (điều kiện);</code></td><td>chạy ít nhất 1 lần (thử kết nối, đọc lại)</td></tr>
<tr><td><code>for (auto x : mang)</code></td><td>duyệt mọi phần tử của mảng/container</td></tr></table>
<p><code>break</code> thoát hẳn vòng lặp, <code>continue</code> bỏ qua phần còn lại của lượt hiện tại.</p>""",
         code="04b-vong-lap.cpp", notes=[
      "Kỹ thuật <b>non-blocking</b>: lưu thời điểm lần cuối làm việc, mỗi vòng kiểm tra <code>now - lanCuoi &gt;= chuKy</code>.",
      "Phép trừ <code>now - lanCuoi</code> với <code>unsigned long</code> vẫn đúng ngay cả khi <code>millis()</code> tràn số sau 49 ngày.",
      "Vòng lặp lồng nhau: vòng trong chạy hết cho mỗi lượt của vòng ngoài — dùng cho ma trận LED, bản đồ.",
    ]),
  ],
  embedded=["<code>loop()</code> của Arduino chính là một vòng <code>while(true)</code>. Không bao giờ dùng <code>delay()</code> dài khi cần đọc nút nhấn hay cảm biến đồng thời.",
            "Máy trạng thái (state machine) = <code>switch</code> trên biến trạng thái bên trong <code>loop()</code>.",
            "Vòng chờ cờ: <code>while (!coNgat) {}</code> — biến cờ phải là <code>volatile</code>."],
  mistakes=["Dấu <code>;</code> ngay sau <code>if (...)</code> hoặc <code>for (...)</code> làm khối lệnh luôn chạy / chỉ chạy một lần.",
            "Vòng <code>while</code> quên cập nhật biến điều kiện → lặp vô hạn, chip bị watchdog reset.", "Quên <code>break</code> trong <code>switch</code>."],
  exercises=["In bảng cửu chương 2–9 bằng hai vòng for lồng nhau.",
             "Viết chương trình đèn giao thông dùng <code>switch</code>: Xanh 5s → Vàng 2s → Đỏ 5s (giả lập thời gian).",
             "Nháy 2 LED với chu kỳ 300 ms và 700 ms cùng lúc bằng kỹ thuật <code>millis()</code>."],
)

L05 = dict(
  id="ham", short="Hàm & Number", title="Hàm và xử lý số (Number)", icon="🧮", time="2 giờ",
  goal="Chia chương trình thành các hàm rõ ràng; dùng thư viện toán và ép kiểu số đúng cách.",
  goals=["Khai báo, định nghĩa, gọi hàm; tách khai báo vào file .h", "Truyền tham trị, tham chiếu, con trỏ; tham số mặc định; nạp chồng",
         "Viết hàm đệ quy, lambda, constexpr", "Dùng <code>&lt;cmath&gt;</code>, ép kiểu, số ngẫu nhiên, <code>map()</code>/<code>constrain()</code>"],
  sections=[
    dict(h="Hàm", html="""
<p>Hàm gom một nhóm lệnh thành một đơn vị có tên để <b>tái sử dụng</b> và làm code dễ đọc. Cấu trúc: <code>kiểu_trả_về tên(danh_sách_tham_số) { thân hàm }</code>.</p>
<table class="tbl"><tr><th>Cách truyền</th><th>Cú pháp</th><th>Hàm sửa được biến gốc?</th><th>Khi nào dùng</th></tr>
<tr><td>Tham trị</td><td><code>void f(int x)</code></td><td>Không (nhận bản sao)</td><td>kiểu nhỏ: int, float, char</td></tr>
<tr><td>Tham chiếu</td><td><code>void f(int&amp; x)</code></td><td>Có</td><td>cần sửa biến, trả nhiều kết quả</td></tr>
<tr><td>Tham chiếu hằng</td><td><code>void f(const T&amp; x)</code></td><td>Không</td><td>đối tượng lớn (string, struct) — không sao chép</td></tr>
<tr><td>Con trỏ</td><td><code>void f(int* x)</code></td><td>Có</td><td>có thể truyền <code>nullptr</code>; giao tiếp với thư viện C</td></tr></table>""",
         code="05a-ham.cpp", notes=[
      "Khai báo (prototype) ở đầu file cho phép gọi hàm trước khi định nghĩa. Dự án thật đặt khai báo trong file <code>.h</code>.",
      "Tham số mặc định phải nằm ở <b>cuối</b> danh sách tham số.",
      "Hàm đệ quy cần điều kiện dừng; trên MCU stack nhỏ nên tránh đệ quy sâu.",
      "<code>constexpr</code> cho phép trình biên dịch tính sẵn kết quả — <code>adcToMilliVolt(2048)</code> không tốn thời gian chạy.",
      "Dòng cảnh báo “parameter set but not used” là do hàm <code>tangThamTri</code> cố ý sửa bản sao vô ích — đúng thứ ví dụ muốn chứng minh.",
    ]),
    dict(h="Number: thư viện toán và ép kiểu", code="05b-number.cpp", notes=[
      "<code>adc * 33 / 40950</code> toàn số nguyên nên bị cắt phần lẻ trước khi gán vào <code>float</code> — lỗi rất phổ biến khi đổi ADC sang điện áp.",
      "<code>static_cast&lt;int&gt;(9.99)</code> cắt bỏ phần lẻ (9), muốn làm tròn dùng <code>std::lround</code>.",
      "<code>std::mt19937</code> với seed cố định cho dãy giống nhau mỗi lần chạy — tiện kiểm thử. Trên Arduino: <code>randomSeed(analogRead(A0))</code> lấy nhiễu làm seed.",
      "Cảnh báo “division by zero” là do ví dụ cố ý tính <code>1.0 / 0</code> để minh hoạ giá trị <code>inf</code>.",
    ]),
  ],
  embedded=["Hàm <code>map()</code> của Arduino dùng số nguyên nên có sai số làm tròn; <code>constrain()</code> tương đương <code>std::clamp</code>.",
            "Trên chip không có FPU (Arduino Uno), phép tính <code>float</code> rất chậm — ưu tiên số nguyên “nhân 10” (285 thay cho 28.5°C).",
            "Hàm ngắn gọi rất nhiều lần nên khai báo <code>inline</code>/<code>constexpr</code>."],
  mistakes=["Hàm khai báo trả về giá trị nhưng quên <code>return</code> → kết quả rác.", "Truyền <code>std::string</code>/struct lớn bằng tham trị làm chậm và tốn RAM.",
            "Nhầm <code>abs()</code> (số nguyên) với <code>fabs()</code> (số thực)."],
  exercises=["Viết hàm <code>float docNhietDoLM35(int adc)</code> (ADC 10 bit, 5V, 10 mV/°C).",
             "Viết hàm <code>void chuyenDoi(int tongGiay, int&amp; gio, int&amp; phut, int&amp; giay)</code>.",
             "Viết hàm đệ quy tính tổng các chữ số của một số."],
)

L06 = dict(
  id="mang-chuoi", short="Mảng & chuỗi", title="Mảng (Array) và chuỗi (String)", icon="📚", time="2 giờ",
  goal="Lưu nhiều giá trị cùng kiểu bằng mảng, xử lý chuỗi kiểu C và std::string, phân tích lệnh văn bản.",
  goals=["Khai báo, khởi tạo, duyệt mảng 1 và 2 chiều; truyền mảng vào hàm", "Dùng <code>std::array</code> và kỹ thuật bộ đệm vòng",
         "Thao tác chuỗi kiểu C an toàn (<code>snprintf</code>) và <code>std::string</code>", "Phân tích lệnh dạng <code>TEN:GIA_TRI</code>"],
  sections=[
    dict(h="Mảng", fig=figs.array_memory(), figcap="Các phần tử mảng nằm liền nhau trong bộ nhớ; C++ KHÔNG kiểm tra chỉ số vượt giới hạn.", html="""
<p>Mảng là dãy các phần tử <b>cùng kiểu</b>, nằm <b>liên tiếp</b> trong bộ nhớ, đánh chỉ số từ <b>0</b>. Kích thước mảng tĩnh phải biết lúc biên dịch.</p>
<ul><li>Số phần tử: <code>sizeof(a) / sizeof(a[0])</code> (chỉ đúng khi <code>a</code> là mảng thật, không phải con trỏ).</li>
<li>Khi truyền vào hàm, mảng “suy biến” thành con trỏ tới phần tử đầu → phải truyền kèm số phần tử.</li>
<li><code>std::array&lt;T, N&gt;</code> là mảng tĩnh “có văn hoá”: biết kích thước, có <code>.at()</code> kiểm tra chỉ số.</li></ul>""",
         code="06a-mang.cpp", notes=[
      "Khởi tạo thiếu phần tử (<code>int day[5] = {1, 2};</code>) thì phần còn lại tự bằng 0.",
      "Mảng 2 chiều <code>banDo[H][W]</code> duyệt bằng 2 vòng lặp lồng nhau (hàng rồi cột).",
      "Lớp <code>MovingAverage</code> dùng bộ đệm vòng: thay phần tử cũ nhất bằng phần tử mới, cập nhật tổng trong O(1).",
    ], after="<figure class='fig'>" + figs.ring_buffer() + "<figcaption>Bộ đệm vòng: chỉ số quay về 0 khi chạm cuối mảng.</figcaption></figure>"),
    dict(h="Chuỗi", html="""
<div class="grid2">
<div class="card"><h5>Chuỗi kiểu C — <code>char[]</code></h5><p>Mảng ký tự kết thúc bằng <code>'\\0'</code>. Nhẹ, không cấp phát động, dùng nhiều trong nhúng. Hàm trong <code>&lt;cstring&gt;</code>: <code>strlen</code>, <code>strcpy</code>, <code>strcat</code>, <code>strcmp</code>, <code>strchr</code>. Dễ tràn bộ đệm — dùng <code>snprintf</code>.</p></div>
<div class="card"><h5><code>std::string</code></h5><p>Tự quản lý bộ nhớ, có <code>+</code>, <code>find</code>, <code>substr</code>, <code>replace</code>, <code>to_string</code>, <code>stoi</code>. Tiện nhưng cấp phát heap → cẩn thận trên MCU RAM nhỏ (Arduino có lớp <code>String</code> tương tự).</p></div>
</div>""", code="06b-chuoi.cpp", notes=[
      "<code>snprintf</code> không bao giờ ghi quá kích thước bộ đệm và trả về số ký tự <i>cần</i> — dùng để phát hiện bị cắt.",
      "<code>find</code> trả về <code>std::string::npos</code> khi không tìm thấy.",
      "Chuỗi tiếng Việt UTF-8: một chữ có dấu chiếm 2–3 byte, nên <code>length()</code> lớn hơn số chữ nhìn thấy.",
    ]),
  ],
  embedded=["Đọc lệnh từ Serial vào bộ đệm <code>char buf[32]</code> tới khi gặp <code>'\\n'</code>, rồi phân tích — tránh dùng <code>String</code> liên tục gây phân mảnh heap trên Arduino Uno.",
            "Lưu mẫu ADC vào mảng tĩnh để lọc nhiễu, tính trung bình, tìm đỉnh.", "Bảng tra (lookup table) <code>const</code> — ví dụ bảng sin cho PWM — được đặt trong Flash."],
  mistakes=["Truy cập <code>a[n]</code> với mảng n phần tử (chỉ số hợp lệ 0..n-1) — không báo lỗi nhưng ghi đè bộ nhớ khác.",
            "Mảng <code>char</code> thiếu chỗ cho <code>'\\0'</code>: <code>char s[5] = \"Hello\";</code> là lỗi.", "So sánh chuỗi C bằng <code>==</code> (so địa chỉ!) thay vì <code>strcmp</code>."],
  exercises=["Nhập 10 số, in ra số lớn nhất, nhỏ nhất và vị trí của chúng.",
             "Viết hàm đếm số từ trong một câu (các từ cách nhau bởi dấu cách).",
             "Phân tích chuỗi <code>\"T=28.5;H=60;L=320\"</code> thành 3 biến số."],
)

L07 = dict(
  id="con-tro", short="Con trỏ (1)", title="Con trỏ: địa chỉ, con trỏ và con trỏ tới con trỏ", icon="👉", time="2 giờ",
  goal="Hiểu bản chất con trỏ — biến chứa địa chỉ — và dùng để truy cập mảng, truyền tham số, sửa con trỏ của nơi khác.",
  goals=["Dùng <code>&amp;</code> lấy địa chỉ và <code>*</code> truy cập giá trị", "Hiểu số học con trỏ và mối liên hệ con trỏ – mảng",
         "Dùng <code>nullptr</code> và <code>const</code> với con trỏ", "Hiểu và dùng con trỏ tới con trỏ <code>int**</code>"],
  sections=[
    dict(h="Con trỏ là gì?", fig=figs.memory_pointer(), figcap="p lưu địa chỉ của nhietDo; pp lưu địa chỉ của p.", html="""
<p>Mỗi biến nằm ở một <b>địa chỉ</b> trong bộ nhớ. <b>Con trỏ</b> là biến dùng để <b>lưu địa chỉ</b> của biến khác.</p>
<table class="tbl"><tr><th>Cú pháp</th><th>Ý nghĩa</th></tr>
<tr><td><code>int* p;</code></td><td>p là con trỏ tới int</td></tr>
<tr><td><code>p = &amp;x;</code></td><td><code>&amp;</code> lấy <b>địa chỉ</b> của x</td></tr>
<tr><td><code>*p</code></td><td><code>*</code> “đi tới” địa chỉ, lấy <b>giá trị</b> ở đó (dereference)</td></tr>
<tr><td><code>p + 1</code></td><td>địa chỉ phần tử kế tiếp: tăng <code>sizeof(int)</code> byte, không phải 1 byte</td></tr>
<tr><td><code>int** pp = &amp;p;</code></td><td>con trỏ tới con trỏ: <code>**pp == x</code></td></tr></table>"""),
    dict(h="Ví dụ đầy đủ", code="07-con-tro-dia-chi.cpp", notes=[
      "Địa chỉ thật thay đổi mỗi lần chạy nên ví dụ chỉ in <b>khoảng cách</b> và kết quả so sánh — kết quả luôn giống nhau.",
      "Tên mảng <code>adc</code> chính là địa chỉ phần tử đầu; <code>pa[3]</code> tương đương <code>*(pa + 3)</code>.",
      "Hàm <code>hoanDoi(int*, int*)</code> sửa được biến của nơi gọi vì nhận địa chỉ của chúng.",
      "<code>capPhatLai(int** pp, ...)</code> sửa được <b>chính con trỏ</b> của nơi gọi — kỹ thuật này dùng nhiều trong thư viện C (ví dụ hàm cấp phát trả kết quả qua tham số).",
      "<code>const int* p</code>: không sửa giá trị qua p. <code>int* const p</code>: không đổi được địa chỉ p trỏ tới. Đọc từ phải sang trái.",
    ]),
  ],
  embedded=["Driver phần cứng truy cập thanh ghi bằng con trỏ tới địa chỉ cố định (xem bài 8).",
            "Hàm thư viện nhận con trỏ tới bộ đệm: <code>Serial.readBytes(buf, n)</code>, <code>Wire.write(data, len)</code>.",
            "DMA (truyền dữ liệu không cần CPU) được cấu hình bằng địa chỉ nguồn và đích — chính là con trỏ."],
  mistakes=["Dùng con trỏ chưa khởi tạo (trỏ lung tung) → treo chip / HardFault.", "Dereference <code>nullptr</code>.",
            "Trả về địa chỉ biến cục bộ từ hàm — biến đã chết khi hàm kết thúc (dangling pointer)."],
  exercises=["Viết hàm <code>void tinh(int a, int b, int* tong, int* hieu)</code>.",
             "Dùng con trỏ duyệt ngược một mảng và in ra.", "Viết hàm <code>bool timMax(int* a, int n, int** viTri)</code> trả về con trỏ tới phần tử lớn nhất qua tham số."],
)

L08 = dict(
  id="con-tro-2", short="Con trỏ (2)", title="Ép kiểu con trỏ và con trỏ hàm", icon="🎯", time="2 giờ",
  goal="Dùng con trỏ để nhìn dữ liệu ở mức byte (gói tin, thanh ghi, endian) và để truyền hàm như một giá trị (callback).",
  goals=["Chuyển đổi int ↔ char, xem số như dãy byte", "Hiểu little/big endian", "Đóng gói/giải gói struct để truyền qua UART",
         "Truy cập thanh ghi qua con trỏ", "Dùng con trỏ hàm: callback, bảng xử lý lệnh"],
  sections=[
    dict(h="Ép kiểu con trỏ", fig=figs.endian(), figcap="Thứ tự byte trong bộ nhớ — quan trọng khi gửi số nhiều byte giữa hai thiết bị.", html="""
<p>Ép <code>uint32_t*</code> thành <code>uint8_t*</code> cho phép đọc từng byte của một số — nền tảng của việc đóng gói dữ liệu truyền thông. C++ có 4 toán tử ép kiểu rõ ràng thay cho kiểu C <code>(T)x</code>: <code>static_cast</code>, <code>reinterpret_cast</code>, <code>const_cast</code>, <code>dynamic_cast</code>.</p>""",
         code="08a-ep-kieu-con-tro.cpp", notes=[
      "<code>'0' + 7</code> ra ký tự <code>'7'</code>, <code>'9' - '0'</code> ra số 9 — mẹo chuyển chữ số ↔ ký tự.",
      "<code>#pragma pack(1)</code> bỏ byte đệm để struct có đúng 9 byte như giao thức quy định.",
      "Đọc/ghi qua <code>memcpy</code> an toàn hơn ép con trỏ trực tiếp (tránh lỗi căn lề và “strict aliasing”).",
      "<code>reinterpret_cast&lt;GPIO_TypeDef*&gt;(địa_chỉ)</code> là đúng cách thư viện STM32 định nghĩa <code>GPIOA</code>.",
    ]),
    dict(h="Con trỏ hàm", html="""
<p>Hàm cũng có địa chỉ. <b>Con trỏ hàm</b> lưu địa chỉ đó để gọi hàm “gián tiếp”: <code>int (*f)(int, int) = cong; f(3, 4);</code>. Dùng để:</p>
<ul><li><b>Callback</b>: đăng ký hàm sẽ được gọi khi có sự kiện (ngắt, hết giờ, nhận dữ liệu).</li>
<li><b>Bảng xử lý</b>: mảng các cặp (tên lệnh, hàm) thay cho chuỗi <code>if/else</code> dài.</li>
<li>Thuật toán tổng quát: <code>qsort</code> nhận hàm so sánh.</li></ul>""", code="08b-con-tro-ham.cpp", notes=[
      "<code>using HamXuLy = void (*)(int);</code> đặt tên cho kiểu con trỏ hàm — cú pháp gốc rất khó đọc.",
      "Bảng <code>BANG_LENH</code> là <code>const</code> nên được đặt trong Flash; thêm lệnh mới chỉ cần thêm một dòng.",
      "<code>std::function</code> linh hoạt hơn (chứa được lambda có “bắt” biến) nhưng tốn bộ nhớ hơn con trỏ hàm.",
    ]),
  ],
  embedded=["<code>attachInterrupt(digitalPinToInterrupt(2), khiNhanNut, FALLING)</code> nhận con trỏ hàm.",
            "Bảng vector ngắt của vi điều khiển thực chất là <b>mảng con trỏ hàm</b> ở đầu bộ nhớ Flash.",
            "Gửi struct cảm biến qua LoRa/ESP-NOW: đóng gói thành mảng byte, kèm CRC, phía nhận <code>memcpy</code> ngược lại — hai bên phải cùng endian và cùng cách pack."],
  mistakes=["Ép <code>float*</code> thành <code>int*</code> rồi đọc — vi phạm strict aliasing, kết quả sai khi bật tối ưu.",
            "Hai thiết bị khác endian gửi số nhiều byte mà không chuẩn hoá thứ tự.", "Gọi con trỏ hàm <code>nullptr</code>."],
  exercises=["Viết hàm đóng gói <code>uint16_t</code> thành 2 byte theo big endian và hàm giải gói ngược lại.",
             "Thêm lệnh <code>BUZZER</code> vào bảng xử lý lệnh.", "Viết máy tính bỏ túi dùng mảng con trỏ hàm <code>{cong, tru, nhan, chia}</code> chọn theo ký tự toán tử."],
)

L09 = dict(
  id="tham-chieu-struct", short="Tham chiếu, struct, I/O", title="Tham chiếu, cấu trúc (struct), vào/ra và ngày giờ", icon="🧱", time="2 giờ",
  goal="Dùng tham chiếu thay con trỏ khi phù hợp, gom dữ liệu bằng struct, nhập/xuất có định dạng và làm việc với thời gian.",
  goals=["Phân biệt tham chiếu và con trỏ; dùng <code>const&amp;</code>", "Định nghĩa và dùng struct, hiểu padding",
         "Nhập bằng <code>cin</code>, in có định dạng bằng <code>&lt;iomanip&gt;</code>", "Dùng <code>&lt;ctime&gt;</code> và <code>&lt;chrono&gt;</code>"],
  sections=[
    dict(h="Tham chiếu (reference)", html="""
<p>Tham chiếu là <b>tên khác</b> (bí danh) của một biến đã có: <code>int&amp; r = x;</code>. Mọi thao tác trên <code>r</code> chính là trên <code>x</code>.</p>
<table class="tbl"><tr><th></th><th>Con trỏ <code>T*</code></th><th>Tham chiếu <code>T&amp;</code></th></tr>
<tr><td>Có thể rỗng?</td><td>Có (<code>nullptr</code>)</td><td>Không — phải gắn với biến ngay khi tạo</td></tr>
<tr><td>Đổi đối tượng trỏ tới?</td><td>Có</td><td>Không</td></tr>
<tr><td>Cú pháp dùng</td><td><code>*p</code>, <code>p-&gt;x</code></td><td>như biến thường</td></tr></table>""",
         code="09a-tham-chieu.cpp", notes=[
      "<code>const CamBien&amp;</code> là cách truyền đối tượng chuẩn nhất: không sao chép, không sửa.",
      "Vòng <code>for (CamBien c : ds)</code> làm việc trên bản sao; muốn sửa phải viết <code>for (CamBien&amp; c : ds)</code>.",
    ]),
    dict(h="Struct và Input/Output", stdin=open(__import__("os").path.join(__import__("os").path.dirname(__file__), "code", "09b-struct-io.stdin"), encoding="utf-8").read(),
         html="""
<p><b>struct</b> gom nhiều dữ liệu liên quan thành một kiểu mới: <code>struct DiemDo { std::string viTri; float nhietDo; int doAm; };</code>. Truy cập bằng dấu chấm <code>d.nhietDo</code> (hoặc <code>p-&gt;nhietDo</code> qua con trỏ).</p>
<p><b>I/O</b>: <code>std::cin &gt;&gt;</code> đọc từ bàn phím (tách theo khoảng trắng), <code>std::getline</code> đọc cả dòng; <code>&lt;iomanip&gt;</code> có <code>setw</code>, <code>setprecision</code>, <code>fixed</code>, <code>hex</code>, <code>setfill</code>. <code>std::cerr</code> là luồng báo lỗi.</p>""",
         code="09b-struct-io.cpp", notes=[
      "Ô “Dữ liệu nhập” là những gì gõ vào bàn phím; chương trình in lại giá trị để kết quả dễ theo dõi.",
      "Trình biên dịch chèn <b>byte đệm (padding)</b> để căn lề: <code>{char, int, char}</code> chiếm 12 byte, sắp lại <code>{int, char, char}</code> chỉ 8 byte.",
      "<code>setw</code> chỉ áp dụng cho lần in kế tiếp; <code>fixed</code>, <code>setprecision</code>, <code>hex</code> có hiệu lực tới khi đổi.",
    ]),
    dict(h="Ngày và giờ", code="09c-thoi-gian.cpp", notes=[
      "<code>time_t</code> là số giây từ 1/1/1970 (Unix time). <code>gmtime</code> đổi sang ngày giờ UTC; Việt Nam là UTC+7.",
      "<code>&lt;chrono&gt;</code> gắn đơn vị vào số (<code>milliseconds</code>, <code>seconds</code>) — không còn nhầm ms với giây.",
      "<code>steady_clock</code> dùng để đo khoảng thời gian (không bị ảnh hưởng khi chỉnh đồng hồ hệ thống) — tương tự <code>micros()</code>.",
    ]),
  ],
  embedded=["ESP32 đồng bộ giờ qua NTP: <code>configTime(7*3600, 0, \"pool.ntp.org\"); time(&amp;now); localtime_r(&amp;now, &amp;tm);</code> — dùng y hệt bài này.",
            "Module RTC DS3231 lưu giờ khi mất điện; struct là cách tự nhiên để giữ một bản ghi đo đạc (thời gian, nhiệt độ, độ ẩm).",
            "Struct gửi qua mạng nên dùng kiểu cố định độ rộng và <code>#pragma pack</code> (xem bài 8)."],
  mistakes=["Trả về tham chiếu tới biến cục bộ.", "Trộn <code>cin &gt;&gt;</code> và <code>getline</code> mà quên bỏ ký tự xuống dòng còn sót.",
            "Dùng <code>int</code> 16 bit lưu Unix time trên AVR."],
  exercises=["Định nghĩa struct <code>HocSinh</code> (tên, lớp, 3 điểm) và hàm tính điểm trung bình nhận <code>const HocSinh&amp;</code>.",
             "Nhập N bản ghi đo đạc và in bảng căn lề đẹp, kèm dòng tổng kết.", "Tính số ngày còn lại tới sinh nhật của bạn bằng <code>mktime</code>/<code>difftime</code>."],
)

LESSONS = [L01, L02, L03, L04, L05, L06, L07, L08, L09]
