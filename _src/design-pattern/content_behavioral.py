# -*- coding: utf-8 -*-
"""Nội dung nhóm Behavioral (hành vi / tương tác)."""

PATTERNS = [
# ------------------------------------------------------------------ 14
dict(
  id="chain-of-responsibility", name="Chain of Responsibility", vn="Chuỗi trách nhiệm", icon="⛓️", freq=3,
  ref="https://gpcoder.com/4665-huong-dan-java-design-pattern-chain-of-responsibility/",
  intent="Chuyển yêu cầu dọc theo <b>một chuỗi các bộ xử lý</b>. Mỗi bộ xử lý quyết định <b>tự xử lý</b> hoặc <b>chuyển tiếp</b> cho mắt xích kế tiếp — người gửi không cần biết ai sẽ xử lý.",
  analogy=("📞", "Gọi tổng đài hỗ trợ: tổng đài tự động trả lời câu hỏi đơn giản → không được thì chuyển nhân viên trực → khó nữa thì chuyển kỹ sư. Bạn chỉ gọi một số, yêu cầu tự “trôi” tới đúng người."),
  problem="""
<p>Đơn xin nghỉ của giáo viên cần được duyệt theo thẩm quyền: ≤ 2 ngày tổ trưởng duyệt, ≤ 5 ngày hiệu phó, ≤ 30 ngày hiệu trưởng.</p>
<p>Viết một hàm với chuỗi <code>if/else</code> dài thì: mỗi khi đổi quy trình (thêm cấp “Trưởng phòng GD”, đổi ngưỡng) phải sửa hàm đó; người gửi đơn bị gắn chặt với toàn bộ bộ máy duyệt; không thể cấu hình quy trình khác nhau cho từng trường.</p>""",
  solution="""
<p>Mỗi cấp duyệt là một đối tượng <b>Handler</b> riêng, có tham chiếu <code>next</code> tới cấp kế tiếp. Khi nhận yêu cầu, handler kiểm tra: đủ thẩm quyền thì xử lý, không thì gọi <code>next.handle()</code>.</p>
<p>Client chỉ gửi yêu cầu vào <b>đầu chuỗi</b>. Chuỗi được lắp ráp lúc chạy, có thể thêm/bớt/đổi thứ tự mắt xích mà không sửa các handler.</p>
<div class="callout">💡 Có hai biến thể: (1) <b>dừng khi có người xử lý</b> — như ví dụ duyệt đơn; (2) <b>mọi mắt xích đều xử lý</b> rồi chuyển tiếp — như chuỗi filter/middleware (xác thực → ghi log → nén → …).</div>""",
  participants=[
    ("Handler (Approver)", "Khai báo interface xử lý và giữ liên kết tới handler kế tiếp."),
    ("ConcreteHandler (TeamLeader…)", "Xử lý yêu cầu nếu có thể, ngược lại chuyển tiếp."),
    ("Client", "Lắp chuỗi và gửi yêu cầu tới handler đầu tiên."),
  ],
  uml=dict(
    boxes=[
      ("cl", "Client", None, [], [], 110, 50),
      ("h", "Approver", "abstract", ["- next: Approver"], ["+ setNext(a): Approver", "+ handle(r: LeaveRequest)", "# canApprove(r): boolean", "# role(): String"], 420, 20),
      ("h1", "TeamLeader", None, [], ["# canApprove(r)"], 240, 250),
      ("h2", "VicePrincipal", None, [], ["# canApprove(r)"], 420, 250),
      ("h3", "Principal", None, [], ["# canApprove(r)"], 600, 250),
    ],
    edges=[("cl", "h", "assoc", ""), ("h1", "h", "ext", "", "tree"), ("h2", "h", "ext", "", "tree"), ("h3", "h", "ext", "", "tree"),
           ("h", "h", "agg", "next")],
  ),
  extra="chain",
  code="14-chain-of-responsibility.java",
  java_notes=[
    "<code>setNext()</code> trả về chính handler kế tiếp nên lắp chuỗi được bằng một câu lệnh nối tiếp.",
    "<code>handle()</code> được khai báo <code>final</code> — lớp con chỉ định nghĩa <i>điều kiện</i> (<code>canApprove</code>), không thể phá vỡ logic chuyển tiếp.",
    "Đơn 45 ngày đi hết chuỗi mà không ai duyệt → cần xử lý trường hợp “rơi khỏi chuỗi”.",
    "<code>LeaveRequest</code> dùng <code>record</code> (Java 16+) — gọn và bất biến.",
  ],
  pros=["Giảm phụ thuộc giữa người gửi và người nhận.", "Thêm/bớt/sắp xếp lại handler linh hoạt lúc chạy.", "Single Responsibility: mỗi handler một nhiệm vụ."],
  cons=["Không đảm bảo yêu cầu luôn được xử lý.", "Chuỗi dài khó debug, có thể ảnh hưởng hiệu năng."],
  when=["Nhiều đối tượng có thể xử lý một yêu cầu và handler cụ thể chỉ được biết lúc chạy.", "Quy trình phê duyệt nhiều cấp.", "Chuỗi bộ lọc / middleware: xác thực, phân quyền, ghi log, nén dữ liệu."],
  realworld=["<code>javax.servlet.Filter</code> / <code>FilterChain.doFilter()</code>", "Spring Security filter chain", "<code>java.util.logging.Logger</code> chuyển log lên logger cha", "Cơ chế nổi bọt sự kiện (event bubbling) trong DOM"],
  related="Thường kết hợp với Composite: yêu cầu chuyển từ con lên cha. Command có thể làm đối tượng yêu cầu. Decorator có cấu trúc gần giống nhưng mọi decorator đều xử lý và không được “cắt ngang” chuỗi.",
  exercises=[
    "Thêm cấp <code>EducationDepartment</code> duyệt ≤ 90 ngày ở cuối chuỗi.",
    "Viết chuỗi middleware cho request HTTP: <code>AuthHandler → RateLimitHandler → LogHandler</code>, trong đó mỗi handler có thể chặn hoặc cho qua.",
    "Cài đặt chuỗi bằng <code>List&lt;Approver&gt;</code> duyệt tuần tự thay vì con trỏ <code>next</code>. So sánh hai cách.",
  ],
),
# ------------------------------------------------------------------ 15
dict(
  id="command", name="Command", vn="Mệnh lệnh", icon="🎮", freq=4,
  ref="https://gpcoder.com/4686-huong-dan-java-design-pattern-command/",
  intent="<b>Đóng gói một yêu cầu thành một đối tượng</b>, nhờ đó có thể truyền yêu cầu như tham số, xếp hàng, ghi lịch sử và <b>hoàn tác (undo)</b>.",
  analogy=("🧾", "Ở nhà hàng, bồi bàn ghi món vào <b>phiếu order</b> rồi đặt lên quầy. Đầu bếp đọc phiếu và nấu. Bồi bàn không cần biết nấu ăn; phiếu có thể xếp hàng, huỷ, hay lưu lại để thống kê."),
  problem="""
<p>Chiếc điều khiển nhà thông minh có nhiều nút. Nếu mỗi nút gọi thẳng <code>light.on()</code>, <code>fan.setSpeed(3)</code>… thì:</p>
<ul>
<li>Điều khiển bị gắn chặt với mọi loại thiết bị; muốn gán lại chức năng cho nút phải sửa code.</li>
<li>Không có cách nào <b>hoàn tác</b> thao tác vừa làm, hay <b>ghi lại macro</b> để phát lại.</li>
<li>Cùng một hành động (bật đèn) có thể đến từ nút bấm, giọng nói, lịch hẹn giờ → code bị lặp.</li>
</ul>""",
  solution="""
<p>Biến mỗi hành động thành một đối tượng cài đặt interface <code>Command</code> với <code>execute()</code> (và thường thêm <code>undo()</code>). Đối tượng command chứa sẵn: <b>ai</b> thực hiện (receiver), <b>làm gì</b> và <b>tham số</b>.</p>
<p><b>Invoker</b> (điều khiển) chỉ biết gọi <code>execute()</code>, và lưu command vào ngăn xếp lịch sử để hoàn tác. Để undo đúng, command phải <b>ghi nhớ trạng thái cũ</b> trước khi thực thi (như <code>prevSpeed</code>).</p>""",
  participants=[
    ("Command", "Interface với execute() (và undo())."),
    ("ConcreteCommand (FanSpeedCommand…)", "Liên kết receiver với hành động; lưu trạng thái cần cho undo."),
    ("Receiver (Light, Fan)", "Đối tượng biết làm việc thật."),
    ("Invoker (RemoteControl)", "Kích hoạt command, quản lý lịch sử."),
    ("Client", "Tạo command, gắn receiver và giao cho invoker."),
  ],
  uml=dict(
    boxes=[
      ("cl", "Client", None, [], [], 120, 240),
      ("inv", "RemoteControl", "Invoker", ["- history: Deque<Command>"], ["+ press(c: Command)", "+ undo()"], 160, 30),
      ("c", "Command", "interface", [], ["+ execute()", "+ undo()", "+ name(): String"], 560, 20),
      ("c1", "LightOnCommand", None, ["- light: Light"], ["+ execute()", "+ undo()"], 440, 230),
      ("c2", "FanSpeedCommand", None, ["- fan: Fan", "- newSpeed, prevSpeed"], ["+ execute()", "+ undo()"], 690, 230),
      ("r1", "Light", "Receiver", [], ["+ on()", "+ off()"], 440, 410),
      ("r2", "Fan", "Receiver", [], ["+ setSpeed(s)", "+ getSpeed()"], 690, 410),
    ],
    edges=[("inv", "c", "agg", "lịch sử"), ("c1", "c", "impl", "", "tree"), ("c2", "c", "impl", "", "tree"),
           ("c1", "r1", "assoc", ""), ("c2", "r2", "assoc", ""), ("cl", "inv", "dep", ""), ("cl", "c1", "dep", "«create»")],
  ),
  code="15-command.java",
  java_notes=[
    "<code>RemoteControl</code> không import <code>Light</code> hay <code>Fan</code> — nó chỉ biết <code>Command</code>.",
    "<code>FanSpeedCommand</code> lưu <code>prevSpeed</code> trước khi đổi tốc độ → undo khôi phục chính xác: 1 → 3 → 0.",
    "Lịch sử là một ngăn xếp (<code>ArrayDeque</code>): lệnh làm sau được hoàn tác trước (LIFO).",
    "Lần undo thứ 5 không còn gì → invoker xử lý an toàn.",
  ],
  pros=["Tách đối tượng gọi lệnh khỏi đối tượng thực hiện.", "Hỗ trợ undo/redo, macro (gộp nhiều command), xếp hàng, lập lịch, ghi log.", "Open/Closed: thêm command mới không sửa invoker."],
  cons=["Mỗi hành động là một lớp → nhiều lớp nhỏ (có thể giảm bằng lambda nếu không cần undo)."],
  when=["Muốn tham số hoá đối tượng bằng hành động (nút bấm, menu, phím tắt).", "Cần undo/redo, lịch sử thao tác.", "Cần xếp hàng, trì hoãn, lập lịch hoặc gửi yêu cầu qua mạng.", "Giao dịch (transaction): ghi lại các bước để rollback."],
  realworld=["<code>java.lang.Runnable</code>, <code>java.util.concurrent.Callable</code>", "<code>javax.swing.Action</code>", "Hàng đợi tác vụ trong <code>ExecutorService</code>", "Lệnh undo/redo trong mọi trình soạn thảo"],
  related="Memento thường đi kèm Command để lưu trạng thái cho undo. Chain of Responsibility có thể chuyển command dọc chuỗi. Command có thể dùng Prototype để sao chép trước khi đưa vào lịch sử. Strategy cũng đóng gói hành vi nhưng mục đích là chọn thuật toán, không phải biểu diễn yêu cầu.",
  exercises=[
    "Thêm <code>redo()</code> cho RemoteControl (gợi ý: dùng ngăn xếp thứ hai).",
    "Viết <code>MacroCommand</code> chứa danh sách command và thực thi lần lượt (“Chế độ đi ngủ”).",
    "Viết lại <code>LightOnCommand</code> bằng lambda <code>Runnable</code> và thảo luận: tại sao lambda khó hỗ trợ undo?",
  ],
),
# ------------------------------------------------------------------ 16
dict(
  id="interpreter", name="Interpreter", vn="Thông dịch", icon="🗣️", freq=1,
  ref="https://gpcoder.com/4702-huong-dan-java-design-pattern-interpreter/",
  intent="Với một ngôn ngữ nhỏ, định nghĩa <b>biểu diễn ngữ pháp</b> của nó dưới dạng các lớp, cùng một bộ thông dịch dùng biểu diễn đó để <b>diễn giải câu</b> trong ngôn ngữ.",
  analogy=("🎼", "Bản nhạc là một “ngôn ngữ”: nốt, dấu lặng, hợp âm… mỗi ký hiệu có một quy tắc. Nhạc công (bộ thông dịch) đọc từng ký hiệu theo quy tắc và chơi ra âm thanh."),
  problem="""
<p>Ứng dụng cần tính các công thức do người dùng nhập, ví dụ cho robot: <code>x 2 + y 1 - *</code> với <code>x</code>, <code>y</code> là giá trị cảm biến. Công thức thay đổi thường xuyên, không thể viết cứng trong code.</p>
<p>Xử lý bằng <code>if/else</code> trên chuỗi thì rối rắm, khó mở rộng thêm toán tử, và không tái sử dụng được kết quả phân tích.</p>""",
  solution="""
<p>Mỗi quy tắc ngữ pháp trở thành một lớp cài đặt interface <code>Expression</code> với phương thức <code>interpret(context)</code>:</p>
<ul>
<li><b>Terminal expression</b>: phần tử không thể chia nhỏ — số, biến.</li>
<li><b>Nonterminal expression</b>: phần tử ghép từ biểu thức khác — cộng, trừ, nhân (chứa 2 biểu thức con).</li>
</ul>
<p>Câu lệnh được <b>phân tích (parse)</b> thành cây cú pháp trừu tượng (AST) — chính là một cây <b>Composite</b>. Gọi <code>interpret()</code> trên gốc → đệ quy tính toàn cây. <b>Context</b> chứa thông tin bên ngoài như giá trị biến.</p>
<div class="callout">💡 Mẫu này hiếm dùng trong ứng dụng thường ngày, nhưng là nền tảng của trình biên dịch, bộ tính công thức Excel, biểu thức chính quy, SQL… Với ngôn ngữ phức tạp nên dùng công cụ sinh parser như ANTLR.</div>""",
  participants=[
    ("AbstractExpression (Expression)", "Khai báo interpret(context)."),
    ("TerminalExpression (NumberExpr, VariableExpr)", "Cài đặt cho ký hiệu kết thúc của ngữ pháp."),
    ("NonterminalExpression (AddExpr…)", "Mỗi quy tắc ghép là một lớp, chứa các biểu thức con."),
    ("Context", "Thông tin toàn cục cho thông dịch (bảng giá trị biến)."),
    ("Client", "Xây/nhận AST (thường qua Parser) và gọi interpret."),
  ],
  uml=dict(
    boxes=[
      ("cl", "Client", None, [], [], 100, 40),
      ("ctx", "Context", None, ["x = 5, y = 3"], [], 100, 220),
      ("e", "Expression", "interface", [], ["+ interpret(ctx): int"], 440, 20),
      ("n", "NumberExpr", "Terminal", ["- value: int"], ["+ interpret(ctx)"], 270, 210),
      ("v", "VariableExpr", "Terminal", ["- name: String"], ["+ interpret(ctx)"], 440, 210),
      ("a", "AddExpr", "Nonterminal", ["- l, r: Expression"], ["+ interpret(ctx)"], 620, 210),
    ],
    notes=[("n1", "return l_->interpret(ctx)\n     + r_->interpret(ctx);", 620, 360)],
    edges=[("cl", "e", "assoc", ""), ("cl", "ctx", "dep", ""), ("n", "e", "impl", "", "tree"),
           ("v", "e", "impl", "", "tree"), ("a", "e", "impl", "", "tree"),
           ("a", "e", "agg", "2", [(760, 245), (760, 55)]), ("n1", "a", "note", "")],
    caption="SubtractExpr, MultiplyExpr cài đặt tương tự AddExpr.",
  ),
  extra="interpreter",
  code="16-interpreter.java",
  java_notes=[
    "<code>Parser.parse</code> dùng ngăn xếp: gặp số/biến thì đẩy vào; gặp toán tử thì lấy 2 phần tử ra, ghép thành nút mới rồi đẩy lại.",
    "Phương thức <code>toString()</code> của mỗi nút in lại cây dưới dạng biểu thức trung tố có ngoặc — giúp “nhìn thấy” AST.",
    "Cùng một AST, đổi context (<code>x = 10</code>) → kết quả mới mà không cần parse lại.",
    "Dùng <code>record</code> và <code>switch</code> mũi tên (Java 14+) giúp mỗi quy tắc chỉ còn một dòng.",
  ],
  pros=["Dễ thay đổi, mở rộng ngữ pháp — mỗi quy tắc một lớp.", "Cài đặt ngữ pháp đơn giản trở nên trực quan."],
  cons=["Ngữ pháp phức tạp → số lớp bùng nổ, khó bảo trì.", "Hiệu năng không cao so với parser chuyên dụng."],
  when=["Có một ngôn ngữ đơn giản cần thông dịch: công thức, quy tắc lọc, lệnh điều khiển robot.", "Ngữ pháp nhỏ và hiệu năng không phải ưu tiên hàng đầu."],
  realworld=["<code>java.util.regex.Pattern</code>", "<code>java.text.Format</code> và các lớp con", "Spring Expression Language (SpEL)", "Bộ tính công thức trong bảng tính"],
  related="Cây AST là một Composite. Visitor dùng để thêm thao tác mới trên AST (in, tối ưu, kiểm tra kiểu). Iterator có thể duyệt AST. Flyweight có thể chia sẻ các nút terminal.",
  exercises=[
    "Thêm toán tử chia <code>/</code> và xử lý chia cho 0.",
    "Viết ngôn ngữ điều khiển robot: <code>FORWARD 10 LEFT 90 REPEAT 4 [ FORWARD 5 ]</code>.",
    "Viết parser cho biểu thức trung tố có ngoặc <code>(x + 2) * (y - 1)</code> (gợi ý: thuật toán Shunting-yard).",
  ],
),
# ------------------------------------------------------------------ 17
dict(
  id="iterator", name="Iterator", vn="Bộ duyệt", icon="🔁", freq=5,
  ref="https://gpcoder.com/4724-huong-dan-java-design-pattern-iterator/",
  intent="Cung cấp cách <b>truy cập tuần tự</b> các phần tử của một tập hợp mà <b>không làm lộ cấu trúc bên trong</b> của nó (mảng, danh sách liên kết, cây…).",
  analogy=("🗺️", "Đi tham quan bảo tàng, bạn có thể tự đi, theo sơ đồ, hoặc theo hướng dẫn viên. Mỗi cách là một “iterator” khác nhau trên cùng một bảo tàng — và bạn không cần biết cách các phòng được xây ra sao."),
  problem="""
<p>Lớp <code>Playlist</code> lưu bài hát trong một mảng. Nếu để client duyệt bằng <code>songs[i]</code>:</p>
<ul>
<li>Client phải biết bên trong là mảng; khi đổi sang <code>LinkedList</code> hay cây, mọi vòng lặp ở client đều hỏng.</li>
<li>Muốn nhiều kiểu duyệt (xuôi, ngược, ngẫu nhiên, chỉ bài &lt; 4 phút) → nhồi hết vào lớp <code>Playlist</code>, làm nó phình to.</li>
</ul>""",
  solution="""
<p>Tách logic duyệt ra một đối tượng riêng — <b>Iterator</b> — giữ vị trí hiện tại và cung cấp <code>hasNext()</code>, <code>next()</code>. Collection chỉ cần có phương thức tạo iterator (<code>iterator()</code>).</p>
<p>Nhiều iterator có thể duyệt <b>độc lập, đồng thời</b> trên cùng một collection, mỗi cái giữ trạng thái riêng.</p>
<div class="callout">💡 Mẫu này đã được tích hợp sẵn vào ngôn ngữ:<br>• <b>C++</b>: iterator là nền tảng của STL — lớp nào có <code>begin()</code>/<code>end()</code> trả về đối tượng hỗ trợ <code>*</code>, <code>++</code>, <code>!=</code> sẽ dùng được <b>range-for</b> và mọi thuật toán <code>&lt;algorithm&gt;</code>.<br>• <b>Python</b>: giao thức <code>__iter__</code>/<code>__next__</code>; hàm có <code>yield</code> (generator) là iterator ngắn gọn nhất.<br>• <b>Java</b>: <code>Iterator</code> + <code>Iterable</code> cho vòng lặp for-each.</div>""",
  participants=[
    ("Iterator", "Interface duyệt: hasNext(), next()."),
    ("ConcreteIterator (ForwardIterator…)", "Cài đặt thuật toán duyệt, giữ vị trí hiện tại."),
    ("Aggregate (Iterable)", "Interface có phương thức tạo iterator."),
    ("ConcreteAggregate (Playlist)", "Trả về iterator phù hợp với cấu trúc bên trong."),
  ],
  uml=dict(
    boxes=[
      ("ag", "Iterable<Song>", "interface", [], ["+ iterator(): Iterator<Song>"], 170, 20),
      ("it", "Iterator<Song>", "interface", [], ["+ hasNext(): boolean", "+ next(): Song"], 560, 20),
      ("pl", "Playlist", None, ["- songs: Song[]", "- count: int"], ["+ add(s)", "+ iterator()", "+ reverseIterator()"], 170, 210),
      ("fi", "ForwardIterator", None, ["- index = 0"], ["+ hasNext()", "+ next()"], 470, 210),
      ("ri", "ReverseIterator", None, ["- index = count - 1"], ["+ hasNext()", "+ next()"], 680, 210),
    ],
    edges=[("pl", "ag", "impl", ""), ("fi", "it", "impl", "", "tree"), ("ri", "it", "impl", "", "tree"),
           ("pl", "fi", "dep", "«create»"), ("ag", "it", "dep", "tạo ra")],
  ),
  code="17-iterator.java",
  java_notes=[
    "Mảng <code>songs</code> là <code>private</code> — client không bao giờ thấy nó.",
    "Hai iterator là <b>inner class</b> nên truy cập trực tiếp được <code>songs</code> và <code>count</code> của Playlist.",
    "<code>next()</code> ném <code>NoSuchElementException</code> khi hết phần tử — đúng hợp đồng của <code>java.util.Iterator</code>.",
    "Nhờ <code>implements Iterable&lt;Song&gt;</code>, vòng <code>for (Song s : playlist)</code> hoạt động tự nhiên.",
  ],
  pros=["Single Responsibility: tách thuật toán duyệt khỏi collection.", "Open/Closed: thêm kiểu duyệt mới không sửa collection.", "Duyệt song song nhiều iterator độc lập.", "Có thể tạm dừng và tiếp tục việc duyệt."],
  cons=["Dư thừa nếu collection đơn giản và chỉ có một kiểu duyệt.", "Có thể kém hiệu quả hơn truy cập trực tiếp với một số cấu trúc."],
  when=["Collection có cấu trúc phức tạp cần che giấu.", "Cần nhiều cách duyệt khác nhau.", "Muốn một cách duyệt thống nhất cho nhiều loại collection khác nhau."],
  realworld=["<code>java.util.Iterator</code>, <code>ListIterator</code>", "<code>java.util.Scanner</code>", "<code>java.sql.ResultSet.next()</code>", "Stream API (<code>Spliterator</code>)"],
  related="Thường dùng để duyệt cây Composite. Factory Method dùng để tạo iterator phù hợp. Memento có thể lưu trạng thái duyệt. Visitor + Iterator: Iterator duyệt, Visitor xử lý từng phần tử.",
  exercises=[
    "Thêm <code>shortSongIterator(int maxMinutes)</code> chỉ trả về bài ngắn hơn ngưỡng.",
    "Thêm <code>remove()</code> vào ForwardIterator.",
    "Viết iterator duyệt cây thư mục (bài Composite) theo chiều sâu (DFS) bằng ngăn xếp.",
  ],
),
# ------------------------------------------------------------------ 18
dict(
  id="mediator", name="Mediator", vn="Người trung gian", icon="🗼", freq=3,
  ref="https://gpcoder.com/4740-huong-dan-java-design-pattern-mediator/",
  intent="Định nghĩa một đối tượng <b>đóng gói cách các đối tượng khác tương tác</b> với nhau. Các đối tượng không gọi nhau trực tiếp mà <b>giao tiếp qua trung gian</b>, nhờ đó giảm phụ thuộc chằng chịt.",
  analogy=("✈️", "Phi công không nói chuyện trực tiếp với nhau để quyết định ai hạ cánh trước. Tất cả liên lạc với <b>đài kiểm soát không lưu</b> — đài điều phối toàn bộ. Không có đài, mỗi phi công phải theo dõi mọi máy bay khác."),
  problem="""
<p>Nhóm chat lớp học có N thành viên. Nếu mỗi người giữ danh sách tất cả người khác và tự gửi tin cho từng người:</p>
<ul>
<li>Số liên kết là <b>N × (N − 1)</b> — với 40 học sinh là 1 560 liên kết!</li>
<li>Thêm quy tắc (tin giáo viên được ghim, chặn người vi phạm) phải sửa lớp thành viên.</li>
<li>Các lớp thành viên gắn chặt với nhau, không tái sử dụng được ở nhóm khác.</li>
</ul>""",
  solution="""
<p>Tạo đối tượng <b>Mediator</b> (<code>ChatRoom</code>). Mỗi thành viên (<b>Colleague</b>) chỉ giữ tham chiếu tới mediator và báo cho nó khi có sự kiện. Mediator quyết định chuyển tin tới ai, theo quy tắc nào.</p>
<p>Quan hệ nhiều – nhiều chằng chịt trở thành quan hệ <b>một – nhiều</b> hình sao. Mọi luật lệ tương tác tập trung ở một chỗ.</p>""",
  participants=[
    ("Mediator (ChatRoom)", "Interface giao tiếp giữa các colleague."),
    ("ConcreteMediator (ClassChatRoom)", "Biết các colleague và điều phối tương tác."),
    ("Colleague (User)", "Chỉ biết mediator; thông báo sự kiện cho mediator."),
    ("ConcreteColleague (Student, Teacher)", "Các thành viên cụ thể."),
  ],
  uml=dict(
    boxes=[
      ("m", "ChatRoom", "interface", [], ["+ join(u: User)", "+ broadcast(msg, from)", "+ sendPrivate(msg, from, to)"], 190, 20),
      ("cm", "ClassChatRoom", None, ["- users: List<User>"], ["+ broadcast(msg, from)"], 190, 230),
      ("u", "User", "abstract", ["# name", "# room: ChatRoom"], ["+ send(msg)", "+ receive(msg, from)"], 600, 20),
      ("s", "Student", None, [], [], 520, 240),
      ("t", "Teacher", None, [], [], 690, 240),
    ],
    edges=[("cm", "m", "impl", ""), ("s", "u", "ext", "", "tree"), ("t", "u", "ext", "", "tree"),
           ("u", "m", "assoc", "room"), ("cm", "u", "agg", "*")],
  ),
  extra="mediator",
  code="18-mediator.java",
  java_notes=[
    "Lớp <code>Student</code> và <code>Teacher</code> không hề tham chiếu tới nhau — chỉ tới <code>ChatRoom</code>.",
    "Quy tắc “tin giáo viên được ghim 📌” nằm trọn trong mediator; thành viên không cần biết.",
    "Tin nhắn riêng cũng đi qua mediator — dễ bổ sung kiểm duyệt, lưu lịch sử…",
  ],
  pros=["Giảm phụ thuộc giữa các thành phần (nhiều–nhiều → một–nhiều).", "Tập trung logic tương tác một chỗ, dễ hiểu, dễ sửa.", "Tái sử dụng colleague ở ngữ cảnh khác dễ hơn."],
  cons=["Mediator có thể trở thành “God object” phình to theo thời gian."],
  when=["Các đối tượng giao tiếp phức tạp, phụ thuộc chằng chịt.", "Form giao diện: thay đổi ô này làm ẩn/hiện/kiểm tra ô khác.", "Phòng chat, điều phối giao thông, hệ thống đặt chỗ."],
  realworld=["<code>java.util.Timer</code> (điều phối các <code>TimerTask</code>)", "<code>java.util.concurrent.Executor</code>", "Controller trong kiến trúc MVC", "Message broker: MQTT broker giữa các thiết bị IoT"],
  related="Facade che giấu hệ thống con và giao tiếp một chiều; Mediator điều phối hai chiều giữa các đồng nghiệp. Observer thường được dùng để cài đặt kênh liên lạc giữa colleague và mediator.",
  exercises=[
    "Thêm chức năng “cấm chat” (mute) một học sinh — chỉ giáo viên có quyền.",
    "Viết mediator cho form đăng ký: chọn “Học sinh” thì hiện ô “Lớp”, chọn “Giáo viên” thì hiện ô “Môn dạy”.",
    "Thiết kế hệ thống MQTT mini: cảm biến publish, màn hình subscribe theo topic, broker là mediator.",
  ],
),
# ------------------------------------------------------------------ 19
dict(
  id="memento", name="Memento", vn="Vật lưu niệm", icon="💾", freq=3,
  ref="https://gpcoder.com/4763-huong-dan-java-design-pattern-memento/",
  intent="<b>Lưu lại và khôi phục trạng thái trước đó</b> của một đối tượng mà <b>không làm lộ chi tiết cài đặt</b> bên trong của nó (không phá vỡ tính đóng gói).",
  analogy=("🎮", "Chơi game, trước khi đánh trùm bạn <b>lưu game (save)</b>. Thua thì <b>tải lại (load)</b>. File save chứa đủ thông tin để khôi phục, nhưng bạn không cần (và không nên) tự mở ra sửa chỉ số nhân vật."),
  problem="""
<p>Trình soạn thảo cần chức năng Undo. Cách đơn giản: một lớp bên ngoài đọc mọi field của <code>Editor</code> và lưu lại. Nhưng:</p>
<ul>
<li>Phải công khai (getter/setter) mọi field private → <b>phá vỡ đóng gói</b>, ai cũng có thể sửa trạng thái.</li>
<li>Mỗi khi <code>Editor</code> thêm field mới, lớp lưu trữ bên ngoài cũng phải sửa theo.</li>
</ul>""",
  solution="""
<p>Giao việc chụp trạng thái cho <b>chính đối tượng chủ</b> (<b>Originator</b>): nó tạo ra một đối tượng <b>Memento</b> chứa bản chụp trạng thái và biết cách khôi phục từ memento.</p>
<p><b>Caretaker</b> (<code>History</code>) chỉ lưu giữ các memento (thường trong ngăn xếp) và trả lại khi cần — nó <b>không đọc, không sửa</b> nội dung memento.</p>
<div class="callout">💡 <b>C++</b>: memento là lớp lồng có mọi thành viên <code>private</code> và khai báo <code>friend class Editor</code> — Caretaker giữ được nhưng <i>trình biên dịch</i> cấm đọc. <b>Python</b>: dùng <code>NamedTuple</code> bất biến. <b>Java</b>: record lồng. Nếu lo bộ nhớ, có thể chỉ lưu phần thay đổi (diff) hoặc giới hạn số bản lưu.</div>""",
  participants=[
    ("Originator (Editor)", "Tạo memento chứa trạng thái hiện tại và khôi phục từ memento."),
    ("Memento (Editor.Memento)", "Ảnh chụp trạng thái, bất biến."),
    ("Caretaker (History)", "Giữ các memento, quyết định khi nào lưu/khôi phục; không xem nội dung."),
  ],
  uml=dict(
    boxes=[
      ("o", "Editor", "Originator", ["- content: String", "- fontSize: int"], ["+ type(text)", "+ save(): Memento", "+ restore(m: Memento)"], 160, 20),
      ("m", "Memento", "nested", ["- content (final)", "- fontSize (final)"], [], 480, 30),
      ("c", "History", "Caretaker", ["- stack: Deque<Memento>"], ["+ backup()", "+ undo()"], 790, 20),
    ],
    edges=[("o", "m", "dep", "«create»"), ("c", "m", "agg", "*"),
           ("c", "o", "assoc", "editor", [(790, 220), (160, 220)])],
  ),
  code="19-memento.java",
  java_notes=[
    "<code>Editor.Memento</code> là <code>record</code> lồng bên trong — bất biến, Caretaker không thể sửa.",
    "<code>History</code> chỉ gọi <code>editor.save()</code> và <code>editor.restore(m)</code>; nó không biết Editor có những field gì.",
    "Undo khôi phục <b>cả</b> nội dung và cỡ chữ — mọi trạng thái được chụp đồng thời.",
    "Undo lần 3 về trạng thái rỗng ban đầu (được backup ngay từ đầu).",
  ],
  pros=["Chụp trạng thái mà không phá vỡ đóng gói.", "Đơn giản hoá Originator — việc quản lý lịch sử giao cho Caretaker."],
  cons=["Tốn bộ nhớ nếu chụp thường xuyên hoặc trạng thái lớn.", "Caretaker phải theo dõi vòng đời để xoá memento cũ."],
  when=["Cần undo/redo, khôi phục, checkpoint, save game.", "Truy cập trực tiếp vào trạng thái sẽ phá vỡ đóng gói.", "Transaction cần rollback khi lỗi."],
  realworld=["<code>java.io.Serializable</code> (lưu trạng thái đối tượng)", "Undo trong trình soạn thảo, Photoshop", "Git commit — mỗi commit là một bản chụp trạng thái"],
  related="Command + Memento: command thực thi, memento lưu trạng thái để undo. Iterator có thể dùng memento lưu vị trí duyệt. Prototype là cách đơn giản để tạo memento khi trạng thái không quá phức tạp.",
  exercises=[
    "Thêm <code>redo()</code> vào History.",
    "Giới hạn History chỉ lưu tối đa 20 bản; bản cũ nhất bị xoá khi đầy.",
    "Áp dụng Memento cho game: nhân vật có máu, vàng, vị trí; lưu tại checkpoint và khôi phục khi thua.",
  ],
),
# ------------------------------------------------------------------ 20
dict(
  id="observer", name="Observer", vn="Người quan sát", icon="👀", freq=5,
  ref="https://gpcoder.com/4747-huong-dan-java-design-pattern-observer/",
  intent="Định nghĩa quan hệ <b>một – nhiều</b> giữa các đối tượng: khi một đối tượng <b>thay đổi trạng thái</b>, mọi đối tượng phụ thuộc đều <b>được thông báo và cập nhật tự động</b>.",
  analogy=("🔔", "Bạn <b>đăng ký (subscribe)</b> kênh YouTube và bật chuông. Mỗi khi có video mới, YouTube tự gửi thông báo cho tất cả người đăng ký. Không cần ngày nào cũng vào kiểm tra; không thích nữa thì huỷ đăng ký."),
  problem="""
<p>Trạm thời tiết đo nhiệt độ và độ ẩm. Màn hình LCD, quạt tự động, ứng dụng điện thoại… đều cần dữ liệu mới.</p>
<ul>
<li>Nếu các thiết bị liên tục hỏi trạm (<b>polling</b>) → lãng phí, có độ trễ.</li>
<li>Nếu trạm gọi thẳng <code>lcd.show()</code>, <code>fan.check()</code>, <code>app.push()</code> → trạm gắn chặt với mọi thiết bị; thêm thiết bị mới phải sửa trạm.</li>
</ul>""",
  solution="""
<p>Đối tượng phát (<b>Subject</b>/Publisher) giữ <b>danh sách người đăng ký</b> và cung cấp <code>subscribe()</code>/<code>unsubscribe()</code>. Mọi người đăng ký (<b>Observer</b>/Subscriber) cài đặt chung interface có <code>update()</code>.</p>
<p>Khi trạng thái thay đổi, subject duyệt danh sách và gọi <code>update()</code> trên từng observer. Subject chỉ biết interface <code>Observer</code> — không biết đó là LCD hay quạt.</p>
<div class="callout">💡 <b>Push vs Pull</b>: Push — subject gửi luôn dữ liệu trong <code>update(t, h)</code> (như ví dụ). Pull — subject chỉ báo “có thay đổi”, observer tự gọi getter để lấy dữ liệu nó cần.</div>""",
  participants=[
    ("Subject", "Interface quản lý danh sách observer."),
    ("ConcreteSubject (WeatherStation)", "Lưu trạng thái; thông báo cho observer khi trạng thái đổi."),
    ("Observer", "Interface với phương thức update()."),
    ("ConcreteObserver (LcdDisplay…)", "Phản ứng với thông báo theo cách riêng."),
  ],
  uml=dict(
    boxes=[
      ("s", "Subject", "interface", [], ["+ subscribe(o)", "+ unsubscribe(o)", "+ notifyObservers()"], 180, 20),
      ("o", "Observer", "interface", [], ["+ update(t, h)"], 590, 30),
      ("ws", "WeatherStation", None, ["- observers: List<Observer>", "- temperature, humidity"], ["+ setMeasurements(t, h)"], 180, 220),
      ("o1", "LcdDisplay", None, [], ["+ update(t, h)"], 450, 220),
      ("o2", "AutoFan", None, ["- threshold"], ["+ update(t, h)"], 600, 220),
      ("o3", "PhoneApp", None, ["- owner"], ["+ update(t, h)"], 750, 220),
    ],
    notes=[("n1", "for (Observer* o : observers_)\n    if (o) o->update(t, h);", 180, 380)],
    edges=[("ws", "s", "impl", ""), ("s", "o", "agg", "*"), ("o1", "o", "impl", "", "tree"),
           ("o2", "o", "impl", "", "tree"), ("o3", "o", "impl", "", "tree"), ("n1", "ws", "note", "")],
  ),
  extra="observer",
  code="20-observer.java",
  java_notes=[
    "<code>WeatherStation</code> chỉ có một <code>List&lt;Observer&gt;</code> — không có field nào kiểu <code>LcdDisplay</code> hay <code>AutoFan</code>.",
    "Mỗi lần <code>setMeasurements()</code> là ba observer phản ứng theo ba cách khác nhau.",
    "Sau khi <code>PhoneApp</code> huỷ đăng ký, nó không còn nhận thông báo.",
    "Thêm observer mới (ví dụ ghi log ra thẻ SD) không phải sửa <code>WeatherStation</code>.",
  ],
  pros=["Open/Closed: thêm subscriber mới không sửa publisher.", "Thiết lập quan hệ giữa các đối tượng lúc chạy.", "Liên kết lỏng giữa publisher và subscriber."],
  cons=["Thứ tự thông báo không được đảm bảo.", "Quên huỷ đăng ký → rò rỉ bộ nhớ (lapsed listener).", "Chuỗi cập nhật dây chuyền khó theo dõi, dễ lặp vô hạn."],
  when=["Thay đổi trạng thái của một đối tượng cần cập nhật nhiều đối tượng khác, mà danh sách đó thay đổi động.", "Hệ thống hướng sự kiện: giao diện người dùng, IoT, thông báo.", "Tách tầng dữ liệu (Model) khỏi tầng hiển thị (View) trong MVC."],
  realworld=["Event listener trong Swing/JavaFX: <code>addActionListener()</code>", "<code>java.beans.PropertyChangeListener</code>", "<code>java.util.concurrent.Flow</code> (Reactive Streams), RxJava", "MQTT publish/subscribe trong IoT; <code>addEventListener</code> trong JavaScript"],
  related="Mediator thường dùng Observer để liên lạc. Khác Mediator: Observer là kết nối động một–nhiều, Mediator loại bỏ phụ thuộc lẫn nhau giữa các thành phần. Chain of Responsibility chuyển tuần tự; Observer phát đồng thời cho tất cả.",
  exercises=[
    "Thêm observer <code>SdCardLogger</code> ghi dữ liệu kèm thời gian.",
    "Đổi sang mô hình <b>pull</b>: <code>update(WeatherStation s)</code> và observer tự gọi <code>s.getTemperature()</code>.",
    "C++: thay mảng con trỏ <code>Observer*</code> bằng mảng <code>std::function&lt;void(float,float)&gt;</code> để đăng ký được cả lambda.",
  ],
),
# ------------------------------------------------------------------ 21
dict(
  id="state", name="State", vn="Trạng thái", icon="🚦", freq=3,
  ref="https://gpcoder.com/4785-huong-dan-java-design-pattern-state/",
  intent="Cho phép một đối tượng <b>thay đổi hành vi khi trạng thái bên trong của nó thay đổi</b> — trông như thể đối tượng đã đổi sang một lớp khác.",
  analogy=("📱", "Nút nguồn điện thoại: khi máy đang khoá, bấm nút → bật màn hình; khi đang mở → khoá máy; khi pin cạn → không phản hồi. Cùng một hành động, phản ứng khác nhau tuỳ trạng thái."),
  problem="""
<p>Máy bán nước tự động có các trạng thái: <i>chờ tiền</i>, <i>đã có tiền</i>, <i>hết hàng</i>. Mỗi hành động (bỏ tiền, trả tiền, bấm nút) phản ứng khác nhau theo trạng thái.</p>
<p>Cài đặt bằng biến <code>int state</code> + <code>switch</code> trong <b>mọi</b> phương thức: 3 trạng thái × 3 hành động = 9 nhánh rải rác. Thêm trạng thái “bảo trì” → sửa tất cả phương thức; logic của một trạng thái bị chia nhỏ ra khắp nơi, rất dễ sót.</p>""",
  solution="""
<p>Mỗi trạng thái thành một lớp riêng cài đặt interface <code>State</code>, chứa <b>toàn bộ hành vi</b> ứng với trạng thái đó. Đối tượng chính (<b>Context</b>) giữ tham chiếu tới đối tượng trạng thái hiện tại và <b>uỷ quyền</b> mọi hành động cho nó.</p>
<p>Chuyển trạng thái = gán một đối tượng State khác cho Context. Việc chuyển có thể do chính các lớp State quyết định (như ví dụ).</p>
<div class="callout">💡 <b>State vs Strategy</b>: cấu trúc gần như giống hệt. Khác biệt: với Strategy, <i>client</i> chọn thuật toán và các strategy không biết nhau; với State, các trạng thái <i>tự chuyển đổi</i> lẫn nhau và biết về nhau.</div>""",
  participants=[
    ("Context (VendingMachine)", "Giữ trạng thái hiện tại; uỷ quyền hành vi cho nó."),
    ("State", "Interface khai báo các hành vi phụ thuộc trạng thái."),
    ("ConcreteState (NoCoinState…)", "Cài đặt hành vi cho một trạng thái; có thể chuyển Context sang trạng thái khác."),
  ],
  uml=dict(
    boxes=[
      ("c", "VendingMachine", "Context", ["- state: State", "- stock: int"], ["+ insertCoin()", "+ ejectCoin()", "+ pressButton()", "+ setState(s: State)"], 170, 20),
      ("s", "State", "interface", [], ["+ insertCoin(m)", "+ ejectCoin(m)", "+ pressButton(m)"], 580, 20),
      ("s1", "NoCoinState", None, [], [], 420, 240),
      ("s2", "HasCoinState", None, [], [], 590, 240),
      ("s3", "SoldOutState", None, [], [], 760, 240),
    ],
    notes=[("n1", "void insertCoin() {\n    state_->insertCoin(*this);\n}", 170, 250)],
    edges=[("c", "s", "agg", "state"), ("s1", "s", "impl", "", "tree"), ("s2", "s", "impl", "", "tree"),
           ("s3", "s", "impl", "", "tree"), ("n1", "c", "note", "")],
  ),
  extra="state",
  code="21-state.java",
  java_notes=[
    "Lớp <code>VendingMachine</code> không có một câu <code>if/switch</code> nào theo trạng thái — mọi thứ được uỷ quyền.",
    "Mỗi lớp State gom đủ 3 hành vi của trạng thái đó tại một chỗ → dễ đọc, dễ kiểm thử.",
    "<code>HasCoinState.pressButton()</code> tự quyết định trạng thái tiếp theo dựa vào số hàng còn lại.",
    "Log in rõ mọi lần chuyển trạng thái, khớp với sơ đồ trạng thái phía trên.",
  ],
  pros=["Single Responsibility: mỗi trạng thái một lớp.", "Open/Closed: thêm trạng thái mới không sửa trạng thái cũ hay Context.", "Loại bỏ các khối điều kiện cồng kềnh."],
  cons=["Thừa thãi nếu chỉ có vài trạng thái và ít khi thay đổi.", "Số lớp tăng theo số trạng thái."],
  when=["Hành vi của đối tượng phụ thuộc mạnh vào trạng thái và có nhiều trạng thái.", "Code có nhiều <code>switch</code>/<code>if</code> lặp lại theo cùng một biến trạng thái.", "Máy trạng thái: đèn giao thông, đơn hàng, nhân vật game, robot (dò line → tránh vật cản → dừng)."],
  realworld=["<code>javax.faces.lifecycle.LifeCycle</code>", "Trạng thái đơn hàng trong thương mại điện tử", "Spring State Machine", "Bộ điều khiển robot dùng máy trạng thái hữu hạn (FSM)"],
  related="Strategy có cấu trúc giống State. Các đối tượng State có thể là Singleton/Flyweight nếu không có field riêng. Bridge cũng dựa trên composition nhưng nhằm tách hai chiều phát triển.",
  exercises=[
    "Thêm trạng thái <code>MaintenanceState</code>: mọi thao tác đều từ chối, chỉ <code>refill()</code> mới thoát ra.",
    "Mô hình hoá đèn giao thông Xanh → Vàng → Đỏ với thời gian mỗi đèn khác nhau.",
    "Viết FSM cho robot: <code>FOLLOW_LINE</code>, <code>AVOID_OBSTACLE</code>, <code>STOP</code>, chuyển trạng thái theo dữ liệu cảm biến.",
  ],
),
# ------------------------------------------------------------------ 22
dict(
  id="strategy", name="Strategy", vn="Chiến lược", icon="♟️", freq=5,
  ref="https://gpcoder.com/4796-huong-dan-java-design-pattern-strategy/",
  intent="Định nghĩa một <b>họ thuật toán</b>, đóng gói từng thuật toán thành lớp riêng và làm cho chúng <b>có thể hoán đổi</b> cho nhau lúc chạy.",
  analogy=("🗺️", "Đến sân bay, bạn có thể đi xe buýt (rẻ, chậm), taxi (nhanh, đắt) hoặc xe đạp (miễn phí, mệt). Mục tiêu như nhau, chọn chiến lược tuỳ ngân sách và thời gian — và đổi được ngay lúc đi."),
  problem="""
<p>Giỏ hàng hỗ trợ nhiều phương thức thanh toán: tiền mặt, thẻ, ví MoMo… mỗi cách tính phí và xử lý khác nhau.</p>
<p>Viết tất cả trong <code>ShoppingCart.checkout()</code> bằng <code>if (method == "card") … else if …</code>: lớp ngày càng phình to; thêm ZaloPay phải sửa lớp giỏ hàng (có nguy cơ làm hỏng phần đang chạy); khó kiểm thử từng phương thức riêng.</p>""",
  solution="""
<p>Tách mỗi thuật toán ra một lớp cài đặt interface chung <b>Strategy</b> (<code>PaymentStrategy</code>). Lớp <b>Context</b> (<code>ShoppingCart</code>) chỉ giữ/nhận một strategy và gọi nó, không biết chi tiết bên trong.</p>
<p>Client chọn strategy phù hợp và đưa cho context — có thể đổi bất cứ lúc nào.</p>
<div class="callout">💡 Ba cách cài đặt Strategy trong C++:<br>① <b>interface + hàm ảo</b> — đổi lúc chạy;<br>② <b>lambda / <code>std::function</code></b> — gọn khi strategy chỉ có một hàm;<br>③ <b>template (policy-based design)</b> — chọn lúc <i>biên dịch</i>, không tốn chi phí gọi hàm ảo, trình biên dịch có thể inline → rất được ưa chuộng trong firmware.<br>Trong Python, strategy thường chỉ là một <b>hàm</b> truyền vào.</div>""",
  participants=[
    ("Strategy (PaymentStrategy)", "Interface chung cho mọi thuật toán."),
    ("ConcreteStrategy (CashPayment…)", "Cài đặt một thuật toán cụ thể."),
    ("Context (ShoppingCart)", "Dùng strategy qua interface; có thể nhận strategy qua tham số hoặc setter."),
    ("Client", "Chọn strategy và đưa cho context."),
  ],
  uml=dict(
    boxes=[
      ("c", "ShoppingCart", "Context", ["- subtotal: int"], ["+ checkout(s: PaymentStrategy)", "+ total(discount)"], 180, 20),
      ("s", "PaymentStrategy", "interface", [], ["+ name(): String", "+ fee(amount): int", "+ pay(amount)"], 580, 20),
      ("s1", "CashPayment", None, [], ["+ pay(amount)"], 420, 220),
      ("s2", "CardPayment", None, ["- cardNumber"], ["+ pay(amount)"], 590, 220),
      ("s3", "MomoPayment", None, ["- phone"], ["+ pay(amount)"], 760, 220),
      ("cl", "Client", None, [], [], 180, 230),
    ],
    edges=[("c", "s", "dep", "dùng"), ("s1", "s", "impl", "", "tree"), ("s2", "s", "impl", "", "tree"),
           ("s3", "s", "impl", "", "tree"), ("cl", "c", "dep", ""), ("cl", "s1", "dep", "chọn")],
  ),
  code="22-strategy.java",
  java_notes=[
    "Cùng một giỏ hàng, gọi <code>checkout()</code> với ba strategy khác nhau → ba cách tính phí và thanh toán.",
    "<code>ShoppingCart</code> không có <code>if</code> nào theo phương thức thanh toán.",
    "Phần giảm giá minh hoạ cách viết strategy bằng <b>lambda</b> với functional interface <code>IntUnaryOperator</code>.",
  ],
  pros=["Hoán đổi thuật toán lúc chạy.", "Tách chi tiết thuật toán khỏi code sử dụng.", "Thay kế thừa bằng composition.", "Open/Closed: thêm strategy mới không sửa context."],
  cons=["Client phải biết sự khác nhau giữa các strategy để chọn.", "Thừa nếu chỉ có 2 thuật toán ít thay đổi — lambda có thể đủ."],
  when=["Có nhiều biến thể của một thuật toán và cần đổi lúc chạy.", "Nhiều lớp chỉ khác nhau ở cách thực hiện một hành vi.", "Thay thế khối điều kiện lớn chọn thuật toán."],
  realworld=["<code>java.util.Comparator</code> truyền vào <code>Collections.sort()</code>/<code>List.sort()</code>", "<code>javax.servlet.http.HttpServlet</code> (service → doGet/doPost)", "Chiến lược nén, mã hoá, định tuyến; thuật toán tìm đường A*/Dijkstra trong game"],
  related="State có cấu trúc giống nhưng các trạng thái biết và chuyển cho nhau. Template Method dùng kế thừa để thay một phần thuật toán (tĩnh, lúc biên dịch); Strategy dùng composition để thay cả thuật toán (động, lúc chạy). Decorator thay vỏ, Strategy thay ruột.",
  exercises=[
    "Thêm <code>ZaloPayPayment</code> với phí 0.5%, tối thiểu 2 000đ.",
    "Sắp xếp danh sách học sinh bằng ba <code>Comparator</code>: theo tên, theo điểm giảm dần, theo lớp rồi tên.",
    "Robot tránh vật cản với ba strategy: rẽ trái, rẽ phải, lùi rồi quay ngẫu nhiên. Cho phép đổi strategy qua Bluetooth.",
  ],
),
# ------------------------------------------------------------------ 23
dict(
  id="template-method", name="Template Method", vn="Phương thức khuôn mẫu", icon="📐", freq=4,
  ref="https://gpcoder.com/4810-huong-dan-java-design-pattern-template-method/",
  intent="Định nghĩa <b>bộ khung (skeleton) của một thuật toán</b> trong lớp cha, cho phép lớp con <b>định nghĩa lại một số bước</b> mà không thay đổi cấu trúc tổng thể của thuật toán.",
  analogy=("🏘️", "Xây nhà theo quy trình cố định: đổ móng → dựng khung → xây tường → lắp điện nước → hoàn thiện. Mỗi chủ nhà chọn kiểu tường, màu sơn khác nhau, nhưng <i>không ai</i> được xây tường trước khi đổ móng."),
  problem="""
<p>Ứng dụng xuất báo cáo điểm ra CSV, HTML, PDF… Mọi định dạng đều theo các bước: tải dữ liệu → lọc → ghi tiêu đề → ghi từng dòng → ghi cuối trang.</p>
<p>Viết ba lớp độc lập thì phần tải dữ liệu, trình tự gọi các bước bị <b>lặp lại</b> ở cả ba. Sửa cách tải dữ liệu phải sửa ba nơi; ai đó có thể “quên” bước lọc ở một định dạng.</p>""",
  solution="""
<p>Chia thuật toán thành các bước, đặt trong lớp trừu tượng. Một phương thức <b>template</b> (<code>generate()</code>, khai báo <code>final</code>) gọi các bước theo đúng trình tự. Các bước gồm:</p>
<ul>
<li><b>Bước chung</b>: cài đặt sẵn ở lớp cha (<code>loadData()</code>).</li>
<li><b>Bước trừu tượng</b> (primitive operations): lớp con <b>bắt buộc</b> cài đặt (<code>writeHeader()</code>, <code>writeRow()</code>…).</li>
<li><b>Hook</b>: có cài đặt mặc định (thường rỗng), lớp con <b>có thể</b> ghi đè để chen vào (<code>filter()</code>, <code>shouldLog()</code>).</li>
</ul>
<div class="callout">💡 <b>Nguyên lý Hollywood</b>: “Đừng gọi chúng tôi, chúng tôi sẽ gọi bạn.” — lớp cha điều khiển luồng và gọi xuống lớp con, chứ không phải ngược lại.</div>""",
  participants=[
    ("AbstractClass (ReportGenerator)", "Định nghĩa template method và các bước trừu tượng/hook."),
    ("ConcreteClass (CsvReport, HtmlReport)", "Cài đặt các bước trừu tượng, tuỳ chọn ghi đè hook."),
  ],
  uml=dict(
    boxes=[
      ("a", "ReportGenerator", "abstract", [], ["+ generate()  {final}", "- loadData()", "# filter(rows)   «hook»", "# shouldLog()    «hook»",
                                                "# writeHeader()  {abstract}", "# writeRow(r)    {abstract}", "# writeFooter(n) {abstract}"], 300, 20),
      ("c1", "CsvReport", None, [], ["# writeHeader()", "# writeRow(r)", "# writeFooter(n)"], 170, 300),
      ("c2", "HtmlReport", None, [], ["# filter(rows)", "# shouldLog()", "# writeHeader()", "# writeRow(r)", "# writeFooter(n)"], 440, 300),
    ],
    notes=[("n1", "generate():\n  rows = loadData()\n  rows = filter(rows)\n  writeHeader()\n  for r in rows: writeRow(r)\n  writeFooter(rows.size())\n  if (shouldLog()) log()", 700, 40)],
    edges=[("c1", "a", "ext", "", "tree"), ("c2", "a", "ext", "", "tree"), ("n1", "a", "note", "")],
  ),
  code="23-template-method.java",
  java_notes=[
    "<code>generate()</code> là <code>final</code> — lớp con không thể đổi trình tự các bước.",
    "<code>CsvReport</code> chỉ cài đặt 3 bước bắt buộc, dùng hook mặc định (không lọc, không log).",
    "<code>HtmlReport</code> ghi đè hook <code>filter()</code> để chỉ lấy học sinh đạt và <code>shouldLog()</code> để bật log.",
    "Dữ liệu chỉ được tải ở một chỗ duy nhất (<code>loadData()</code>) — không còn trùng lặp.",
  ],
  pros=["Loại bỏ code trùng lặp — phần chung nằm ở lớp cha.", "Kiểm soát điểm mở rộng: lớp con chỉ ghi đè những gì được phép.", "Dễ thêm biến thể mới."],
  cons=["Bị giới hạn bởi bộ khung đã định nghĩa.", "Có thể vi phạm Liskov nếu lớp con làm sai “hợp đồng” của bước.", "Càng nhiều bước càng khó bảo trì; dựa trên kế thừa nên kém linh hoạt hơn composition."],
  when=["Nhiều lớp có thuật toán giống nhau, chỉ khác vài bước.", "Muốn kiểm soát lớp con chỉ mở rộng ở những điểm nhất định.", "Xây dựng framework: framework định luồng, người dùng điền các bước."],
  realworld=["<code>java.io.InputStream.read(byte[], int, int)</code> gọi <code>read()</code> trừu tượng", "<code>java.util.AbstractList</code>, <code>AbstractMap</code>", "<code>HttpServlet.service()</code> gọi <code>doGet()</code>/<code>doPost()</code>", "JUnit: <code>@BeforeEach</code> → test → <code>@AfterEach</code>; vòng <code>setup()</code>/<code>loop()</code> của Arduino"],
  related="Factory Method là một dạng đặc biệt của Template Method (một bước là “tạo đối tượng”). Strategy thay toàn bộ thuật toán bằng composition lúc chạy; Template Method thay một phần bằng kế thừa lúc biên dịch.",
  exercises=[
    "Thêm <code>MarkdownReport</code> xuất bảng Markdown.",
    "Thêm hook <code>sortRows()</code> để HtmlReport sắp xếp theo điểm giảm dần.",
    "Viết lớp trừu tượng <code>RobotMission</code> với template <code>run()</code>: <code>calibrate() → move() → report()</code>, và hai nhiệm vụ cụ thể.",
  ],
),
# ------------------------------------------------------------------ 24
dict(
  id="visitor", name="Visitor", vn="Người viếng thăm", icon="🧳", freq=2,
  ref="https://gpcoder.com/4813-huong-dan-java-design-pattern-visitor/",
  intent="Cho phép <b>thêm thao tác mới</b> lên các đối tượng của một cấu trúc <b>mà không cần sửa các lớp</b> của những đối tượng đó — bằng cách tách thao tác ra một đối tượng “khách viếng thăm”.",
  analogy=("🩺", "Bác sĩ đi khám sức khoẻ định kỳ ở trường: tới lớp nào khám lớp đó. Hôm sau là nhân viên chụp ảnh thẻ, tuần sau là đoàn tiêm phòng. Trường không thay đổi, chỉ có “khách viếng thăm” khác nhau mang theo công việc khác nhau."),
  problem="""
<p>Phần mềm vẽ có các lớp hình: <code>Circle</code>, <code>Rectangle</code>, <code>Triangle</code>. Liên tục có yêu cầu thao tác mới: tính diện tích, xuất JSON, xuất XML, vẽ ra SVG…</p>
<p>Nếu mỗi lần lại thêm một phương thức vào <b>mọi</b> lớp hình → các lớp hình phình to với những trách nhiệm chẳng liên quan (xuất XML là việc của hình tròn sao?), và mỗi thay đổi phải sửa nhiều lớp đã ổn định.</p>""",
  solution="""
<p>Đưa mỗi thao tác vào một lớp <b>Visitor</b> riêng, có một phương thức <code>visit()</code> cho từng loại phần tử. Mỗi phần tử chỉ cần một phương thức duy nhất: <code>accept(visitor)</code> gọi <code>visitor.visit(this)</code>.</p>
<p><b>Double dispatch</b>: lời gọi <code>shape.accept(v)</code> chọn đúng lớp phần tử (dispatch lần 1, đa hình), sau đó <code>v.visit(this)</code> chọn đúng overload theo kiểu tĩnh của <code>this</code> (dispatch lần 2). Nhờ vậy không cần <code>instanceof</code>.</p>
<div class="callout warn">⚠️ Visitor phù hợp khi <b>cấu trúc phần tử ổn định</b> nhưng <b>thao tác hay thay đổi</b>. Ngược lại, nếu hay thêm loại phần tử mới thì mọi Visitor đều phải sửa. (Lựa chọn hiện đại: C++17 <code>std::variant</code> + <code>std::visit</code> — không cần hàm ảo, không cấp phát động; Python 3.10 <code>match/case</code>.)</div>""",
  participants=[
    ("Visitor (ShapeVisitor)", "Khai báo visit() cho từng ConcreteElement."),
    ("ConcreteVisitor (AreaVisitor…)", "Cài đặt một thao tác cho mọi loại phần tử; có thể tích luỹ trạng thái."),
    ("Element (Shape)", "Khai báo accept(visitor)."),
    ("ConcreteElement (Circle…)", "Cài đặt accept bằng cách gọi visitor.visit(this)."),
    ("ObjectStructure", "Tập hợp phần tử có thể duyệt (danh sách drawing)."),
  ],
  uml=dict(
    boxes=[
      ("e", "Shape", "interface", [], ["+ accept(v: ShapeVisitor)"], 200, 20),
      ("c", "Circle", None, ["- r"], ["+ accept(v)"], 80, 220),
      ("r", "Rectangle", None, ["- w, h"], ["+ accept(v)"], 200, 220),
      ("t", "Triangle", None, ["- base, height"], ["+ accept(v)"], 330, 220),
      ("v", "ShapeVisitor", "interface", [], ["+ visit(c: Circle)", "+ visit(r: Rectangle)", "+ visit(t: Triangle)"], 640, 20),
      ("v1", "AreaVisitor", None, ["- total: double"], ["+ visit(...) ×3"], 550, 230),
      ("v2", "JsonExportVisitor", None, ["- sb: StringBuilder"], ["+ visit(...) ×3"], 750, 230),
    ],
    notes=[("n1", "void accept(ShapeVisitor& v) const override {\n    v.visit(*this);   // double dispatch\n}", 200, 370)],
    edges=[("c", "e", "impl", "", "tree"), ("r", "e", "impl", "", "tree"), ("t", "e", "impl", "", "tree"),
           ("v1", "v", "impl", "", "tree"), ("v2", "v", "impl", "", "tree"), ("e", "v", "dep", "accept"), ("n1", "r", "note", "")],
  ),
  code="24-visitor.java",
  java_notes=[
    "Các <code>record</code> hình học chỉ có <code>accept()</code> — không có code tính diện tích hay xuất JSON.",
    "<code>AreaVisitor</code> tích luỹ tổng diện tích qua nhiều lần visit (visitor có trạng thái).",
    "Thêm thao tác <code>SvgExportVisitor</code>: tạo 1 lớp mới, không sửa một dòng nào của Circle/Rectangle/Triangle.",
  ],
  pros=["Open/Closed với thao tác: thêm thao tác mới không sửa lớp phần tử.", "Single Responsibility: gom các phiên bản của một thao tác vào một lớp.", "Visitor có thể tích luỹ thông tin khi duyệt cấu trúc phức tạp."],
  cons=["Thêm loại phần tử mới phải sửa mọi Visitor.", "Visitor có thể cần truy cập dữ liệu private của phần tử → phải công khai bớt.", "Khó hiểu với người mới (double dispatch)."],
  when=["Cần thực hiện nhiều thao tác không liên quan trên một cấu trúc đối tượng phức tạp (cây Composite, AST).", "Cấu trúc phần tử ổn định, thao tác thường xuyên thay đổi.", "Trình biên dịch: kiểm tra kiểu, tối ưu, sinh mã trên cùng một AST."],
  realworld=["<code>java.nio.file.FileVisitor</code> / <code>Files.walkFileTree()</code>", "<code>javax.lang.model.element.ElementVisitor</code> (annotation processing)", "ASM, JavaParser: duyệt cây bytecode/mã nguồn"],
  related="Visitor thường dùng trên cây Composite và AST của Interpreter. Iterator duyệt cấu trúc, Visitor xử lý từng phần tử. Visitor là phiên bản mạnh hơn của Command — thực thi thao tác trên nhiều loại đối tượng khác nhau.",
  exercises=[
    "Viết <code>PerimeterVisitor</code> tính tổng chu vi.",
    "Viết <code>SvgExportVisitor</code> xuất bản vẽ ra chuỗi SVG.",
    "Thêm hình <code>Square</code>. Liệt kê các file phải sửa và giải thích nhược điểm của Visitor.",
    "C++: thêm <code>Triangle</code> vào bản <code>std::variant</code>. Trình biên dịch báo lỗi gì nếu quên viết lambda cho nó? Đó là ưu điểm gì?",
  ],
),
]
