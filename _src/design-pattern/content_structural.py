# -*- coding: utf-8 -*-
"""Nội dung nhóm Structural (cấu trúc)."""

PATTERNS = [
# ------------------------------------------------------------------ 7
dict(
  id="adapter", name="Adapter", vn="Bộ chuyển đổi", icon="🔌", freq=5,
  ref="https://gpcoder.com/4483-huong-dan-java-design-pattern-adapter/",
  intent="Cho phép các lớp có <b>interface không tương thích</b> làm việc được với nhau, bằng cách bọc một lớp bằng một interface mà client mong đợi.",
  analogy=("🔌", "Laptop mua ở Mỹ có phích cắm chân dẹt, ổ điện ở Việt Nam là chân tròn. Bạn không sửa laptop, cũng không đục tường — chỉ cần một <b>cục chuyển đổi (adapter)</b> ở giữa."),
  problem="""
<p>Trạm thời tiết của lớp đang hiển thị nhiệt độ từ các cảm biến cài đặt interface <code>TemperatureSensor</code> (trả về <b>độ C</b>, có hàm <code>readCelsius()</code>).</p>
<p>Nhà trường mua thêm cảm biến nhập khẩu kèm thư viện <code>UsFahrenheitSensor</code> — trả về <b>độ F</b>, tên hàm là <code>getTempF()</code>. Ta <b>không thể sửa</b> thư viện này (không có mã nguồn, hoặc sửa sẽ mất khi cập nhật), cũng không muốn sửa <code>Dashboard</code> đang chạy tốt.</p>""",
  solution="""
<p>Tạo lớp <b>Adapter</b> cài đặt interface mà client cần (<code>TemperatureSensor</code>), bên trong giữ đối tượng cần chuyển đổi (<i>adaptee</i>). Mỗi lời gọi từ client được adapter <b>dịch</b> sang lời gọi tương ứng của adaptee — kèm chuyển đổi dữ liệu nếu cần (°F → °C).</p>
<table class="tbl">
<tr><th></th><th>Object Adapter</th><th>Class Adapter</th></tr>
<tr><td>Cơ chế</td><td>Composition — adapter <b>chứa</b> adaptee</td><td>Kế thừa — adapter <b>extends</b> adaptee</td></tr>
<tr><td>Bọc được lớp con của adaptee?</td><td>✓</td><td>✗</td></tr>
<tr><td>Ghi đè hành vi adaptee?</td><td>Khó</td><td>Dễ</td></tr>
<tr><td>Khuyên dùng</td><td>✓ (linh hoạt hơn)</td><td>Khi cần ghi đè</td></tr>
</table>""",
  participants=[
    ("Target (TemperatureSensor)", "Interface mà client mong đợi."),
    ("Adaptee (UsFahrenheitSensor)", "Lớp có sẵn với interface không tương thích."),
    ("Adapter (FahrenheitSensorAdapter)", "Cài đặt Target, chuyển lời gọi sang Adaptee."),
    ("Client (Dashboard)", "Chỉ làm việc với Target."),
  ],
  uml=dict(
    boxes=[
      ("cl", "Dashboard", "Client", [], ["+ show(s: TemperatureSensor)"], 120, 40),
      ("t", "TemperatureSensor", "interface", [], ["+ name(): String", "+ readCelsius(): double"], 450, 20),
      ("d", "Dht11Sensor", None, [], ["+ readCelsius(): double"], 300, 200),
      ("a", "FahrenheitSensorAdapter", "Adapter", ["- adaptee: UsFahrenheitSensor"], ["+ readCelsius(): double"], 580, 200),
      ("ad", "UsFahrenheitSensor", "Adaptee", [], ["+ getSerialNumber()", "+ getTempF(): double"], 890, 200),
    ],
    notes=[("n1", "return (adaptee_.getTempF() - 32) * 5 / 9;", 580, 350)],
    edges=[("cl", "t", "assoc", ""), ("d", "t", "impl", "", "tree"), ("a", "t", "impl", "", "tree"),
           ("a", "ad", "assoc", "adaptee"), ("n1", "a", "note", "")],
  ),
  code="07-adapter.java",
  java_notes=[
    "<code>Dashboard</code> và <code>UsFahrenheitSensor</code> <b>không bị sửa một dòng nào</b>.",
    "<code>FahrenheitSensorAdapter</code> (object adapter) vừa đổi tên hàm vừa đổi đơn vị: 95°F → 35°C.",
    "<code>FahrenheitClassAdapter</code> làm cùng việc bằng kế thừa — gọi thẳng <code>getTempF()</code> của lớp cha.",
    "Cả ba cảm biến nằm chung một <code>List&lt;TemperatureSensor&gt;</code> và được xử lý giống hệt nhau.",
  ],
  pros=["Tái sử dụng lớp có sẵn mà không sửa mã nguồn.", "Single Responsibility: logic chuyển đổi tách riêng khỏi nghiệp vụ.", "Open/Closed: thêm adapter mới không ảnh hưởng client."],
  cons=["Thêm lớp trung gian, tăng độ phức tạp.", "Đôi khi sửa trực tiếp lớp dịch vụ cho tương thích lại đơn giản hơn (nếu được phép)."],
  when=["Muốn dùng một lớp có sẵn (thư viện bên thứ ba, code cũ) nhưng interface không khớp.", "Tích hợp hệ thống cũ (legacy) với hệ thống mới.", "Chuẩn hoá nhiều nguồn dữ liệu khác định dạng về một interface chung."],
  realworld=["<code>Arrays.asList()</code> — biến mảng thành List", "<code>InputStreamReader</code> — chuyển byte stream thành character stream", "<code>Collections.enumeration()</code>, <code>Collections.list()</code>"],
  related="Bridge được thiết kế <b>từ đầu</b> để tách hai phần; Adapter dùng để <b>chữa cháy</b> cho các lớp đã có. Decorator giữ nguyên interface và thêm hành vi; Adapter đổi interface. Facade tạo interface mới cho cả hệ thống con; Adapter chỉ bọc một đối tượng.",
  exercises=[
    "Viết <code>JsonToXmlAdapter</code>: hệ thống cũ chỉ nhận XML, dịch vụ mới trả về JSON.",
    "Cảm biến Nhật trả về nhiệt độ Kelvin qua hàm <code>fetchKelvin()</code>. Viết adapter cho nó.",
    "Dùng <code>InputStreamReader</code> để đọc file UTF-8 và giải thích vai trò adapter của nó.",
  ],
),
# ------------------------------------------------------------------ 8
dict(
  id="bridge", name="Bridge", vn="Cầu nối", icon="🌉", freq=3,
  ref="https://gpcoder.com/4520-huong-dan-java-design-pattern-bridge/",
  intent="<b>Tách phần trừu tượng (abstraction) ra khỏi phần cài đặt (implementation)</b> để hai phần có thể phát triển độc lập với nhau.",
  analogy=("📺", "Điều khiển từ xa và thiết bị là hai thứ độc lập: điều khiển cơ bản, điều khiển có nút mute… đều điều khiển được TV, radio, quạt. Hãng làm remote và hãng làm TV không cần biết nhau, chỉ cần thống nhất “giao thức hồng ngoại” (cây cầu)."),
  problem="""
<p>Có 2 loại điều khiển (Cơ bản, Nâng cao) và 2 loại thiết bị (TV, Radio). Nếu dùng kế thừa thuần tuý, ta cần các lớp: <code>BasicTvRemote</code>, <code>BasicRadioRemote</code>, <code>AdvancedTvRemote</code>, <code>AdvancedRadioRemote</code>.</p>
<p>Thêm thiết bị Quạt → thêm 2 lớp. Thêm điều khiển Giọng nói → thêm 3 lớp nữa. Số lớp = <b>M × N</b> — “bùng nổ lớp”, và rất nhiều code trùng lặp.</p>""",
  solution="""
<p>Tách thành <b>hai cây phân cấp</b> riêng biệt và nối bằng <b>composition</b>:</p>
<ul>
<li><b>Abstraction</b> (<code>RemoteControl</code>): phần điều khiển cấp cao, giữ tham chiếu tới một <code>Device</code> — chính tham chiếu này là “cây cầu”.</li>
<li><b>Implementation</b> (<code>Device</code>): phần thao tác cấp thấp (bật, tắt, chỉnh âm lượng).</li>
</ul>
<p>Số lớp giờ chỉ là <b>M + N</b>. Mỗi bên mở rộng độc lập: thêm điều khiển mới không cần đụng tới thiết bị, và ngược lại.</p>
<div class="callout">💡 Nguyên lý cốt lõi: <b>“Ưu tiên composition hơn kế thừa”</b> (favor composition over inheritance).</div>""",
  participants=[
    ("Abstraction (RemoteControl)", "Định nghĩa logic điều khiển cấp cao, uỷ quyền công việc cho Implementor."),
    ("RefinedAbstraction (AdvancedRemote)", "Mở rộng Abstraction với chức năng mới."),
    ("Implementor (Device)", "Interface cho các thao tác cấp thấp."),
    ("ConcreteImplementor (Tv, Radio)", "Cài đặt cụ thể cho từng nền tảng/thiết bị."),
  ],
  uml=dict(
    boxes=[
      ("a", "RemoteControl", "Abstraction", ["# device: Device"], ["+ togglePower()", "+ volumeUp()", "+ volumeDown()"], 180, 50),
      ("ra", "AdvancedRemote", "RefinedAbstraction", [], ["+ mute()"], 180, 270),
      ("i", "Device", "interface", [], ["+ isEnabled(): boolean", "+ enable()", "+ disable()", "+ getVolume(): int", "+ setVolume(p)"], 600, 30),
      ("tv", "Tv", None, [], [], 520, 270),
      ("rd", "Radio", None, [], [], 680, 270),
    ],
    texts=[(180, 20, "PHÍA TRỪU TƯỢNG"), (600, 14, "PHÍA CÀI ĐẶT")],
    edges=[("ra", "a", "ext", ""), ("a", "i", "agg", "bridge"),
           ("tv", "i", "impl", "", "tree"), ("rd", "i", "impl", "", "tree")],
  ),
  code="08-bridge.java",
  java_notes=[
    "<code>RemoteControl</code> giữ <code>Device device</code> — mọi thao tác đều uỷ quyền qua tham chiếu này.",
    "<code>AdvancedRemote</code> thêm nút <code>mute()</code> mà không cần biết thiết bị là TV hay Radio.",
    "Ghép tuỳ ý lúc chạy: <code>new AdvancedRemote(new Radio())</code>, <code>new RemoteControl(new Tv())</code>…",
    "<code>BaseDevice</code> là lớp trừu tượng gom code chung của các thiết bị (không bắt buộc trong mẫu).",
  ],
  pros=["Tránh bùng nổ lớp M × N.", "Abstraction và Implementation mở rộng độc lập (Open/Closed).", "Có thể đổi implementation lúc chạy.", "Che giấu chi tiết nền tảng khỏi client."],
  cons=["Thiết kế phức tạp hơn khi áp dụng cho lớp vốn đã gắn kết chặt.", "Cần xác định đúng hai chiều biến đổi ngay từ đầu."],
  when=["Một lớp có hai (hoặc nhiều) chiều thay đổi độc lập (loại điều khiển × loại thiết bị; hình dạng × màu sắc; giao diện × hệ điều hành).", "Cần đổi implementation lúc chạy.", "Viết code đa nền tảng / đa driver."],
  realworld=["JDBC: <code>DriverManager</code>/<code>Connection</code> (abstraction) ↔ driver MySQL, PostgreSQL (implementation)", "SLF4J: API ghi log ↔ Logback, Log4j", "AWT: <code>java.awt.Component</code> ↔ peer của từng hệ điều hành"],
  related="Bridge thường được thiết kế từ đầu; Adapter dùng cho hệ thống đã có. Abstract Factory có thể dùng để tạo cặp Abstraction–Implementor phù hợp. Cấu trúc giống Strategy nhưng mục đích khác: Bridge tách cấu trúc, Strategy hoán đổi thuật toán.",
  exercises=[
    "Thêm thiết bị <code>SmartFan</code> và điều khiển <code>VoiceRemote</code> (nhận chuỗi lệnh “bật”, “to lên”). Đếm số lớp phải thêm.",
    "Áp dụng Bridge cho bài toán <code>Shape</code> (Tròn, Vuông) × <code>Renderer</code> (Vector, Pixel).",
    "Vẽ sơ đồ nếu KHÔNG dùng Bridge cho 3 điều khiển × 4 thiết bị.",
  ],
),
# ------------------------------------------------------------------ 9
dict(
  id="composite", name="Composite", vn="Hỗn hợp / Cây đối tượng", icon="🌳", freq=4,
  ref="https://gpcoder.com/4554-huong-dan-java-design-pattern-composite/",
  intent="Tổ chức các đối tượng thành <b>cấu trúc cây</b> để biểu diễn quan hệ bộ phận – toàn thể; cho phép client xử lý <b>đối tượng đơn lẻ và nhóm đối tượng theo cùng một cách</b>.",
  analogy=("🪖", "Một quân đội gồm các sư đoàn, sư đoàn gồm trung đoàn, … cuối cùng là từng người lính. Lệnh “tiến lên!” được truyền từ trên xuống — mỗi cấp chỉ việc truyền tiếp cho cấp dưới, không cần biết bên dưới có bao nhiêu người."),
  problem="""
<p>Cần tính dung lượng một thư mục dự án. Thư mục chứa file và các thư mục con; thư mục con lại chứa file và thư mục con nữa…</p>
<p>Nếu xử lý riêng từng loại: <code>if (item instanceof File) … else if (item instanceof Folder) { for … }</code> — code đầy kiểm tra kiểu, phải biết độ sâu của cây, và mỗi khi thêm loại phần tử mới (Shortcut, ZipFile) lại phải sửa mọi chỗ.</p>""",
  solution="""
<p>Định nghĩa interface chung <b>Component</b> (<code>FileSystemItem</code>) cho cả phần tử lá và phần tử chứa. Phần tử chứa (<b>Composite</b>, <code>Folder</code>) giữ danh sách <code>Component</code> con và cài đặt các phương thức bằng cách <b>đệ quy</b> gọi xuống các con rồi tổng hợp kết quả.</p>
<p>Client gọi <code>root.getSize()</code> — không cần biết <code>root</code> là một file hay cả một cây khổng lồ.</p>
<div class="callout">💡 Có hai cách đặt <code>add()/remove()</code>: trong <b>Component</b> (minh bạch — client đối xử mọi thứ như nhau, nhưng lá phải ném lỗi) hoặc chỉ trong <b>Composite</b> (an toàn kiểu — như ví dụ này).</div>""",
  participants=[
    ("Component (FileSystemItem)", "Interface chung cho mọi phần tử trong cây."),
    ("Leaf (FileItem)", "Phần tử không có con, thực hiện công việc thật."),
    ("Composite (Folder)", "Chứa các Component con, uỷ quyền công việc cho con và tổng hợp kết quả."),
    ("Client", "Làm việc với mọi phần tử qua Component."),
  ],
  uml=dict(
    boxes=[
      ("cl", "Client", None, [], [], 110, 50),
      ("c", "FileSystemItem", "interface", [], ["+ getName(): String", "+ getSize(): int", "+ print(indent)"], 400, 20),
      ("l", "FileItem", "Leaf", ["- name", "- size: int"], ["+ getSize(): int"], 270, 220),
      ("f", "Folder", "Composite", ["- children: List<FileSystemItem>"], ["+ add(item)", "+ remove(item)", "+ getSize(): int"], 560, 220),
    ],
    notes=[("n1", "int total = 0;\nfor (auto& c : children_)\n    total += c->getSize();\nreturn total;", 840, 230)],
    edges=[("cl", "c", "assoc", ""), ("l", "c", "impl", "", "tree"), ("f", "c", "impl", "", "tree"),
           ("f", "c", "agg", "0..*", [(720, 255), (720, 65)]), ("n1", "f", "note", "")],
  ),
  extra="composite",
  code="09-composite.java",
  java_notes=[
    "<code>Folder.getSize()</code> gọi <code>getSize()</code> của từng con — con là file thì trả ngay, con là thư mục thì lại đệ quy tiếp.",
    "<code>print()</code> cũng đệ quy, mỗi cấp thụt lề thêm 3 dấu cách → in ra cây thư mục đẹp mắt.",
    "Client chỉ gọi <code>root.print(\"\")</code> và <code>root.getSize()</code>; có thể gọi trên bất kỳ nút nào (ví dụ <code>docs.getSize()</code>).",
  ],
  pros=["Làm việc với cấu trúc cây phức tạp một cách thuận tiện nhờ đa hình và đệ quy.", "Open/Closed: thêm loại phần tử mới không sửa code client.", "Client đơn giản hơn — không cần phân biệt lá và nhánh."],
  cons=["Khó giới hạn loại phần tử con (ví dụ: thư mục chỉ chứa ảnh) — phải kiểm tra lúc chạy.", "Interface chung có thể trở nên quá tổng quát."],
  when=["Dữ liệu có cấu trúc cây: thư mục, menu đa cấp, sơ đồ tổ chức, cây DOM HTML, bản vẽ gồm nhóm hình.", "Muốn client xử lý đối tượng đơn và nhóm như nhau."],
  realworld=["<code>java.awt.Container</code> chứa các <code>Component</code> (một Panel chứa Button và Panel khác)", "Cây DOM: <code>org.w3c.dom.Node</code>", "JavaFX: <code>Parent</code> / <code>Node</code>"],
  related="Builder dùng để tạo cây Composite; Iterator dùng để duyệt cây; Visitor thực hiện thao tác trên toàn cây; Chain of Responsibility thường chạy dọc theo quan hệ cha – con của Composite. Decorator có cấu trúc giống nhưng chỉ có một con.",
  exercises=[
    "Thêm phương thức <code>int countFiles()</code> đếm tổng số file.",
    "Thêm <code>find(String name)</code> trả về đường dẫn đầy đủ của file nếu tìm thấy.",
    "Áp dụng Composite cho menu nhà hàng: <code>Menu</code> chứa <code>MenuItem</code> và <code>Menu</code> con; tính tổng giá combo.",
  ],
),
# ------------------------------------------------------------------ 10
dict(
  id="decorator", name="Decorator", vn="Người trang trí", icon="🎁", freq=5,
  ref="https://gpcoder.com/4574-huong-dan-java-design-pattern-decorator/",
  intent="<b>Gắn thêm hành vi mới cho đối tượng một cách động</b> bằng cách bọc nó trong các đối tượng “trang trí” có cùng interface — một giải pháp linh hoạt thay cho kế thừa.",
  analogy=("🧥", "Trời lạnh bạn mặc áo len; mưa thì khoác thêm áo mưa bên ngoài. Mỗi lớp áo “bọc” lớp trong và thêm một tính năng (ấm, chống nước) — bạn tháo/mặc từng lớp tuỳ ý, không phải “trở thành” một người khác."),
  problem="""
<p>Quán trà sữa có nhiều đồ uống gốc và hàng chục loại topping (trân châu, kem cheese, pudding…), khách được thêm bao nhiêu tuỳ thích, thêm 2 lần cùng một loại cũng được.</p>
<p>Dùng kế thừa: <code>MilkTeaWithPearl</code>, <code>MilkTeaWithPearlAndCheese</code>, <code>GreenTeaWithPuddingAndDoublePearl</code>… → <b>bùng nổ tổ hợp</b>. Thêm biến boolean <code>hasPearl</code>, <code>hasCheese</code> vào lớp cha → mỗi topping mới phải sửa lớp cha, và không xử lý được “thêm 2 lần”.</p>""",
  solution="""
<p>Tạo lớp <b>Decorator</b> vừa <b>cài đặt</b> interface <code>Drink</code> vừa <b>chứa</b> một <code>Drink</code> bên trong. Mỗi decorator uỷ quyền lời gọi cho đối tượng bên trong rồi <b>thêm</b> hành vi của mình (cộng giá, nối mô tả).</p>
<p>Vì decorator cũng là một <code>Drink</code>, ta có thể <b>bọc lồng nhau nhiều lớp</b>: <code>new Pearl(new CheeseFoam(new MilkTea()))</code>. Client vẫn thấy một <code>Drink</code> bình thường.</p>""",
  participants=[
    ("Component (Drink)", "Interface chung cho đối tượng gốc và decorator."),
    ("ConcreteComponent (MilkTea)", "Đối tượng gốc được bọc."),
    ("BaseDecorator (ToppingDecorator)", "Giữ tham chiếu tới Component bên trong, mặc định uỷ quyền mọi lời gọi."),
    ("ConcreteDecorator (Pearl…)", "Thêm hành vi trước/sau khi uỷ quyền."),
  ],
  uml=dict(
    boxes=[
      ("c", "Drink", "interface", [], ["+ getDescription(): String", "+ cost(): int"], 330, 20),
      ("m", "MilkTea", None, [], ["+ getDescription()", "+ cost()"], 130, 200),
      ("d", "ToppingDecorator", "abstract", ["# inner: Drink"], ["+ getDescription()", "+ cost()"], 470, 200),
      ("p", "Pearl", None, [], ["+ getDescription()", "+ cost()"], 370, 380),
      ("cf", "CheeseFoam", None, [], ["+ getDescription()", "+ cost()"], 580, 380),
    ],
    notes=[("n1", "return inner_->cost() + 5000;", 130, 400)],
    edges=[("m", "c", "impl", "", "tree"), ("d", "c", "impl", "", "tree"),
           ("d", "c", "agg", "inner", [(660, 245), (660, 60)]),
           ("p", "d", "ext", "", "tree"), ("cf", "d", "ext", "", "tree"), ("n1", "p", "note", "")],
  ),
  extra="decorator",
  code="10-decorator.java",
  java_notes=[
    "<code>ToppingDecorator</code> vừa <i>là</i> Drink (implements) vừa <i>có</i> Drink (field <code>inner</code>) — hai mối quan hệ này là “chữ ký” của Decorator.",
    "Lời gọi <code>cost()</code> đi xuyên qua các lớp vỏ: Pearl → CheeseFoam → MilkTea, rồi cộng dồn ngược ra: 25 000 + 10 000 + 5 000.",
    "Bọc <code>Pearl</code> hai lần hoàn toàn hợp lệ — điều mà kế thừa không làm được.",
    "Thứ tự bọc quyết định thứ tự xuất hiện trong mô tả.",
  ],
  pros=["Thêm/bớt trách nhiệm lúc chạy, kết hợp tuỳ ý.", "Tránh bùng nổ lớp con.", "Single Responsibility: mỗi decorator chỉ lo một tính năng."],
  cons=["Khó gỡ một decorator cụ thể ra khỏi giữa chồng bọc.", "Hành vi có thể phụ thuộc thứ tự bọc.", "Nhiều đối tượng nhỏ, khó debug; code khởi tạo dài."],
  when=["Cần thêm chức năng cho đối tượng lúc chạy mà không ảnh hưởng đối tượng khác cùng lớp.", "Kế thừa không khả thi (lớp <code>final</code>) hoặc gây bùng nổ tổ hợp.", "Các tính năng có thể bật/tắt độc lập: nén, mã hoá, đệm, ghi log…"],
  realworld=["<code>java.io</code>: <code>new BufferedReader(new InputStreamReader(new FileInputStream(f)))</code>", "<code>Collections.unmodifiableList()</code>, <code>Collections.synchronizedList()</code>", "Servlet: <code>HttpServletRequestWrapper</code>"],
  related="Adapter đổi interface, Decorator giữ nguyên interface và thêm hành vi. Proxy cũng bọc đối tượng nhưng thường tự quản lý vòng đời đối tượng thật và không xếp chồng. Composite có nhiều con, Decorator chỉ có một. Strategy thay “ruột” của đối tượng, Decorator thay “vỏ”.",
  exercises=[
    "Thêm topping <code>Jelly</code> (+6 000đ) và size <code>Large</code> (nhân giá × 1.3).",
    "Viết <code>DataSource</code> với các decorator <code>EncryptionDecorator</code> (đảo ngược chuỗi) và <code>CompressionDecorator</code> (bỏ dấu cách).",
    "Python: viết hàm decorator <code>@retry(3)</code> tự gọi lại hàm đọc cảm biến khi bị lỗi. So sánh cú pháp <code>@</code> của Python với mẫu Decorator.",
  ],
),
# ------------------------------------------------------------------ 11
dict(
  id="facade", name="Facade", vn="Mặt tiền", icon="🏠", freq=5,
  ref="https://gpcoder.com/4604-huong-dan-java-design-pattern-facade/",
  intent="Cung cấp một <b>interface đơn giản, thống nhất</b> cho một tập hợp các interface phức tạp trong một hệ thống con.",
  analogy=("☎️", "Gọi tổng đài đặt đồ ăn: bạn chỉ nói “1 phần cơm gà, giao tới trường”. Nhân viên tổng đài lo việc báo bếp, thanh toán, gọi shipper, đóng gói… Tổng đài chính là “mặt tiền” của cả hệ thống phía sau."),
  problem="""
<p>Ngôi nhà thông minh có đèn, điều hoà, rèm, máy chiếu, loa… Để xem phim, chương trình phải gọi đúng thứ tự 7 thao tác trên 5 hệ thống khác nhau. Mỗi nơi muốn “bật chế độ xem phim” (app điện thoại, nút bấm, trợ lý giọng nói) lại lặp lại đoạn code dài này.</p>
<p>Client bị <b>phụ thuộc chặt</b> vào mọi chi tiết của hệ thống con: thay máy chiếu loại khác → sửa mọi nơi.</p>""",
  solution="""
<p>Tạo lớp <b>Facade</b> (<code>SmartHomeFacade</code>) giữ tham chiếu tới các hệ thống con và cung cấp vài phương thức cấp cao (<code>startMovieMode()</code>, <code>leaveHome()</code>). Facade biết cần gọi ai, theo thứ tự nào.</p>
<p>Client chỉ nói chuyện với Facade. Hệ thống con <b>không biết</b> Facade tồn tại và vẫn có thể được dùng trực tiếp khi cần điều khiển chi tiết.</p>
<div class="callout">💡 Facade gắn liền với <b>Nguyên lý Demeter</b> (“chỉ nói chuyện với bạn thân”): giảm số lượng đối tượng mà client phải biết.</div>""",
  participants=[
    ("Facade (SmartHomeFacade)", "Biết hệ thống con nào xử lý yêu cầu nào; điều phối các lời gọi."),
    ("Subsystem classes (Lights, Projector…)", "Thực hiện công việc thật; không biết tới Facade."),
    ("Client", "Dùng Facade thay vì gọi trực tiếp hệ thống con."),
  ],
  uml=dict(
    boxes=[
      ("cl", "Client", None, [], [], 400, 10),
      ("f", "SmartHomeFacade", "Facade", [], ["+ startMovieMode(movie)", "+ leaveHome()"], 400, 100),
      ("s1", "Lights", None, [], ["+ dim(p)", "+ off()"], 80, 290),
      ("s2", "AirConditioner", None, [], ["+ setTemperature(c)", "+ off()"], 250, 290),
      ("s3", "Curtains", None, [], ["+ close()"], 410, 290),
      ("s4", "Projector", None, [], ["+ on()", "+ setInput(s)", "+ off()"], 560, 290),
      ("s5", "SoundSystem", None, [], ["+ on()", "+ setVolume(v)", "+ off()"], 720, 290),
    ],
    groups=[(10, 262, 800, 130, "Hệ thống con (subsystem)")],
    edges=[("cl", "f", "assoc", ""), ("f", "s1", "assoc", ""), ("f", "s2", "assoc", ""), ("f", "s3", "assoc", ""),
           ("f", "s4", "assoc", ""), ("f", "s5", "assoc", "")],
  ),
  code="11-facade.java",
  java_notes=[
    "<code>main()</code> chỉ gọi 2 phương thức của Facade, trong khi Facade gọi 11 thao tác trên 5 hệ thống con.",
    "Thứ tự hợp lý (kéo rèm trước khi giảm đèn, bật máy chiếu trước khi chọn nguồn) được đóng gói một chỗ.",
    "Các lớp hệ thống con hoàn toàn không biết <code>SmartHomeFacade</code> tồn tại.",
  ],
  pros=["Cô lập client khỏi sự phức tạp của hệ thống con.", "Giảm phụ thuộc (loose coupling) — thay đổi hệ thống con ít ảnh hưởng client.", "Dễ dùng, dễ học cho người mới."],
  cons=["Facade có thể phình to thành “God object” ôm mọi thứ.", "Che giấu quá kỹ khiến người dùng nâng cao khó tuỳ biến (nên vẫn cho phép truy cập trực tiếp hệ thống con)."],
  when=["Cần interface đơn giản cho một hệ thống con phức tạp.", "Muốn phân tầng hệ thống: mỗi tầng giao tiếp với tầng khác qua một facade.", "Bọc thư viện bên thứ ba phức tạp để dễ thay thế sau này."],
  realworld=["<code>javax.faces.context.FacesContext</code>", "SLF4J <code>LoggerFactory</code>", "Tầng Service trong kiến trúc MVC/Spring — một facade cho nhiều Repository", "Thư viện <code>Arduino.h</code>: <code>digitalWrite()</code> che giấu thao tác thanh ghi phức tạp"],
  related="Adapter bọc <b>một</b> đối tượng và đổi interface; Facade định nghĩa interface mới cho <b>cả hệ thống con</b>. Mediator cũng điều phối nhiều đối tượng, nhưng các đối tượng biết Mediator và giao tiếp hai chiều. Facade thường là Singleton.",
  exercises=[
    "Thêm chế độ <code>goodNight()</code>: tắt hết, đặt điều hoà 27°C, bật đèn ngủ 5%.",
    "Viết <code>OrderFacade.placeOrder()</code> che giấu các bước: kiểm tra kho, tính tiền, thanh toán, tạo vận đơn.",
    "Tìm trong thư viện Arduino một hàm đóng vai trò facade và giải thích nó che giấu điều gì.",
  ],
),
# ------------------------------------------------------------------ 12
dict(
  id="flyweight", name="Flyweight", vn="Hạng ruồi / Dùng chung", icon="🪶", freq=2,
  ref="https://gpcoder.com/4626-huong-dan-java-design-pattern-flyweight/",
  intent="<b>Tiết kiệm bộ nhớ</b> khi có số lượng rất lớn đối tượng giống nhau, bằng cách <b>chia sẻ phần trạng thái chung</b> giữa chúng thay vì mỗi đối tượng giữ một bản riêng.",
  analogy=("🔤", "Một cuốn sách 300 trang có hàng trăm nghìn ký tự, nhưng nhà in chỉ cần một bộ <b>khuôn chữ</b> cho mỗi chữ cái. Chữ “a” ở trang 1 và trang 200 dùng chung khuôn, chỉ khác <i>vị trí</i> in."),
  problem="""
<p>Game cần vẽ một khu rừng 100 000 cây. Mỗi đối tượng <code>Tree</code> chứa toạ độ (x, y) <b>và</b> dữ liệu loại cây: tên, màu, texture, mô hình 3D… (giả sử ~2 KB).</p>
<p>100 000 × 2 KB ≈ <b>200 MB</b> RAM — trong khi thực tế chỉ có 3 loại cây! Phần lớn bộ nhớ chứa dữ liệu <b>giống hệt nhau</b> bị nhân bản.</p>""",
  solution="""
<p>Tách trạng thái của đối tượng thành hai phần:</p>
<ul>
<li><b>Intrinsic (nội tại)</b>: dữ liệu chung, không đổi (tên, màu, texture) → đưa vào đối tượng <b>Flyweight</b> (<code>TreeType</code>), được <b>dùng chung</b>.</li>
<li><b>Extrinsic (ngoại tại)</b>: dữ liệu riêng của từng đối tượng (x, y) → giữ trong đối tượng ngữ cảnh nhỏ gọn (<code>Tree</code>) hoặc truyền vào khi gọi phương thức.</li>
</ul>
<p>Một <b>Flyweight Factory</b> quản lý bộ đệm: yêu cầu loại cây nào thì trả về bản đã có, chỉ tạo mới khi chưa tồn tại.</p>
<div class="callout warn">⚠️ Flyweight <b>phải bất biến</b> (immutable) — vì nhiều đối tượng dùng chung, sửa một chỗ sẽ ảnh hưởng tất cả.</div>""",
  participants=[
    ("Flyweight (TreeType)", "Chứa trạng thái intrinsic, bất biến, dùng chung."),
    ("FlyweightFactory (TreeFactory)", "Tạo và cache flyweight, đảm bảo không trùng lặp."),
    ("Context (Tree)", "Chứa trạng thái extrinsic + tham chiếu tới flyweight."),
    ("Client (Forest)", "Tính toán/lưu trạng thái extrinsic, lấy flyweight qua factory."),
  ],
  uml=dict(
    boxes=[
      ("cl", "Forest", "Client", ["- trees: List<Tree>"], ["+ plantTree(x, y, name, color)"], 140, 20),
      ("ctx", "Tree", "Context", ["- x, y: int  (extrinsic)", "- type: TreeType"], ["+ draw()"], 140, 230),
      ("fac", "TreeFactory", "FlyweightFactory", ["- cache: Map<String,TreeType>"], ["+ get(name, color): TreeType"], 520, 20),
      ("fw", "TreeType", "Flyweight", ["- name, color  (intrinsic)", "- texture…"], ["+ draw(x, y)"], 520, 230),
    ],
    edges=[("cl", "ctx", "comp", "100 000"), ("ctx", "fw", "assoc", "dùng chung"),
           ("fac", "fw", "agg", "cache"), ("cl", "fac", "dep", "get()")],
  ),
  code="12-flyweight.java",
  java_notes=[
    "100 000 cây được trồng nhưng <code>TreeFactory.count()</code> chỉ là <b>3</b>.",
    "<code>computeIfAbsent</code> giúp factory chỉ tạo <code>TreeType</code> khi khoá chưa có trong cache.",
    "Ước tính bộ nhớ giảm từ ~196 MB xuống dưới 1 MB (mỗi <code>Tree</code> chỉ còn giữ 2 số nguyên + 1 tham chiếu).",
    "<code>Random(42)</code> với seed cố định giúp mỗi lần chạy cho cùng kết quả — thuận tiện khi kiểm tra.",
  ],
  pros=["Giảm mạnh bộ nhớ khi có rất nhiều đối tượng tương tự."],
  cons=["Code phức tạp hơn — phải tách trạng thái.", "Có thể tốn CPU hơn nếu phải tính lại trạng thái extrinsic mỗi lần dùng.", "Chỉ đáng dùng khi số lượng đối tượng thực sự lớn."],
  when=["Ứng dụng tạo cực nhiều đối tượng và đang thiếu RAM.", "Phần lớn trạng thái của đối tượng có thể đưa ra ngoài (extrinsic).", "Ví dụ: ký tự trong trình soạn thảo, hạt/viên đạn/cây trong game, ô bản đồ (tile)."],
  realworld=["<code>String</code> pool / <code>String.intern()</code>", "<code>Integer.valueOf(int)</code>, <code>Boolean.valueOf()</code>, <code>Character.valueOf()</code> cache", "Font glyph trong các trình soạn thảo văn bản"],
  related="Factory của Flyweight thường dùng Singleton. Các nút lá của Composite có thể là Flyweight để tiết kiệm bộ nhớ. Khác Singleton: Flyweight có nhiều thể hiện (mỗi loại một), và luôn bất biến.",
  exercises=[
    "Đổi số loại cây thành 10 và số cây thành 1 000 000. Quan sát số TreeType và mức bộ nhớ ước tính.",
    "Chứng minh <code>Integer.valueOf(100) == Integer.valueOf(100)</code> là <code>true</code> nhưng với 1000 là <code>false</code>. Giải thích.",
    "Thiết kế Flyweight cho trình soạn thảo: mỗi ký tự có font, cỡ chữ (dùng chung) và vị trí dòng/cột (riêng).",
  ],
),
# ------------------------------------------------------------------ 13
dict(
  id="proxy", name="Proxy", vn="Người đại diện", icon="🛡️", freq=4,
  ref="https://gpcoder.com/4644-huong-dan-java-design-pattern-proxy/",
  intent="Cung cấp một <b>vật thay thế (đại diện)</b> cho đối tượng khác để <b>kiểm soát việc truy cập</b> tới nó — cho phép làm gì đó trước hoặc sau khi yêu cầu tới được đối tượng thật.",
  analogy=("💳", "Thẻ ngân hàng là “proxy” của số tiền trong tài khoản: dùng được ở mọi nơi chấp nhận thanh toán như tiền mặt, nhưng còn kiểm tra mã PIN, hạn mức, ghi lịch sử giao dịch — trước khi tiền thật được chuyển đi."),
  problem="""
<p>Một số đối tượng cần được “canh cửa”:</p>
<ul>
<li>Ảnh 4K rất nặng — tải tất cả lúc mở album thì chậm, trong khi người dùng có thể không bao giờ xem tới.</li>
<li>Dịch vụ điểm số — học sinh chỉ được xem, giáo viên mới được sửa.</li>
<li>Truy vấn cơ sở dữ liệu chậm — cùng một câu hỏi lặp lại nhiều lần.</li>
</ul>
<p>Nhét các logic này vào chính lớp gốc sẽ làm nó phình to và vi phạm Single Responsibility; bắt client tự kiểm tra thì lặp code khắp nơi.</p>""",
  solution="""
<p>Tạo lớp <b>Proxy</b> cài đặt <b>cùng interface</b> với đối tượng thật và giữ tham chiếu tới nó. Client dùng proxy như dùng đối tượng thật; proxy làm thêm việc của mình rồi mới (hoặc không) chuyển yêu cầu.</p>
<table class="tbl">
<tr><th>Loại proxy</th><th>Mục đích</th></tr>
<tr><td><b>Virtual proxy</b></td><td>Khởi tạo trễ đối tượng nặng (lazy loading)</td></tr>
<tr><td><b>Protection proxy</b></td><td>Kiểm tra quyền truy cập</td></tr>
<tr><td><b>Caching proxy</b></td><td>Lưu kết quả để trả nhanh lần sau</td></tr>
<tr><td><b>Remote proxy</b></td><td>Đại diện cho đối tượng ở máy khác (RMI, gRPC)</td></tr>
<tr><td><b>Logging proxy</b></td><td>Ghi lại lịch sử các lời gọi</td></tr>
</table>""",
  participants=[
    ("Subject (Image)", "Interface chung của Proxy và RealSubject."),
    ("RealSubject (RealImage)", "Đối tượng thật thực hiện công việc chính."),
    ("Proxy (LazyImageProxy)", "Giữ tham chiếu tới RealSubject, kiểm soát truy cập, có thể tạo/huỷ RealSubject."),
    ("Client", "Làm việc với Subject, không phân biệt proxy hay đối tượng thật."),
  ],
  uml=dict(
    boxes=[
      ("cl", "Client", None, [], [], 110, 50),
      ("s", "Image", "interface", [], ["+ display()"], 400, 30),
      ("r", "RealImage", "RealSubject", ["- file: String"], ["+ RealImage(file)", "+ display()"], 260, 210),
      ("p", "LazyImageProxy", "Proxy", ["- file: String", "- real: RealImage"], ["+ display()"], 560, 210),
    ],
    notes=[("n1", "if (!real_)\n    real_ = std::make_unique<RealImage>(file_);\nreal_->display();", 560, 370)],
    edges=[("cl", "s", "assoc", ""), ("r", "s", "impl", "", "tree"), ("p", "s", "impl", "", "tree"),
           ("p", "r", "assoc", "real"), ("n1", "p", "note", "")],
  ),
  code="13-proxy.java",
  java_notes=[
    "Tạo <code>LazyImageProxy</code> gần như không tốn gì; ảnh chỉ thực sự được tải ở lần <code>display()</code> đầu tiên.",
    "<code>ScoreServiceProxy</code> kết hợp hai vai trò: <b>caching</b> (lần gọi thứ 2 không truy vấn DB) và <b>protection</b> (học sinh bị chặn khi sửa điểm).",
    "Sau khi cập nhật điểm, proxy xoá cache để lần đọc sau lấy dữ liệu mới — đây là vấn đề “cache invalidation” kinh điển.",
  ],
  pros=["Kiểm soát đối tượng thật mà client không hay biết.", "Quản lý vòng đời đối tượng thật (lazy).", "Open/Closed: thêm proxy mới không sửa đối tượng thật hay client."],
  cons=["Thêm tầng trung gian → phản hồi có thể chậm hơn.", "Tăng số lượng lớp."],
  when=["Lazy initialization cho đối tượng nặng.", "Kiểm soát quyền truy cập.", "Cache, ghi log, đếm số lần gọi.", "Làm việc với đối tượng ở xa (remote)."],
  realworld=["<code>java.lang.reflect.Proxy</code> — dynamic proxy", "Spring AOP: <code>@Transactional</code>, <code>@Cacheable</code> hoạt động nhờ proxy", "Hibernate lazy loading của entity", "Java RMI stub"],
  related="Adapter đổi interface; Proxy giữ nguyên interface; Decorator mở rộng interface/hành vi. Decorator do client chủ động xếp chồng; Proxy thường tự quản lý đối tượng thật. Facade giống Proxy ở chỗ đứng chắn trước đối tượng phức tạp, nhưng Facade có interface khác.",
  exercises=[
    "Viết <code>LoggingProxy</code> cho <code>ScoreService</code> in ra thời gian thực thi mỗi lời gọi.",
    "Python: dùng <code>__getattr__</code> viết một proxy tổng quát ghi log mọi lời gọi phương thức của đối tượng bất kỳ.",
    "Thiết kế proxy cho cảm biến ESP32 ở xa: chỉ gọi HTTP thật nếu dữ liệu cache cũ hơn 5 giây.",
  ],
),
]
