# -*- coding: utf-8 -*-
"""Nội dung nhóm Creational (khởi tạo).

Cấu trúc mỗi mẫu: xem README.md. Sơ đồ UML mô tả bằng dict:
  boxes: (id, tên, stereotype|None, [thuộc tính], [phương thức], cx, y)   cx = tâm ngang, y = mép trên
  edges: (từ, tới, loại, nhãn, tuỳ_chọn)  loại: ext | impl | assoc | dep | agg | comp | note
  notes: (id, văn bản nhiều dòng, cx, y)
"""

PATTERNS = [
# ------------------------------------------------------------------ 1
dict(
  id="singleton", name="Singleton", vn="Đơn thể", icon="1️⃣", freq=5,
  ref="https://gpcoder.com/4190-huong-dan-java-design-pattern-singleton/",
  intent="Đảm bảo một lớp <b>chỉ có duy nhất một thể hiện (instance)</b> và cung cấp một điểm truy cập toàn cục tới thể hiện đó.",
  analogy=("🏛️", "Mỗi nước chỉ có <b>một chính phủ</b> chính thức. Dù ai hỏi “chính phủ ở đâu?” thì câu trả lời luôn chỉ về cùng một nơi — không ai tự lập thêm một chính phủ thứ hai."),
  problem="""
<p>Có những đối tượng mà cả chương trình <b>chỉ nên có một</b>: bộ cấu hình ứng dụng, đối tượng ghi log, bộ quản lý kết nối phần cứng (cổng Serial tới Arduino), bộ đệm (cache)… Nếu mỗi nơi tự <code>new</code> một bản:</p>
<ul>
<li>Cấu hình bị <b>lệch nhau</b> — module A sửa <code>wifi.ssid</code> nhưng module B vẫn đọc giá trị cũ.</li>
<li><b>Lãng phí tài nguyên</b> — mở nhiều kết nối tới cùng một thiết bị, có khi còn gây xung đột.</li>
<li>Biến toàn cục (<code>public static</code>) thì giải quyết được “truy cập ở mọi nơi”, nhưng <b>không chặn được</b> người khác tạo thêm đối tượng và có thể bị ghi đè bất cứ lúc nào.</li>
</ul>""",
  solution="""
<p>Singleton giải quyết bằng 3 bước:</p>
<ol>
<li>Đặt constructor là <code>private</code> → bên ngoài <b>không thể</b> gọi <code>new</code>.</li>
<li>Giữ một biến <code>static</code> trỏ tới thể hiện duy nhất.</li>
<li>Cung cấp phương thức <code>static getInstance()</code>: lần đầu thì tạo, các lần sau trả lại đúng đối tượng đã tạo.</li>
</ol>
<p>Cách cài đặt được khuyên dùng ở mỗi ngôn ngữ:</p>
<table class="tbl">
<tr><th>Ngôn ngữ</th><th>Cách viết</th><th>Ghi chú</th></tr>
<tr><td><b>C++11 trở lên</b></td><td><i>Meyers Singleton</i>: <code>static T&amp; get() { static T inst; return inst; }</code></td><td>Lazy, thread-safe theo chuẩn, không dùng heap. Nhớ <code>= delete</code> copy constructor và phép gán.</td></tr>
<tr><td><b>C++ trên vi điều khiển</b></td><td>Đối tượng toàn cục / <code>static</code> (như <code>Serial</code>, <code>WiFi</code> của Arduino)</td><td>Đơn giản nhất, nhưng cẩn thận <i>thứ tự khởi tạo</i> giữa các file .cpp — dùng hàm <code>begin()</code> gọi trong <code>setup()</code>.</td></tr>
<tr><td><b>Python</b></td><td>Một <b>module</b>, hoặc ghi đè <code>__new__</code> / metaclass</td><td>Module chỉ được nạp một lần nên đã là singleton tự nhiên.</td></tr>
<tr><td><b>Java</b></td><td><code>enum</code> hoặc static holder (Bill Pugh)</td><td>Double-checked locking phải có <code>volatile</code>.</td></tr>
</table>""",
  participants=[
    ("Singleton", "Khai báo constructor private, giữ thể hiện duy nhất trong biến static và trả về qua getInstance()."),
    ("Client", "Không bao giờ new Singleton, chỉ gọi Singleton.getInstance()."),
  ],
  uml=dict(
    boxes=[
      ("client", "Client", None, [], ["main()"], 100, 46),
      ("s", "Singleton", None, ["- instance: Singleton {static}", "- data"],
       ["- Singleton()", "+ getInstance(): Singleton {static}", "+ operation()"], 410, 20),
    ],
    notes=[("n1", "static Singleton& getInstance() {\n    static Singleton instance;  // tạo 1 lần\n    return instance;\n}", 410, 200)],
    edges=[("client", "s", "dep", "getInstance()"), ("n1", "s", "note", "")],
  ),
  code="01-singleton.java",
  java_notes=[
    "<b>AppConfig</b> dùng kỹ thuật <i>static holder</i>: lớp lồng <code>Holder</code> chỉ được JVM nạp khi lần đầu gọi <code>getInstance()</code>, và việc nạp lớp vốn đã thread-safe.",
    "<b>LazyLogger</b> minh hoạ <i>double-checked locking</i>. Từ khoá <code>volatile</code> là bắt buộc — thiếu nó, luồng khác có thể thấy một đối tượng “chưa khởi tạo xong”.",
    "Thử 50 luồng gọi đồng thời: chỉ <b>1</b> thể hiện được tạo, constructor chạy đúng <b>1</b> lần.",
    "<b>Counter</b> là cách viết bằng <code>enum</code>: gọn nhất và an toàn nhất.",
  ],
  pros=["Đảm bảo chỉ có một thể hiện.", "Truy cập toàn cục, khởi tạo trễ (lazy) khi cần.", "Kiểm soát chặt việc truy cập tài nguyên dùng chung."],
  cons=["Vi phạm nguyên lý Single Responsibility (vừa lo nghiệp vụ vừa lo vòng đời).", "Che giấu phụ thuộc → khó viết unit test, khó mock.", "Cần cẩn thận trong môi trường đa luồng.", "Dễ bị lạm dụng như một “biến toàn cục trá hình”."],
  when=["Cần đúng một đối tượng dùng chung: cấu hình, logger, cache, connection manager, driver phần cứng.", "Muốn kiểm soát chặt hơn biến toàn cục."],
  realworld=["<code>java.lang.Runtime.getRuntime()</code>", "<code>java.awt.Desktop.getDesktop()</code>", "Bean mặc định (scope singleton) trong Spring Framework"],
  related="Facade, Abstract Factory và Builder thường được cài đặt dưới dạng Singleton. Khác với Flyweight: Flyweight có nhiều thể hiện bất biến được chia sẻ, Singleton chỉ có một thể hiện (có thể thay đổi).",
  exercises=[
    "Viết lớp <code>I2CBus</code> (Singleton) quản lý bus I2C dùng chung cho nhiều cảm biến, có <code>begin()</code> chỉ khởi tạo phần cứng một lần.",
    "Dùng reflection (<code>getDeclaredConstructor().setAccessible(true)</code>) phá Singleton kiểu Bill Pugh. Sau đó chứng minh enum Singleton chống được cách này.",
    "Trên Arduino, khai báo hai đối tượng toàn cục ở hai file .cpp, đối tượng này dùng đối tượng kia trong constructor. Giải thích “static initialization order fiasco” và cách Meyers Singleton khắc phục.",
  ],
),
# ------------------------------------------------------------------ 2
dict(
  id="factory-method", name="Factory Method", vn="Phương thức nhà máy", icon="🏭", freq=5,
  ref="https://gpcoder.com/4352-huong-dan-java-design-pattern-factory-method/",
  intent="Định nghĩa một <b>giao diện để tạo đối tượng</b>, nhưng để <b>lớp con quyết định</b> lớp cụ thể nào sẽ được khởi tạo.",
  analogy=("🚚", "Công ty logistics có quy trình giao hàng chung: nhận đơn → đóng gói → <i>chọn phương tiện</i> → giao. Chi nhánh đường bộ chọn xe tải, chi nhánh đường biển chọn tàu. Quy trình không đổi, chỉ “bước tạo phương tiện” là khác."),
  problem="""
<p>Ứng dụng của trường ban đầu chỉ gửi thông báo qua Email, nên code viết thẳng <code>new EmailNotification()</code> khắp nơi. Giờ nhà trường muốn thêm SMS và Zalo:</p>
<ul>
<li>Phải tìm và sửa <b>mọi chỗ</b> có <code>new EmailNotification()</code>, thêm hàng loạt <code>if/else</code> hoặc <code>switch</code>.</li>
<li>Mỗi lần thêm kênh mới lại sửa code cũ → vi phạm nguyên lý <b>Open/Closed</b> (mở để mở rộng, đóng để sửa đổi).</li>
<li>Logic nghiệp vụ (gửi cho ai, khi nào) bị trộn lẫn với logic khởi tạo đối tượng.</li>
</ul>""",
  solution="""
<p>Thay vì gọi <code>new</code> trực tiếp, ta gọi một phương thức đặc biệt — <b>factory method</b> — <code>createNotification()</code>. Lớp cha <code>NotificationService</code> chứa thuật toán chung và <i>gọi</i> factory method, còn <b>lớp con ghi đè</b> phương thức này để trả về loại thông báo cụ thể.</p>
<p>Mọi sản phẩm đều cài đặt chung interface <code>Notification</code>, nên lớp cha làm việc với sản phẩm mà không cần biết lớp cụ thể của nó.</p>
<div class="callout">💡 <b>Phân biệt với “Simple Factory”</b>: Simple Factory là một hàm static có <code>switch</code> trả về đối tượng (không phải mẫu GoF). Factory Method dựa vào <b>kế thừa và đa hình</b> — muốn thêm loại mới chỉ cần thêm lớp con, không sửa code cũ.</div>""",
  participants=[
    ("Product (Notification)", "Interface chung cho mọi đối tượng mà factory method tạo ra."),
    ("ConcreteProduct (EmailNotification…)", "Các cài đặt cụ thể của Product."),
    ("Creator (NotificationService)", "Khai báo factory method trả về Product; chứa logic nghiệp vụ dùng Product."),
    ("ConcreteCreator (EmailService…)", "Ghi đè factory method để trả về ConcreteProduct tương ứng."),
  ],
  uml=dict(
    boxes=[
      ("creator", "NotificationService", "abstract", [], ["+ notifyUser(msg)", "# createNotification(): Notification"], 200, 20),
      ("product", "Notification", "interface", [], ["+ send(message)"], 620, 30),
      ("c1", "EmailService", None, [], ["# createNotification()"], 100, 210),
      ("c2", "SmsService", None, [], ["# createNotification()"], 300, 210),
      ("p1", "EmailNotification", None, [], ["+ send(message)"], 530, 210),
      ("p2", "SmsNotification", None, [], ["+ send(message)"], 720, 210),
    ],
    notes=[("n1", "auto n = createNotification();\nn->send(msg);", 200, 330)],
    edges=[
      ("c1", "creator", "ext", "", "tree"), ("c2", "creator", "ext", "", "tree"),
      ("p1", "product", "impl", "", "tree"), ("p2", "product", "impl", "", "tree"),
      ("creator", "product", "dep", "dùng"),
      ("n1", "c2", "note", ""),
    ],
    caption="EmailService tạo EmailNotification, SmsService tạo SmsNotification (ZaloService tương tự).",
  ),
  code="02-factory-method.java",
  java_notes=[
    "<code>notifyUser()</code> ở lớp cha là logic chung — nó không hề biết đang gửi qua Email hay SMS.",
    "Mỗi lớp con chỉ cần ghi đè <b>một dòng</b>: <code>createNotification()</code>.",
    "<code>SmsNotification</code> có xử lý riêng (cắt chuỗi 30 ký tự) — chi tiết này được đóng gói trong sản phẩm, client không cần biết.",
    "Thêm kênh Telegram? Tạo <code>TelegramNotification</code> + <code>TelegramService</code>. Không sửa dòng code cũ nào.",
  ],
  pros=["Tách rời code tạo đối tượng khỏi code sử dụng (loose coupling).", "Tuân thủ Open/Closed: thêm sản phẩm mới không sửa code cũ.", "Tuân thủ Single Responsibility: việc khởi tạo tập trung một chỗ."],
  cons=["Số lượng lớp tăng lên (mỗi sản phẩm cần thêm một Creator con).", "Có thể “dùng dao mổ trâu giết gà” nếu chỉ có 1–2 loại sản phẩm không bao giờ thay đổi."],
  when=["Không biết trước chính xác loại đối tượng cần tạo.", "Muốn cho phép người dùng thư viện/framework mở rộng các thành phần bên trong.", "Muốn tái sử dụng đối tượng có sẵn thay vì luôn tạo mới (factory method có thể trả về đối tượng từ cache)."],
  realworld=["<code>java.util.Calendar.getInstance()</code>", "<code>java.text.NumberFormat.getInstance()</code>", "<code>Collection.iterator()</code> — mỗi collection tạo iterator riêng", "<code>javax.xml.parsers.DocumentBuilderFactory.newInstance()</code>"],
  related="Factory Method thường là điểm khởi đầu, sau đó phát triển thành Abstract Factory, Prototype hoặc Builder khi cần linh hoạt hơn. Template Method thường gọi Factory Method bên trong.",
  exercises=[
    "Thêm kênh <code>TelegramNotification</code> mà không sửa bất kỳ lớp nào đã có.",
    "Viết <code>RobotFactory</code>: lớp cha có <code>runMission()</code>, lớp con <code>LineRobotFactory</code>/<code>SumoRobotFactory</code> tạo ra robot tương ứng.",
    "So sánh: viết lại ví dụ bằng Simple Factory (hàm static có switch). Nêu ưu, nhược của mỗi cách.",
  ],
),
# ------------------------------------------------------------------ 3
dict(
  id="abstract-factory", name="Abstract Factory", vn="Nhà máy trừu tượng", icon="🏗️", freq=4,
  ref="https://gpcoder.com/4365-huong-dan-java-design-pattern-abstract-factory/",
  intent="Cung cấp một interface để tạo ra <b>các họ (family) đối tượng liên quan</b> với nhau mà không cần chỉ rõ lớp cụ thể của chúng.",
  analogy=("🛋️", "Cửa hàng nội thất bán theo <b>bộ sưu tập</b>: bộ Hiện đại (ghế, bàn, sofa hiện đại) và bộ Cổ điển. Bạn chọn bộ nào thì <i>mọi món</i> đều hợp phong cách — không ai giao ghế hiện đại kèm bàn cổ điển."),
  problem="""
<p>Ứng dụng có giao diện Sáng (Light) và Tối (Dark). Mỗi giao diện gồm nhiều thành phần: nút bấm, checkbox, thanh cuộn…</p>
<ul>
<li>Nếu tạo từng thành phần bằng <code>if (dark) new DarkButton() else new LightButton()</code> ở khắp nơi → code rối, dễ <b>trộn lẫn</b> nút tối với checkbox sáng.</li>
<li>Thêm giao diện thứ ba (High Contrast) phải sửa tất cả các chỗ đó.</li>
</ul>""",
  solution="""
<p>Khai báo interface riêng cho từng <b>loại sản phẩm</b> (<code>Button</code>, <code>Checkbox</code>). Tạo interface <b>Abstract Factory</b> (<code>UIFactory</code>) với các phương thức tạo cho mọi loại sản phẩm. Mỗi “họ” sản phẩm có một <b>Concrete Factory</b> riêng (<code>LightThemeFactory</code>, <code>DarkThemeFactory</code>).</p>
<p>Client nhận một factory duy nhất lúc khởi động và chỉ làm việc qua các interface → đảm bảo mọi thành phần <b>cùng một họ</b>.</p>
<div class="callout">💡 <b>Factory Method vs Abstract Factory</b>: Factory Method tạo <b>một</b> sản phẩm qua kế thừa. Abstract Factory tạo <b>cả một họ</b> sản phẩm qua một đối tượng factory (composition) — thực chất mỗi phương thức trong Abstract Factory thường là một factory method.</div>""",
  participants=[
    ("AbstractFactory (UIFactory)", "Khai báo các phương thức tạo cho từng loại sản phẩm trừu tượng."),
    ("ConcreteFactory (LightThemeFactory…)", "Cài đặt các phương thức tạo, trả về sản phẩm cùng một họ."),
    ("AbstractProduct (Button, Checkbox)", "Interface cho một loại sản phẩm."),
    ("ConcreteProduct (DarkButton…)", "Sản phẩm cụ thể thuộc một họ."),
    ("Client", "Chỉ dùng AbstractFactory và AbstractProduct."),
  ],
  uml=dict(
    boxes=[
      ("f", "UIFactory", "interface", [], ["+ createButton(): Button", "+ createCheckbox(): Checkbox"], 175, 20),
      ("f1", "LightThemeFactory", None, [], ["+ createButton()", "+ createCheckbox()"], 85, 210),
      ("f2", "DarkThemeFactory", None, [], ["+ createButton()", "+ createCheckbox()"], 265, 210),
      ("b", "Button", "interface", [], ["+ paint()"], 520, 30),
      ("c", "Checkbox", "interface", [], ["+ paint()"], 800, 30),
      ("b1", "LightButton", None, [], ["+ paint()"], 455, 210),
      ("b2", "DarkButton", None, [], ["+ paint()"], 590, 210),
      ("c1", "LightCheckbox", None, [], ["+ paint()"], 735, 210),
      ("c2", "DarkCheckbox", None, [], ["+ paint()"], 875, 210),
    ],
    edges=[
      ("f1", "f", "impl", "", "tree"), ("f2", "f", "impl", "", "tree"),
      ("b1", "b", "impl", "", "tree"), ("b2", "b", "impl", "", "tree"),
      ("c1", "c", "impl", "", "tree"), ("c2", "c", "impl", "", "tree"),
    ],
    caption="LightThemeFactory chỉ tạo LightButton + LightCheckbox; DarkThemeFactory chỉ tạo DarkButton + DarkCheckbox.",
  ),
  code="03-abstract-factory.java",
  java_notes=[
    "Hàm <code>render(UIFactory)</code> không có một chữ “Light” hay “Dark” nào — nó hoàn toàn độc lập với giao diện cụ thể.",
    "Việc chọn họ sản phẩm chỉ diễn ra <b>một lần</b> trong <code>main</code> (thực tế: đọc từ file cấu hình hoặc cài đặt hệ điều hành).",
    "Muốn thêm giao diện High Contrast: thêm 1 factory + 2 sản phẩm, không sửa client.",
  ],
  pros=["Đảm bảo các sản phẩm từ cùng một factory luôn tương thích với nhau.", "Client tách biệt hoàn toàn khỏi lớp cụ thể.", "Đổi cả họ sản phẩm chỉ bằng việc đổi một đối tượng factory."],
  cons=["Thêm một <b>loại</b> sản phẩm mới (ví dụ Slider) phải sửa interface factory và <b>mọi</b> concrete factory.", "Nhiều interface và lớp mới → code phức tạp hơn."],
  when=["Hệ thống cần làm việc với nhiều họ sản phẩm liên quan và cần đảm bảo tính nhất quán giữa chúng.", "Muốn cung cấp thư viện sản phẩm mà chỉ lộ ra interface, không lộ cài đặt.", "Hỗ trợ đa nền tảng: Windows/macOS, MySQL/PostgreSQL…"],
  realworld=["<code>javax.xml.parsers.DocumentBuilderFactory</code>", "<code>javax.xml.transform.TransformerFactory</code>", "JDBC: <code>Connection</code> tạo ra <code>Statement</code>, <code>PreparedStatement</code> cùng một driver"],
  related="Concrete Factory thường là Singleton. Có thể cài đặt bằng Factory Method hoặc Prototype. Abstract Factory có thể thay Facade khi chỉ cần che giấu cách tạo đối tượng của hệ thống con.",
  exercises=[
    "Thêm họ <code>HighContrastThemeFactory</code>.",
    "Thêm loại sản phẩm <code>Slider</code>. Có bao nhiêu file phải sửa? Nhận xét.",
    "Thiết kế <code>DatabaseFactory</code> tạo <code>Connection</code> + <code>QueryBuilder</code> cho MySQL và SQLite.",
  ],
),
# ------------------------------------------------------------------ 4
dict(
  id="builder", name="Builder", vn="Người xây dựng", icon="🧱", freq=5,
  ref="https://gpcoder.com/4434-huong-dan-java-design-pattern-builder/",
  intent="<b>Tách quá trình xây dựng</b> một đối tượng phức tạp ra khỏi biểu diễn của nó, để cùng một quá trình có thể tạo ra nhiều biểu diễn khác nhau — xây <b>từng bước một</b>.",
  analogy=("🍔", "Gọi bánh mì ở tiệm: “Cho 1 ổ, <i>thêm</i> pate, <i>thêm</i> chả, <i>không</i> hành, <i>thêm</i> ớt” — rồi mới “Làm đi!”. Bạn chỉ nói những thứ mình cần, theo bất kỳ thứ tự nào, và chỉ nhận bánh khi đã đủ."),
  problem="""
<p>Lớp <code>Robot</code> có 2 thông số bắt buộc (tên, bo mạch) và nhiều thông số tuỳ chọn (số bánh, pin, bluetooth, danh sách cảm biến…). Các cách làm thông thường đều có vấn đề:</p>
<ul>
<li><b>Telescoping constructor</b>: <code>new Robot("BK", "ESP32", 4, 3000, true, null, null, false)</code> — không ai nhớ tham số thứ 5 là gì, dễ truyền nhầm thứ tự.</li>
<li><b>Constructor rỗng + nhiều setter</b>: đối tượng ở trạng thái “dở dang” giữa các lần gọi setter, và không thể làm đối tượng <b>bất biến (immutable)</b>.</li>
</ul>""",
  solution="""
<p>Đưa việc xây dựng ra một lớp riêng — <b>Builder</b>. Builder có các phương thức đặt từng thuộc tính, mỗi phương thức <code>return this</code> để gọi nối tiếp (<i>fluent interface</i>). Cuối cùng gọi <code>build()</code> để kiểm tra dữ liệu và tạo đối tượng hoàn chỉnh.</p>
<p>Tuỳ chọn: lớp <b>Director</b> đóng gói các “công thức” xây dựng thường dùng (robot dò line, robot sumo…) để tái sử dụng.</p>
<div class="callout">💡 <b>C++</b>: Builder thường là lớp lồng <code>Robot::Builder</code>, các hàm trả về <code>Builder&amp;</code> để gọi nối tiếp. Firmware hay tắt exception (<code>-fno-exceptions</code>) nên <code>build()</code> trả về <code>std::optional</code> thay vì <code>throw</code>.<br><b>Python</b>: tham số đặt tên + giá trị mặc định đã giải quyết phần lớn vấn đề; Builder vẫn hữu ích khi cần kiểm tra ràng buộc và xây từng bước. <b>Java</b>: static nested class hoặc Lombok <code>@Builder</code>.</div>""",
  participants=[
    ("Builder (Robot.Builder)", "Cung cấp các bước xây dựng và phương thức build()."),
    ("Product (Robot)", "Đối tượng phức tạp được tạo ra, thường immutable."),
    ("Director (RobotDirector)", "Biết trình tự gọi các bước để tạo cấu hình chuẩn (không bắt buộc)."),
    ("Client", "Tạo Builder, gọi các bước, nhận Product."),
  ],
  uml=dict(
    boxes=[
      ("d", "RobotDirector", "Director", [], ["+ makeLineFollower(): Robot", "+ makeSumoRobot(): Robot"], 130, 30),
      ("b", "Robot.Builder", "Builder", ["- name, board", "- wheels = 2", "- sensors: List"],
       ["+ Builder(name, board)", "+ wheels(n): Builder", "+ addSensor(s): Builder", "+ battery(mAh): Builder", "+ build(): Robot"], 460, 20),
      ("p", "Robot", "Product", ["- final name, board", "- final wheels, sensors…"], ["- Robot(Builder)", "+ toString()"], 790, 40),
      ("cl", "Client", None, [], ["main()"], 130, 250),
    ],
    edges=[
      ("d", "b", "assoc", "dùng"), ("b", "p", "dep", "«create»"),
      ("cl", "b", "dep", "gọi nối tiếp"), ("cl", "d", "dep", ""),
    ],
  ),
  code="04-builder.java",
  java_notes=[
    "Constructor của <code>Robot</code> là <code>private</code> và nhận vào <code>Builder</code> → chỉ có thể tạo Robot thông qua Builder.",
    "Mọi field của Robot là <code>final</code>, danh sách cảm biến được sao chép bằng <code>List.copyOf</code> → Robot là immutable, an toàn đa luồng.",
    "Tham số bắt buộc đưa vào constructor của Builder; tham số tuỳ chọn có giá trị mặc định.",
    "<code>build()</code> là nơi lý tưởng để <b>kiểm tra ràng buộc</b> (ví dụ chỉ 2 hoặc 4 bánh) trước khi đối tượng ra đời.",
  ],
  pros=["Code tạo đối tượng dễ đọc, tự mô tả.", "Tạo được đối tượng immutable với nhiều tham số tuỳ chọn.", "Kiểm tra dữ liệu tập trung trước khi tạo.", "Tái sử dụng quy trình xây dựng cho nhiều biểu diễn (qua Director)."],
  cons=["Phải viết thêm một lớp Builder (trùng lặp các field).", "Không đáng dùng với lớp chỉ có 2–3 thuộc tính."],
  when=["Constructor có nhiều tham số (thường từ 4 trở lên), nhất là tham số tuỳ chọn.", "Cần tạo đối tượng immutable.", "Cần tạo các biểu diễn khác nhau của cùng một sản phẩm theo cùng quy trình (ví dụ xuất tài liệu ra HTML/PDF/Markdown)."],
  realworld=["<code>StringBuilder</code> / <code>StringBuffer</code>", "<code>java.net.http.HttpRequest.newBuilder()</code>", "<code>Stream.builder()</code>, <code>Locale.Builder</code>", "Lombok <code>@Builder</code>, OkHttp <code>Request.Builder</code>"],
  related="Builder tập trung vào xây dựng từng bước; Abstract Factory tập trung vào họ sản phẩm và trả về ngay. Builder thường dùng để tạo cây Composite phức tạp.",
  exercises=[
    "Viết <code>Student.Builder</code> với: họ tên, mã HS (bắt buộc); lớp, email, số điện thoại, danh sách môn (tuỳ chọn). Kiểm tra email phải chứa “@”.",
    "Thêm vào Director công thức <code>makeAvoidObstacleRobot()</code>.",
    "Viết <code>HtmlPageBuilder</code> với các bước <code>title()</code>, <code>heading()</code>, <code>paragraph()</code>, <code>build()</code> trả về chuỗi HTML.",
  ],
),
# ------------------------------------------------------------------ 5
dict(
  id="prototype", name="Prototype", vn="Nguyên mẫu", icon="🧬", freq=3,
  ref="https://gpcoder.com/4413-huong-dan-java-design-pattern-prototype/",
  intent="Tạo đối tượng mới bằng cách <b>sao chép (clone) một đối tượng có sẵn</b> — bản mẫu — thay vì khởi tạo từ đầu.",
  analogy=("🐑", "Giáo viên soạn một <b>đề gốc</b> rất công phu, rồi <i>photo</i> ra nhiều bản và sửa nhẹ từng bản thành mã đề 101, 102… Nhanh hơn rất nhiều so với soạn lại từng đề từ con số 0."),
  problem="""
<p>Bạn muốn tạo một bản sao y hệt một đối tượng. Cách “ngây thơ” là tạo đối tượng mới rồi chép từng field sang. Nhưng:</p>
<ul>
<li>Nhiều field là <code>private</code> — từ bên ngoài không đọc được.</li>
<li>Code sao chép phụ thuộc vào <b>lớp cụ thể</b> của đối tượng, trong khi đôi khi ta chỉ biết nó qua interface.</li>
<li>Việc khởi tạo có thể rất <b>tốn kém</b> (đọc file, truy vấn CSDL, tính toán nặng) — làm lại nhiều lần là lãng phí.</li>
</ul>""",
  solution="""
<p>Giao trách nhiệm sao chép cho <b>chính đối tượng</b> đó: khai báo interface chung có phương thức <code>clone()</code>. Đối tượng tự biết cách sao chép mọi field của nó (kể cả private).</p>
<p>Có thể kết hợp <b>Prototype Registry</b>: một kho lưu sẵn các bản mẫu đã cấu hình, cần loại nào thì lấy ra và clone.</p>
<div class="callout warn">⚠️ <b>Shallow copy vs Deep copy</b>: <br>• <i>Shallow</i>: chỉ chép tham chiếu → bản sao và bản gốc <b>dùng chung</b> các đối tượng con (như List). Sửa list của bản sao sẽ làm hỏng bản gốc!<br>• <i>Deep</i>: tạo bản sao mới cho cả các đối tượng con. Ví dụ dùng <code>new ArrayList&lt;&gt;(src.questions)</code> để deep copy.</div>
<table class="tbl">
<tr><th>Ngôn ngữ</th><th>Công cụ có sẵn</th><th>Lưu ý</th></tr>
<tr><td><b>C++</b></td><td>Copy constructor; hàm ảo <code>clone()</code> trả về <code>std::unique_ptr&lt;Base&gt;</code></td><td>Copy mặc định sao chép sâu với <code>std::vector</code>, <code>std::string</code>… nhưng <b>nông</b> với con trỏ thô → dễ double-free (quy tắc 3/5).</td></tr>
<tr><td><b>Python</b></td><td><code>copy.copy()</code> (nông), <code>copy.deepcopy()</code> (sâu)</td><td>Có thể tuỳ biến bằng <code>__copy__</code>/<code>__deepcopy__</code>.</td></tr>
<tr><td><b>Java</b></td><td><code>Cloneable</code> + <code>Object.clone()</code></td><td>Nhiều cạm bẫy; nên dùng copy constructor.</td></tr>
</table>""",
  participants=[
    ("Prototype", "Interface khai báo phương thức clone()."),
    ("ConcretePrototype (ExamPaper, Circle)", "Cài đặt clone() — tự sao chép chính mình."),
    ("Registry (ShapeRegistry)", "Lưu các bản mẫu dựng sẵn, trả về bản sao theo khoá (không bắt buộc)."),
    ("Client", "Gọi clone() thay vì new."),
  ],
  uml=dict(
    boxes=[
      ("p", "Prototype<T>", "interface", [], ["+ clone(): T"], 320, 20),
      ("e", "ExamPaper", None, ["- title, code", "- questions: List"], ["+ clone(): ExamPaper", "+ addQuestion(q)"], 130, 190),
      ("s", "Shape", "abstract", ["# x, y, color"], ["+ clone(): Shape", "+ move(dx, dy)"], 420, 190),
      ("c", "Circle", None, ["- radius"], ["+ clone(): Circle"], 420, 360),
      ("r", "ShapeRegistry", None, ["- prototypes: Map"], ["+ get(key): Shape"], 730, 190),
    ],
    notes=[("n1", "return std::make_unique<Circle>(*this);\n// gọi copy constructor", 700, 380)],
    edges=[
      ("e", "p", "impl", "", "tree"), ("s", "p", "impl", "", "tree"),
      ("c", "s", "ext", ""), ("r", "s", "agg", "*"), ("n1", "c", "note", ""),
    ],
  ),
  code="05-prototype.java",
  java_notes=[
    "<code>ExamPaper</code> dùng <b>copy constructor private</b> để clone — truy cập được mọi field private.",
    "Dòng <code>new ArrayList&lt;&gt;(src.questions)</code> đảm bảo deep copy: thêm câu hỏi vào đề 101 <b>không</b> ảnh hưởng đề gốc (kết quả <code>false</code>).",
    "<code>ShapeRegistry.get()</code> luôn trả về bản sao mới — di chuyển <code>c2</code> không làm <code>c1</code> thay đổi.",
    "Trong <code>Shape</code> phải khai báo lại <code>public abstract Shape clone()</code> vì <code>Object.clone()</code> là <code>protected</code>.",
  ],
  pros=["Sao chép đối tượng mà không phụ thuộc vào lớp cụ thể.", "Tránh lặp lại quá trình khởi tạo tốn kém.", "Tạo đối tượng phức tạp tiện lợi hơn từ các bản mẫu dựng sẵn.", "Có thể thay thế việc tạo nhiều lớp con chỉ khác nhau về cấu hình."],
  cons=["Clone đối tượng có tham chiếu vòng (A → B → A) rất phức tạp.", "Dễ nhầm lẫn shallow/deep copy gây lỗi khó phát hiện."],
  when=["Chi phí tạo mới cao hơn nhiều so với sao chép.", "Cần nhiều đối tượng chỉ khác nhau một chút về trạng thái.", "Code không nên phụ thuộc vào lớp cụ thể của đối tượng cần sao chép."],
  realworld=["<code>java.lang.Object#clone()</code> và interface <code>Cloneable</code>", "<code>ArrayList.clone()</code>, <code>HashMap.clone()</code> (shallow copy)", "Spring bean với <code>scope=\"prototype\"</code>"],
  related="Prototype có thể thay thế Factory Method khi không muốn tạo nhiều lớp Creator con. Memento đôi khi dùng Prototype để chụp trạng thái. Composite và Decorator hưởng lợi từ Prototype khi cần sao chép cấu trúc phức tạp.",
  exercises=[
    "Sửa copy constructor thành <code>this.questions = src.questions;</code> rồi chạy lại. Giải thích kết quả <code>true</code> và tác hại.",
    "Thêm lớp <code>Rectangle</code> vào registry với khoá <code>\"green-square\"</code>.",
    "C++: viết copy constructor đúng cho <code>SensorBuffer</code> (cấp phát mảng mới và chép dữ liệu) theo quy tắc 3/5, kiểm chứng rằng sửa bản sao không còn ảnh hưởng bản gốc.",
  ],
),
# ------------------------------------------------------------------ 6
dict(
  id="object-pool", name="Object Pool", vn="Bể đối tượng", icon="🏊", freq=3,
  ref="https://gpcoder.com/4456-huong-dan-java-design-pattern-object-pool/",
  intent="Quản lý một <b>tập các đối tượng có thể tái sử dụng</b>. Thay vì tạo mới và huỷ liên tục, client <b>mượn</b> đối tượng từ bể và <b>trả lại</b> khi dùng xong.",
  analogy=("🚲", "Trạm <b>xe đạp công cộng</b>: bạn mượn xe, đạp xong trả lại trạm cho người sau dùng. Thành phố không cần sản xuất xe mới cho mỗi lượt đi; khi hết xe thì người đến sau phải chờ."),
  problem="""
<p>Một số đối tượng rất “đắt” để tạo: kết nối cơ sở dữ liệu (bắt tay TCP, xác thực), thread, socket, bộ đệm lớn, đối tượng đồ hoạ trong game (đạn, hiệu ứng nổ)…</p>
<ul>
<li>Tạo mới cho mỗi yêu cầu → <b>chậm</b> (mỗi kết nối DB có thể mất hàng trăm mili-giây).</li>
<li>Không giới hạn số lượng → <b>cạn tài nguyên</b> (CSDL chỉ cho phép N kết nối đồng thời).</li>
<li>Tạo/huỷ liên tục gây áp lực cho bộ thu gom rác (GC), làm game bị giật.</li>
</ul>""",
  solution="""
<p>Tạo lớp <b>Pool</b> giữ hai danh sách: đối tượng <i>rảnh</i> và đối tượng <i>đang dùng</i>.</p>
<ol>
<li><code>acquire()</code>: nếu có đối tượng rảnh → lấy ra; nếu chưa đạt giới hạn → tạo mới; nếu đã đầy → chờ, trả <code>null</code> hoặc ném ngoại lệ.</li>
<li><code>release(obj)</code>: <b>làm sạch (reset)</b> đối tượng rồi đưa về danh sách rảnh.</li>
</ol>
<div class="callout">💡 Object Pool <b>không</b> thuộc 23 mẫu gốc của GoF, nhưng rất phổ biến và được xếp vào nhóm Creational. Hai phương thức của Pool phải <code>synchronized</code> (hoặc dùng <code>BlockingQueue</code>) vì nhiều luồng cùng mượn/trả.</div>""",
  participants=[
    ("Reusable (DbConnection)", "Đối tượng tốn kém, có thể reset để tái sử dụng."),
    ("ObjectPool (ConnectionPool)", "Quản lý danh sách rảnh/đang dùng, giới hạn số lượng; thường là Singleton."),
    ("Client", "Mượn bằng acquire(), bắt buộc trả bằng release()."),
  ],
  uml=dict(
    boxes=[
      ("cl", "Client", None, [], ["main()"], 100, 50),
      ("p", "ConnectionPool", "ObjectPool", ["- maxSize: int", "- available: Deque", "- inUse: Set"],
       ["+ acquire(): DbConnection", "+ release(c: DbConnection)"], 400, 20),
      ("r", "DbConnection", "Reusable", ["- id: int"], ["+ query(sql)", "+ reset()"], 720, 40),
    ],
    notes=[("n1", "if (available không rỗng) lấy ra\nelse if (inUse < maxSize) tạo mới\nelse chờ / trả null", 400, 200)],
    edges=[("cl", "p", "assoc", "acquire / release"), ("p", "r", "agg", "0..maxSize"), ("n1", "p", "note", "")],
  ),
  code="06-object-pool.java",
  java_notes=[
    "Pool giới hạn 2 kết nối: lần mượn thứ 3 trả về <code>null</code> vì đã đầy.",
    "Sau khi <code>release(a)</code>, lần <code>acquire()</code> tiếp theo nhận lại <b>chính</b> đối tượng <code>a</code> (<code>d == a</code> là <code>true</code>).",
    "Dù gọi acquire 4 lần, chỉ <b>2</b> kết nối thực sự được tạo.",
    "<code>reset()</code> trước khi cho mượn lại là bước rất quan trọng — tránh rò rỉ trạng thái của người dùng trước.",
  ],
  pros=["Tăng hiệu năng rõ rệt khi đối tượng tốn kém để khởi tạo.", "Giới hạn và kiểm soát tài nguyên hệ thống.", "Giảm áp lực cho garbage collector."],
  cons=["Client <b>quên trả</b> đối tượng → pool cạn dần (leak).", "Đối tượng trả về chưa được reset sạch → lỗi khó tìm.", "Thêm độ phức tạp đồng bộ đa luồng.", "Với đối tượng nhẹ, pool còn chậm hơn tạo mới (JVM hiện đại cấp phát rất nhanh)."],
  when=["Đối tượng tốn kém để tạo: kết nối DB, thread, socket, buffer lớn.", "Số lượng đối tượng đồng thời cần bị giới hạn.", "Game: đạn, hạt (particle), kẻ địch xuất hiện và biến mất liên tục."],
  realworld=["Connection pool: HikariCP, Apache DBCP, C3P0", "Thread pool: <code>java.util.concurrent.ExecutorService</code> / <code>Executors.newFixedThreadPool()</code>", "<code>Integer.valueOf()</code> cache các số từ -128 đến 127"],
  related="Pool thường được cài đặt như Singleton. Khác với Flyweight: đối tượng trong Flyweight được dùng chung <b>đồng thời</b> và bất biến; đối tượng trong Pool chỉ được <b>một client</b> dùng tại một thời điểm.",
  exercises=[
    "Sửa <code>acquire()</code> để <b>chờ</b> tối đa 2 giây thay vì trả null (gợi ý: <code>wait(timeout)</code>/<code>notify()</code> hoặc <code>ArrayBlockingQueue.poll(timeout)</code>).",
    "Cho <code>DbConnection</code> implements <code>AutoCloseable</code> để <code>close()</code> tự trả về pool, dùng được với try-with-resources.",
    "Viết <code>BulletPool</code> cho game bắn máy bay: tối đa 50 viên đạn trên màn hình.",
  ],
),
]
