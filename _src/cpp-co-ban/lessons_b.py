# -*- coding: utf-8 -*-
"""Bài 10–17: hướng đối tượng, con trỏ lớp, C++ nâng cao, bài tập tổng hợp."""
import figs

L10 = dict(
  id="lop-doi-tuong", short="Lớp & đối tượng", title="Hướng đối tượng: lớp, đối tượng và tính bao đóng", icon="🏗️", time="2 giờ",
  goal="Mô hình hoá thiết bị phần cứng thành lớp có dữ liệu riêng tư và phương thức công khai; hiểu vòng đời đối tượng và RAII.",
  goals=["Định nghĩa lớp với <code>private</code>/<code>public</code>, constructor, destructor", "Hiểu tính bao đóng và vì sao cần setter có kiểm tra",
         "Dùng thành viên <code>static</code>, hàm <code>const</code>", "Áp dụng RAII; viết/cấm copy constructor"],
  intro="<p>Lập trình hướng đối tượng (OOP) có 4 trụ cột: <b>bao đóng</b> (encapsulation), <b>kế thừa</b> (inheritance), <b>đa hình</b> (polymorphism) và <b>trừu tượng</b> (abstraction). Bài này bắt đầu với lớp, đối tượng và bao đóng.</p>",
  sections=[
    dict(h="Lớp và đối tượng", fig=figs.oop_class(), figcap="Một lớp, nhiều đối tượng — mỗi đối tượng có dữ liệu riêng.", html="""
<ul><li><b>Lớp (class)</b> = bản thiết kế gồm <b>dữ liệu</b> (thuộc tính) và <b>hành vi</b> (phương thức).</li>
<li><b>Đối tượng (object)</b> = một thể hiện cụ thể của lớp.</li>
<li><b>Bao đóng</b>: giấu dữ liệu ở <code>private</code>, chỉ cho truy cập qua phương thức <code>public</code> có kiểm tra → đối tượng luôn ở trạng thái hợp lệ.</li>
<li><b>Constructor</b> chạy khi tạo đối tượng (khởi tạo), <b>destructor</b> <code>~TenLop()</code> chạy khi huỷ (dọn dẹp).</li></ul>
<div class="callout">💡 <code>struct</code> và <code>class</code> trong C++ gần như giống nhau; khác biệt duy nhất là mặc định <code>public</code> (struct) hay <code>private</code> (class). Quy ước: struct cho dữ liệu đơn giản, class cho đối tượng có hành vi.</div>""",
         code="10a-lop-doi-tuong.cpp", notes=[
      "Danh sách khởi tạo <code>: pin_(pin), ten_(...)</code> là cách duy nhất khởi tạo thành viên <code>const</code>.",
      "<code>datDoSang(999)</code> bị từ chối — bên ngoài không thể đưa đối tượng vào trạng thái sai.",
      "<code>static int soLuong</code> dùng chung cho mọi đối tượng — đếm số LED đang tồn tại.",
      "Đối tượng huỷ theo thứ tự <b>ngược</b> với lúc tạo.",
    ]),
    dict(h="RAII và sao chép đối tượng", html="""
<p><b>RAII</b> (Resource Acquisition Is Initialization): chiếm tài nguyên trong constructor, trả trong destructor. Vì destructor <b>luôn</b> được gọi khi đối tượng ra khỏi phạm vi, tài nguyên không bao giờ bị “quên trả” — kể cả khi <code>return</code> sớm hay có ngoại lệ.</p>
<p><b>Quy tắc 3</b>: lớp tự quản lý tài nguyên (con trỏ cấp phát, file, khoá) cần tự viết <i>destructor</i>, <i>copy constructor</i> và <i>operator=</i>; hoặc <b>cấm sao chép</b> bằng <code>= delete</code>.</p>""",
         code="10b-raii-sao-chep.cpp", notes=[
      "Dòng <code>[unlock]</code> vẫn xuất hiện khi hàm <code>return false</code> sớm — đó là sức mạnh của RAII.",
      "Copy constructor sao chép <b>sâu</b>: cấp phát mảng mới, nên sửa <code>b</code> không ảnh hưởng <code>a</code>.",
      "<code>UartPort(const UartPort&amp;) = delete;</code> biến việc sao chép thành lỗi biên dịch.",
    ]),
  ],
  embedded=["Thư viện Arduino đều là lớp: <code>Servo myservo; myservo.attach(9); myservo.write(90);</code>.",
            "Đóng gói mỗi thiết bị (LED, động cơ, cảm biến) thành một lớp giúp code robot gọn và tái sử dụng được.",
            "RAII hợp với khoá mutex (<code>std::lock_guard</code>), tắt/bật ngắt tạm thời, chọn chip SPI (CS xuống khi tạo, lên khi huỷ)."],
  mistakes=["Để thuộc tính <code>public</code> rồi sửa tuỳ tiện ở khắp nơi.", "Quên định nghĩa thành viên <code>static</code> ngoài lớp → lỗi liên kết.",
            "Lớp giữ con trỏ cấp phát nhưng dùng copy mặc định → hai đối tượng cùng <code>delete</code> một vùng nhớ."],
  exercises=["Viết lớp <code>NutNhan</code> có <code>vuaNhan()</code> chỉ trả về true một lần cho mỗi lần nhấn (chống dội phím bằng thời gian).",
             "Viết lớp <code>DongCo</code> với tốc độ trong khoảng -255..255, phương thức <code>tien(v)</code>, <code>lui(v)</code>, <code>dung()</code>.",
             "Viết lớp RAII <code>DoThoiGian</code> in ra thời gian thực thi khối lệnh khi bị huỷ."],
)

L11 = dict(
  id="ke-thua", short="Kế thừa & nạp chồng", title="Tính kế thừa và nạp chồng (overloading)", icon="🧬", time="2 giờ",
  goal="Tái sử dụng code bằng kế thừa; dùng nạp chồng hàm và toán tử để viết code tự nhiên hơn.",
  goals=["Tạo lớp con từ lớp cha, dùng <code>protected</code>", "Hiểu thứ tự gọi constructor/destructor", "Gọi hàm lớp cha từ lớp con; biết đa kế thừa",
         "Nạp chồng hàm, constructor, toán tử <code>+ - == &lt;&lt; [] ()</code>"],
  sections=[
    dict(h="Kế thừa", fig=figs.inheritance_tree(), figcap="Quan hệ “là một”: cảm biến nhiệt LÀ MỘT cảm biến.", html="""
<p>Lớp con <code>class CamBienNhiet : public CamBien</code> nhận toàn bộ thuộc tính và phương thức của lớp cha, rồi thêm/thay đổi phần riêng.</p>
<table class="tbl"><tr><th>Thành viên lớp cha</th><th>Lớp con truy cập?</th><th>Bên ngoài truy cập?</th></tr>
<tr><td><code>public</code></td><td>✓</td><td>✓</td></tr><tr><td><code>protected</code></td><td>✓</td><td>✗</td></tr><tr><td><code>private</code></td><td>✗</td><td>✗</td></tr></table>
<p>Constructor lớp <b>cha chạy trước</b>, destructor lớp <b>con chạy trước</b>.</p>""",
         code="11a-ke-thua.cpp", notes=[
      "Lớp con gọi constructor lớp cha trong danh sách khởi tạo: <code>CamBienNhiet(int chan) : CamBien(\"LM35\", chan, 88)</code>.",
      "<code>CamBien::moTa()</code> gọi bản của lớp cha từ bên trong lớp con.",
      "Đa kế thừa (<code>TramThoiTiet</code>) hữu ích khi ghép các “khả năng” độc lập, nhưng dễ rối — ưu tiên kế thừa interface (bài 12).",
      "Lớp con định nghĩa lại <code>moTa()</code> không có <code>virtual</code> chỉ là “che” hàm — xem sự khác biệt với đa hình ở bài 12.",
    ]),
    dict(h="Nạp chồng", html="""
<p><b>Nạp chồng hàm</b>: nhiều hàm cùng tên nhưng khác kiểu hoặc số tham số; trình biên dịch chọn bản phù hợp lúc biên dịch. <b>Nạp chồng toán tử</b>: định nghĩa ý nghĩa của <code>+</code>, <code>==</code>, <code>&lt;&lt;</code>… cho kiểu do bạn tạo, ví dụ cộng hai vector vị trí.</p>""",
         code="11b-nap-chong.cpp", notes=[
      "<code>operator+</code> trả về đối tượng mới; <code>operator+=</code> sửa chính đối tượng và trả về <code>*this</code>.",
      "<code>operator&lt;&lt;</code> là hàm <code>friend</code> nhận <code>std::ostream&amp;</code> để in được bằng <code>cout</code>.",
      "<code>operator[]</code> trả về tham chiếu nên gán được: <code>bang[0] = true;</code>.",
    ]),
  ],
  embedded=["Lớp <code>Print</code> của Arduino là lớp cha của <code>Serial</code>, <code>LiquidCrystal</code>, <code>WiFiClient</code>… — tất cả đều có <code>print()</code>/<code>println()</code> nhờ kế thừa.",
            "<code>Serial.print()</code> có hàng chục bản nạp chồng cho int, float, chuỗi, cơ số (<code>Serial.print(255, HEX)</code>)."],
  mistakes=["Kế thừa chỉ để dùng lại vài hàm dù không có quan hệ “là một” — dùng composition (chứa đối tượng) thay thế.",
            "Nạp chồng toán tử với ý nghĩa bất ngờ (ví dụ <code>+</code> mà lại trừ).", "Gọi hàm nạp chồng với đối số mơ hồ (<code>f(0)</code> khi có <code>f(int)</code> và <code>f(char*)</code>)."],
  exercises=["Tạo lớp <code>DongCoBuoc</code> kế thừa <code>DongCo</code>, thêm <code>quaySoBuoc(n)</code>.",
             "Viết lớp <code>PhanSo</code> với các toán tử <code>+ - * / == &lt;&lt;</code>, tự rút gọn.",
             "Nạp chồng hàm <code>guiGoiTin</code> cho <code>uint8_t</code>, <code>uint16_t</code>, <code>float</code> — gửi đúng số byte của mỗi kiểu."],
)

L12 = dict(
  id="da-hinh", short="Đa hình & trừu tượng", title="Tính đa hình, tính trừu tượng và interface", icon="🎭", time="2 giờ",
  goal="Viết code làm việc với “bất kỳ loại thiết bị nào” qua lớp cha/interface — nền tảng của mọi thiết kế mềm dẻo.",
  goals=["Dùng <code>virtual</code>/<code>override</code>, phân biệt liên kết tĩnh và động", "Hiểu vtable và chi phí của hàm ảo",
         "Luôn có destructor ảo cho lớp cha đa hình", "Thiết kế lớp trừu tượng và interface (hàm thuần ảo <code>= 0</code>)"],
  sections=[
    dict(h="Đa hình", fig=figs.vtable(), figcap="Mỗi đối tượng có hàm ảo mang một con trỏ ẩn (vptr) tới bảng hàm ảo của lớp thật.", html="""
<p><b>Đa hình</b>: cùng một lời gọi <code>dc-&gt;chay(128)</code> nhưng hành vi khác nhau tuỳ <b>kiểu thật</b> của đối tượng. Điều kiện: hàm ở lớp cha khai báo <code>virtual</code>, gọi qua <b>con trỏ hoặc tham chiếu</b> lớp cha.</p>
<ul><li><code>override</code>: yêu cầu trình biên dịch kiểm tra bạn thật sự ghi đè (gõ sai tên/kiểu sẽ báo lỗi).</li>
<li>Hàm không <code>virtual</code> được chọn theo kiểu <b>con trỏ</b> lúc biên dịch (liên kết tĩnh).</li>
<li>Lớp cha có hàm ảo <b>bắt buộc</b> có <code>virtual ~LopCha()</code>, nếu không xoá qua con trỏ cha sẽ bỏ sót destructor lớp con.</li></ul>""",
         code="12a-da-hinh.cpp", notes=[
      "Mảng <code>DongCo* ds[]</code> chứa ba loại động cơ khác nhau, một vòng lặp điều khiển tất cả.",
      "<code>p-&gt;tenLop()</code> gọi bản của <code>DongCo</code> vì hàm không ảo — dù đối tượng thật là <code>DongCoDC</code>.",
      "Mỗi đối tượng có hàm ảo tốn thêm một con trỏ (8 byte trên PC, 4 byte trên ESP32/STM32) — chấp nhận được trong hầu hết trường hợp.",
    ]),
    dict(h="Trừu tượng và interface", html="""
<p><b>Hàm thuần ảo</b> <code>virtual float doc() = 0;</code> không có thân; lớp chứa nó là <b>lớp trừu tượng</b> — không tạo đối tượng được, chỉ dùng làm lớp cha. Lớp chỉ toàn hàm thuần ảo gọi là <b>interface</b>: mô tả “làm được gì” mà không nói “làm thế nào”.</p>
<div class="callout ok">✅ Nguyên lý <b>phụ thuộc vào trừu tượng</b>: logic ứng dụng chỉ biết <code>IHienThi</code>, <code>CamBien</code>; đổi LCD sang OLED hay đổi DHT22 sang SHT31 không phải sửa logic — chỉ cần lớp mới cài đặt interface.</div>""",
         code="12b-truu-tuong-interface.cpp", notes=[
      "<code>capNhatManHinh()</code> chạy được với cả <code>Lcd1602</code> lẫn <code>SerialMonitor</code> mà không có <code>if</code> nào.",
      "<code>SerialMonitor</code> cài đặt hai interface cùng lúc (<code>IHienThi</code> và <code>IGhiLog</code>).",
      "Lớp trừu tượng <code>CamBien</code> vẫn có code dùng chung (<code>docChuoi()</code>) gọi tới hàm trừu tượng — đây là mẫu Template Method.",
    ]),
  ],
  embedded=["Tầng <b>HAL</b> (Hardware Abstraction Layer) là interface: cùng một firmware chạy trên nhiều board chỉ cần thay lớp cài đặt.",
            "Viết lớp giả (mock) cài đặt interface cảm biến để <b>kiểm thử logic trên máy tính</b> trước khi nạp vào chip.",
            "Khi cần tốc độ tối đa và loại thiết bị cố định lúc biên dịch, có thể thay đa hình bằng template (xem khóa Design Pattern — Strategy)."],
  mistakes=["Quên <code>virtual</code> ở lớp cha → gọi nhầm hàm lớp cha.", "Thiếu destructor ảo.",
            "Truyền đối tượng lớp con vào hàm nhận lớp cha <b>theo giá trị</b> → bị “cắt lát” (object slicing), mất phần lớp con."],
  exercises=["Thiết kế interface <code>IDongCo</code> và hai lớp <code>L298N</code>, <code>TB6612</code>; viết hàm <code>diThang(IDongCo&amp; trai, IDongCo&amp; phai)</code>.",
             "Thêm lớp <code>Oled128x64</code> cài đặt <code>IHienThi</code> và chạy với <code>capNhatManHinh</code>.",
             "Chứng minh object slicing bằng một hàm nhận <code>DongCo</code> theo giá trị."],
)

L13 = dict(
  id="con-tro-lop", short="Con trỏ lớp", title="Con trỏ lớp: Singleton, đổi đối tượng, Adapter, Abstract", icon="🧭", time="2 giờ",
  goal="Dùng con trỏ tới đối tượng để xây các kỹ thuật thiết kế thường gặp trong firmware.",
  goals=["Dùng <code>-&gt;</code>, <code>this</code>, mảng đối tượng", "Viết Singleton bằng con trỏ static",
         "Đổi hành vi lúc chạy bằng cách đổi đối tượng mà con trỏ trỏ tới", "Bọc lớp có sẵn bằng Adapter; làm việc qua con trỏ lớp trừu tượng"],
  sections=[
    dict(h="Con trỏ tới đối tượng, Singleton, đổi đối tượng", html="""
<ul><li><code>p-&gt;ham()</code> là cách viết gọn của <code>(*p).ham()</code>.</li>
<li><code>this</code> là con trỏ tới chính đối tượng đang gọi; trả về <code>this</code> cho phép gọi nối tiếp.</li>
<li><b>Singleton</b> (một thể hiện duy nhất): constructor <code>private</code> + con trỏ <code>static</code> + hàm <code>layThucThe()</code>.</li>
<li><b>Đổi đối tượng qua con trỏ</b>: giữ <code>CheDo* hienTai</code>; đổi chế độ chỉ là gán con trỏ sang đối tượng khác — không cần <code>if/else</code>.</li></ul>""",
         code="13a-con-tro-lop.cpp", notes=[
      "<code>p-&gt;tien(10)-&gt;re(90)-&gt;tien(5)</code> chạy được vì mỗi hàm trả về <code>this</code>.",
      "<code>it - doi</code> (hiệu hai con trỏ) cho ra chỉ số của phần tử trong mảng.",
      "Singleton kiểu con trỏ static đơn giản nhưng không an toàn đa luồng; cách tốt hơn là biến static cục bộ (xem khóa Design Pattern).",
      "Đổi <code>cheDoHienTai</code> chính là ý tưởng của mẫu <b>Strategy/State</b>.",
    ]),
    dict(h="Adapter và Abstract qua con trỏ", code="13b-adapter-abstract.cpp", notes=[
      "<code>VL53Adapter</code> giữ con trỏ tới đối tượng thư viện, cài đặt interface của ta và đổi mm → cm.",
      "Robot giữ <code>std::vector&lt;std::unique_ptr&lt;IKhoangCach&gt;&gt;</code>: danh sách cảm biến bất kỳ, tự giải phóng khi robot bị huỷ.",
      "Đối tượng <code>laser</code> khai báo <code>static</code> để sống suốt chương trình — adapter chỉ “mượn”, không sở hữu.",
    ]),
  ],
  embedded=["Firmware thường có một con trỏ <code>CheDo* cheDoHienTai</code> trong <code>loop()</code>; nút MODE chỉ đổi con trỏ.",
            "Adapter là cách chuẩn để dùng nhiều thư viện cảm biến của các hãng khác nhau dưới một interface chung.",
            "Muốn hiểu sâu hơn: xem khóa <a href='design-pattern.html'>Design Pattern</a> — bài Singleton, Adapter, Strategy, State."],
  mistakes=["Giữ con trỏ tới đối tượng đã bị huỷ (đối tượng cục bộ trong hàm khác).", "Singleton tạo bằng <code>new</code> nhưng không bao giờ giải phóng (chấp nhận được trên MCU, nhưng cần biết).",
            "Dùng <code>dynamic_cast</code> khi firmware tắt RTTI."],
  exercises=["Thêm chế độ <code>CheDoBanDem</code> (quạt luôn chậm) và nút chuyển vòng giữa 3 chế độ.",
             "Viết adapter cho một “thư viện” cảm biến trả về nhiệt độ °F qua hàm <code>getF()</code>.",
             "Viết lớp <code>CauHinh</code> Singleton lưu ngưỡng nhiệt, dùng từ 2 lớp khác nhau."],
)

L14 = dict(
  id="file-ngoai-le-bo-nho", short="File, ngoại lệ, bộ nhớ", title="File I/O, xử lý ngoại lệ và bộ nhớ động", icon="💾", time="2 giờ",
  goal="Ghi/đọc dữ liệu ra file, xử lý lỗi bằng ngoại lệ hoặc std::optional, và quản lý bộ nhớ động an toàn.",
  goals=["Dùng <code>ofstream</code>/<code>ifstream</code>, chế độ ghi thêm, file nhị phân", "Phân tích file CSV",
         "Dùng <code>try/catch/throw</code>, tự định nghĩa ngoại lệ", "Hiểu stack/heap, <code>new/delete</code>, rò rỉ bộ nhớ, con trỏ thông minh, placement new"],
  sections=[
    dict(h="File I/O và Stream", html="""
<table class="tbl"><tr><th>Lớp</th><th>Dùng để</th></tr>
<tr><td><code>std::ofstream</code></td><td>ghi file (<code>std::ios::app</code> để ghi thêm, <code>std::ios::binary</code> cho file nhị phân)</td></tr>
<tr><td><code>std::ifstream</code></td><td>đọc file; <code>std::getline</code> đọc từng dòng</td></tr>
<tr><td><code>std::stringstream</code></td><td>coi một chuỗi như luồng để tách dữ liệu</td></tr></table>
<p>File tự đóng khi đối tượng stream bị huỷ (RAII). Luôn kiểm tra mở file thành công: <code>if (!f) ...</code>.</p>""",
         code="14a-file-io.cpp", notes=[
      "Định dạng CSV (giá trị cách nhau bởi dấu phẩy) mở được bằng Excel — cách ghi log cảm biến phổ biến nhất.",
      "<code>getline(ss, o, ',')</code> tách chuỗi theo dấu phẩy.",
      "File nhị phân lưu nguyên bộ nhớ của struct — nhỏ gọn, nhưng chỉ đọc lại đúng trên máy cùng kiến trúc.",
    ]),
    dict(h="Xử lý ngoại lệ", html="""
<p><b>Ngoại lệ</b> tách đường đi “bình thường” khỏi đường xử lý lỗi: hàm phát hiện lỗi <code>throw</code>; nơi gọi bọc trong <code>try</code> và bắt bằng <code>catch</code>. Ngoại lệ “bay” ngược qua các hàm cho tới khi gặp <code>catch</code> phù hợp; các đối tượng trên đường đi được huỷ đúng cách (RAII).</p>
<div class="callout warn">⚠️ Nhiều dự án nhúng biên dịch với <code>-fno-exceptions</code> để tiết kiệm Flash và đảm bảo thời gian thực. Khi đó trả lỗi bằng giá trị: <code>bool</code>, mã lỗi, hoặc <code>std::optional</code>.</div>""",
         code="14b-ngoai-le.cpp", notes=[
      "Bắt loại cụ thể (<code>LoiCamBien</code>) trước, loại tổng quát (<code>std::exception</code>) sau.",
      "Bắt bằng <code>const&amp;</code> để không sao chép và không bị cắt lát.",
      "<code>std::optional&lt;float&gt;</code>: có giá trị hoặc <code>std::nullopt</code> — kiểm tra bằng <code>if (auto t = ...)</code>.",
    ]),
    dict(h="Bộ nhớ động", fig=figs.memory_layout(), figcap="Các vùng nhớ của một chương trình.", html="""
<table class="tbl"><tr><th>Vùng</th><th>Chứa gì</th><th>Ai giải phóng</th></tr>
<tr><td>Stack</td><td>biến cục bộ, tham số</td><td>tự động khi ra khỏi hàm/khối</td></tr>
<tr><td>Heap</td><td><code>new</code>, <code>malloc</code></td><td>bạn phải <code>delete</code>/<code>free</code> — hoặc giao cho con trỏ thông minh</td></tr>
<tr><td>Static</td><td>biến toàn cục, <code>static</code></td><td>sống suốt chương trình</td></tr></table>
<p><b>Con trỏ thông minh</b>: <code>std::unique_ptr</code> (một chủ, tự <code>delete</code>, không sao chép được, chuyển bằng <code>std::move</code>), <code>std::shared_ptr</code> (nhiều chủ, đếm tham chiếu).</p>""",
         code="14c-bo-nho-dong.cpp", notes=[
      "Ba <code>GoiTin</code> tạo bằng <code>new</code> mà không <code>delete</code> vẫn còn sống ở cuối chương trình — đó là <b>rò rỉ bộ nhớ</b>.",
      "<code>new[]</code> phải đi với <code>delete[]</code>.",
      "<b>Placement new</b> dựng đối tượng vào một vùng nhớ tĩnh có sẵn — kỹ thuật của Object Pool trong firmware, không đụng tới heap.",
    ]),
  ],
  embedded=["ESP32 ghi log ra thẻ SD hoặc LittleFS bằng API rất giống <code>fstream</code>: <code>File f = SD.open(\"/log.csv\", FILE_APPEND); f.println(...);</code>.",
            "Arduino Uno có 2 KB RAM: tránh <code>new</code> và <code>String</code> trong <code>loop()</code> — heap bị phân mảnh và chip treo sau vài giờ.",
            "Quy tắc an toàn (MISRA, AUTOSAR): chỉ cấp phát động lúc khởi động, không cấp phát trong vòng lặp chính."],
  mistakes=["Quên kiểm tra file mở thành công.", "<code>delete</code> hai lần cùng một con trỏ; dùng con trỏ sau khi đã <code>delete</code>.",
            "Ném ngoại lệ trong destructor; bắt ngoại lệ bằng giá trị."],
  exercises=["Ghi 100 mẫu nhiệt độ giả lập ra CSV, đọc lại và tìm max, min, trung bình.",
             "Viết hàm <code>docCauHinh(path)</code> ném ngoại lệ nếu file thiếu dòng bắt buộc; viết lại bằng <code>std::optional</code>.",
             "Viết lại ví dụ rò rỉ bộ nhớ bằng <code>std::unique_ptr</code> và chứng minh không còn rò rỉ."],
)

L15 = dict(
  id="namespace-template", short="Namespace, template…", title="Namespace, template, bộ tiền xử lý và xử lý tín hiệu", icon="🧰", time="2 giờ",
  goal="Tổ chức code lớn bằng namespace, viết code tổng quát bằng template, cấu hình biên dịch bằng tiền xử lý và hiểu tín hiệu.",
  goals=["Tạo và dùng namespace, bí danh, namespace ẩn danh", "Viết hàm mẫu và lớp mẫu (RingBuffer)",
         "Dùng <code>#define</code>, <code>#if/#ifdef</code>, macro có sẵn, include guard", "Đăng ký signal handler và hiểu sự tương đồng với ngắt"],
  sections=[
    dict(h="Namespace", html="<p>Namespace gom tên vào một “họ” để tránh trùng: <code>dht::doc()</code> và <code>bmp::doc()</code> cùng tồn tại. Mọi thứ của thư viện chuẩn nằm trong <code>std::</code>.</p>",
         code="15a-namespace.cpp", notes=["<code>namespace robot::dongCo</code> là cú pháp lồng gọn của C++17.",
                                          "Namespace ẩn danh thay cho <code>static</code> ở phạm vi file.", "Tránh <code>using namespace std;</code> trong file header."]),
    dict(h="Template", html="""
<p>Template cho phép viết code <b>một lần cho nhiều kiểu</b>; trình biên dịch sinh ra bản cụ thể cho từng kiểu được dùng. Tham số template có thể là kiểu (<code>typename T</code>) hoặc giá trị hằng (<code>size_t N</code>) — rất hợp để tạo cấu trúc dữ liệu kích thước cố định cho vi điều khiển.</p>""",
         code="15b-template.cpp", notes=["<code>RingBuffer&lt;uint16_t, 4&gt;</code> có kích thước cố định lúc biên dịch, không cấp phát động.",
                                          "Template thường được viết toàn bộ trong file <code>.h</code> vì trình biên dịch cần thấy định nghĩa để sinh code.",
                                          "Chuyên biệt hoá <code>moTa&lt;bool&gt;</code> cho phép xử lý riêng một kiểu."]),
    dict(h="Bộ tiền xử lý", html="""
<p>Bộ tiền xử lý chạy <b>trước</b> trình biên dịch, chỉ thay thế văn bản: <code>#include</code>, <code>#define</code>, <code>#if/#ifdef/#elif/#else/#endif</code>, <code>#error</code>, <code>#pragma</code>. Macro có sẵn: <code>__FILE__</code>, <code>__LINE__</code>, <code>__func__</code>, <code>__cplusplus</code>.</p>""",
         code="15c-tien-xu-ly.cpp", notes=["Macro thiếu ngoặc: <code>BINH_PHUONG_SAI(2 + 3)</code> thành <code>2 + 3 * 2 + 3 = 11</code>.",
                                            "Biên dịch có điều kiện cho phép một mã nguồn hỗ trợ nhiều board; khi <code>DEBUG 0</code>, macro <code>LOG</code> biến mất hoàn toàn.",
                                            "Trong C++ hiện đại, ưu tiên <code>constexpr</code>, <code>inline</code>, template thay cho macro khi có thể."]),
    dict(h="Xử lý tín hiệu (signal)", html="<p>Tín hiệu là cách hệ điều hành báo sự kiện bất đồng bộ cho chương trình (Ctrl+C, lỗi bộ nhớ…). Hàm xử lý (handler) chạy “chen ngang” chương trình chính — giống hệt <b>hàm phục vụ ngắt (ISR)</b> trên vi điều khiển: phải ngắn, chỉ đặt cờ, việc nặng để vòng lặp chính làm.</p>",
         code="15d-tin-hieu.cpp", notes=["Biến dùng chung với handler có kiểu <code>volatile std::sig_atomic_t</code>.",
                                          "<code>std::raise(SIGINT)</code> tự gửi tín hiệu — dùng ở đây để ví dụ chạy tự động.",
                                          "Giá trị số của tín hiệu phụ thuộc hệ điều hành (ví dụ SIGABRT trên Windows là 22, Linux là 6)."]),
  ],
  embedded=["Arduino định nghĩa sẵn macro theo board: <code>#if defined(ESP32)</code>, <code>#ifdef ARDUINO_AVR_UNO</code>.",
            "PlatformIO cho phép đặt macro trong <code>build_flags = -DDEBUG=1</code> mà không sửa code.",
            "Template + <code>constexpr</code> tạo ra code nhỏ và nhanh như C viết tay — nhiều thư viện nhúng hiện đại (ETL) dựa vào đây."],
  mistakes=["Macro có tác dụng phụ: <code>BINH_PHUONG(i++)</code> tăng i hai lần.", "Quên include guard → lỗi định nghĩa trùng khi include file .h hai lần.",
            "Làm việc nặng (in, cấp phát) trong signal handler / ISR."],
  exercises=["Viết hàm template <code>trungBinh(const T* a, size_t n)</code> dùng được cho int và float.",
             "Thêm vào <code>RingBuffer</code> các hàm <code>full()</code>, <code>empty()</code>, <code>peek()</code>.",
             "Viết macro <code>LOG_LEVEL</code> 0–3 điều khiển in DEBUG/INFO/WARN/ERROR lúc biên dịch."],
)

L16 = dict(
  id="da-luong-stl", short="Đa luồng & STL", title="Đa luồng, thư viện STL, thư viện chuẩn và lập trình web", icon="🧵", time="2 giờ",
  goal="Chạy nhiều việc song song an toàn, dùng thành thạo container và thuật toán STL, biết C++ làm web thế nào.",
  goals=["Tạo luồng, nhận biết data race, dùng mutex / atomic", "Mẫu producer–consumer với condition_variable",
         "Dùng vector, map, set, queue, stack, priority_queue và <code>&lt;algorithm&gt;</code>", "Biết <code>optional</code>, <code>variant</code>, <code>tuple</code>, <code>string_view</code>, <code>bitset</code>"],
  sections=[
    dict(h="Đa luồng", fig=figs.race_timeline(), figcap="Data race: hai luồng cùng đọc giá trị cũ, một lần cộng bị mất.", html="""
<p><b>Luồng (thread)</b> là một dòng thực thi chạy song song với các luồng khác trong cùng chương trình và <b>dùng chung bộ nhớ</b>. Dùng chung tiện nhưng nguy hiểm: hai luồng cùng ghi một biến gây <b>data race</b>.</p>
<table class="tbl"><tr><th>Công cụ</th><th>Dùng để</th></tr>
<tr><td><code>std::thread</code>, <code>join()</code></td><td>tạo luồng, chờ luồng kết thúc</td></tr>
<tr><td><code>std::mutex</code> + <code>std::lock_guard</code></td><td>đảm bảo mỗi lúc chỉ một luồng vào vùng găng</td></tr>
<tr><td><code>std::atomic&lt;T&gt;</code></td><td>thao tác đơn giản (tăng, gán) không thể bị chen ngang</td></tr>
<tr><td><code>std::condition_variable</code></td><td>cho luồng ngủ tới khi có dữ liệu — không tốn CPU chờ</td></tr></table>""",
         code="16a-da-luong.cpp", notes=[
      "Kết quả của bản “không bảo vệ” thay đổi theo từng lần chạy — đặc trưng của lỗi đa luồng, rất khó tái hiện.",
      "<code>lock_guard</code> khoá trong constructor, mở trong destructor (RAII) — không thể quên mở khoá.",
      "Producer–consumer: một luồng đọc cảm biến đẩy vào hàng đợi, một luồng xử lý lấy ra — đúng mô hình task + queue của FreeRTOS.",
    ]),
    dict(h="Thư viện STL", fig=figs.stl_containers(), figcap="Các container thường dùng.", html="""
<p><b>STL</b> (Standard Template Library) gồm <b>container</b> (chứa dữ liệu), <b>iterator</b> (duyệt) và <b>thuật toán</b> (sort, find, count_if, accumulate…). Thuật toán làm việc qua iterator nên dùng được với mọi container.</p>""",
         code="16b-stl.cpp", notes=[
      "Thành ngữ “erase–remove”: <code>v.erase(std::remove(...), v.end())</code> xoá mọi phần tử bằng một giá trị.",
      "<code>for (const auto&amp; [ten, chan] : map)</code> — structured binding duyệt cặp khoá/giá trị.",
      "<code>priority_queue</code> luôn lấy ra phần tử lớn nhất — dùng cho hàng việc theo mức ưu tiên.",
    ]),
    dict(h="Thư viện chuẩn C++ và lập trình web", html="""
<p>Ngoài STL, thư viện chuẩn còn có <code>&lt;optional&gt;</code>, <code>&lt;variant&gt;</code>, <code>&lt;tuple&gt;</code>, <code>&lt;string_view&gt;</code>, <code>&lt;bitset&gt;</code>, <code>&lt;chrono&gt;</code>, <code>&lt;filesystem&gt;</code>, <code>&lt;regex&gt;</code>… và toàn bộ thư viện C (<code>&lt;cstring&gt;</code>, <code>&lt;cstdlib&gt;</code>, <code>&lt;cmath&gt;</code>).</p>
<p><b>Lập trình web với C++</b>: C++ thường làm phần <b>máy chủ hiệu năng cao</b> hoặc <b>web server nhúng</b>:</p>
<ul><li>ESP32: thư viện <code>WebServer</code> / <code>ESPAsyncWebServer</code> — chip tự phát trang web điều khiển LED, xem cảm biến.</li>
<li>Máy tính: <code>cpp-httplib</code> (một file header), Crow, Drogon. Ví dụ: <code>svr.Get("/temp", [](auto&amp;, auto&amp; res){ res.set_content("28.5", "text/plain"); });</code></li>
<li>WebAssembly: biên dịch C++ chạy trong trình duyệt (Emscripten).</li></ul>""",
         code="16c-thu-vien-chuan.cpp", notes=[
      "<code>std::string_view</code> không sao chép chuỗi — tốt cho hàm phân tích lệnh.",
      "<code>auto [t, h, ok] = docDht();</code> nhận nhiều giá trị trả về cùng lúc.",
      "<code>std::variant</code> thay cho <code>union</code>: biết đang chứa kiểu nào, truy cập sai kiểu sẽ báo lỗi.",
    ]),
  ],
  embedded=["ESP32 chạy FreeRTOS: mỗi “luồng” là một <b>task</b>, <code>std::mutex</code> tương ứng mutex của FreeRTOS, hàng đợi tương ứng <code>xQueue</code> — xem khóa <a href='freertos.html'>FreeRTOS</a>.",
            "Trên ESP32, <code>std::thread</code>, <code>std::vector</code>, <code>std::map</code> đều dùng được (ESP-IDF hỗ trợ C++17); trên Arduino Uno thì không có STL.",
            "Biến dùng chung giữa task và ngắt: dùng <code>std::atomic</code> hoặc tắt ngắt trong vùng găng."],
  mistakes=["Quên <code>join()</code> hoặc <code>detach()</code> → chương trình bị huỷ (std::terminate).", "Khoá hai mutex theo thứ tự khác nhau ở hai luồng → deadlock.",
            "Giữ iterator sau khi <code>push_back</code> làm vector cấp phát lại."],
  exercises=["Hai luồng: một luồng sinh 20 số ngẫu nhiên vào hàng đợi, một luồng tính trung bình trượt và in ra.",
             "Dùng <code>std::map&lt;std::string, int&gt;</code> đếm số lần xuất hiện của từng từ trong một đoạn văn.",
             "Sắp xếp danh sách thiết bị theo mức pin tăng dần bằng <code>std::sort</code> với lambda."],
  refs=[("cppreference: thread", "https://en.cppreference.com/w/cpp/thread"), ("cpp-httplib", "https://github.com/yhirose/cpp-httplib"),
        ("ESPAsyncWebServer", "https://github.com/me-no-dev/ESPAsyncWebServer")],
)

_EX = [
  ("17-01-tong-chu-so.cpp", "Tổng chữ số và đảo ngược số", "Dùng <code>% 10</code> lấy chữ số cuối và <code>/ 10</code> bỏ chữ số cuối."),
  ("17-02-so-nguyen-to.cpp", "Số nguyên tố và sàng Eratosthenes", "Chỉ cần thử chia tới √n; sàng gạch bỏ bội số để liệt kê nhanh."),
  ("17-03-fibonacci.cpp", "Dãy Fibonacci: đệ quy vs vòng lặp", "So sánh độ phức tạp: đệ quy O(2ⁿ), vòng lặp O(n)."),
  ("17-04-chuoi.cpp", "Đảo chuỗi, chuỗi đối xứng, đếm nguyên âm", "Kỹ thuật hai con trỏ chạy từ hai đầu vào giữa."),
  ("17-05-sap-xep.cpp", "Sắp xếp nổi bọt và chèn", "Đếm số phép so sánh để thấy thuật toán nào hiệu quả hơn."),
  ("17-06-tim-kiem.cpp", "Tìm kiếm tuần tự và nhị phân", "Nhị phân chỉ cần ~log₂(1000) ≈ 10 bước trên mảng đã sắp xếp."),
  ("17-07-ucln-bcnn.cpp", "UCLN, BCNN và rút gọn phân số", "Thuật toán Euclid: UCLN(a, b) = UCLN(b, a % b)."),
  ("17-08-dem-bit.cpp", "Đếm bit 1, lũy thừa của 2, đảo bit", "Mẹo <code>x &amp; (x - 1)</code> xoá bit 1 thấp nhất."),
  ("17-09-doi-co-so.cpp", "Đổi cơ số 10 ↔ 2/8/16", "Chia liên tiếp cho cơ số, lấy phần dư theo thứ tự ngược."),
  ("17-10-ma-tran.cpp", "Ma trận: nhân, chuyển vị, vết", "Phần tử C[i][j] = tổng A[i][k] × B[k][j]."),
  ("17-11-crc-checksum.cpp", "Checksum XOR và CRC-8", "Kiểm tra lỗi gói tin — kết quả khớp đúng ví dụ trong datasheet cảm biến SHT3x."),
  ("17-12-quan-ly-sinh-vien.cpp", "Quản lý danh sách học sinh", "Bài tổng hợp: struct, vector, sort với lambda, find_if, thống kê."),
]
L17 = dict(
  id="bai-tap", short="12 bài tập C phổ biến", title="12 bài tập C/C++ phổ biến có lời giải", icon="🏆", time="2–4 giờ",
  goal="Rèn tư duy thuật toán qua 12 bài kinh điển (thường gặp trong kiểm tra và phỏng vấn) — tự làm trước, rồi mở lời giải để đối chiếu.",
  goals=["Tự giải được các bài toán cơ bản về số, chuỗi, mảng, bit", "Biết đánh giá thuật toán nhanh/chậm", "Tổng hợp kiến thức của cả khóa trong một chương trình"],
  intro="<p>Mỗi bài có đề, gợi ý và <b>lời giải ẩn</b> (bấm “Xem lời giải”). Hãy tự viết trước ít nhất 15 phút cho mỗi bài.</p>",
  sections=[dict(h=t, html=f"<p><b>Gợi ý:</b> {g}</p>", code=f, solution=True) for f, t, g in _EX],
  summary=["Biến – kiểu – toán tử – rẽ nhánh – vòng lặp – hàm là nền tảng của mọi bài.", "Con trỏ, mảng, chuỗi là chìa khoá khi làm việc với phần cứng và giao thức.",
           "OOP giúp tổ chức firmware lớn; STL và template giúp viết ít mà đúng.", "Bước tiếp theo: khóa <b>FreeRTOS</b> (đa nhiệm thời gian thực) và <b>Design Pattern</b> (thiết kế phần mềm)."],
)

LESSONS_OOP = [L10, L11, L12, L13]
LESSONS_ADV = [L14, L15, L16]
LESSONS_PRACTICE = [L17]
