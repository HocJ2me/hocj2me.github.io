# -*- coding: utf-8 -*-
"""Khóa AI cơ bản (THCS cuối – THPT, đã biết Python cơ bản).  Build: python -X utf8 course.py
Cần: numpy, scikit-learn."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "common")]
import coursekit
import figs

CODE = os.path.join(HERE, "code")
_runner = coursekit.Runner(os.path.join(HERE, "out", "run-cache.json"))


def run(path, stdin):
    return f"python {os.path.basename(path)}", coursekit.run_py(path, stdin, runner=_runner)


L = []
L.append(dict(
  id="ai-la-gi", short="AI là gì?", title="AI là gì? Lập trình truyền thống và học máy", icon="🤖", time="1,5 giờ",
  goal="Hiểu AI, học máy, học sâu khác nhau thế nào và vì sao “cho máy học từ dữ liệu” lại mạnh hơn tự viết luật trong nhiều bài toán.",
  goals=["Phân biệt AI – Machine Learning – Deep Learning", "Hiểu học có giám sát / không giám sát", "Viết chương trình đầu tiên để máy tự tìm ngưỡng phân loại từ dữ liệu"],
  sections=[
    dict(h="Trí tuệ nhân tạo, học máy, học sâu", fig=figs.ai_venn(), html="""
<p><b>Trí tuệ nhân tạo (AI)</b> là mọi kỹ thuật giúp máy tính làm những việc tưởng như cần trí thông minh của con người: nhận ra khuôn mặt, hiểu câu nói, chơi cờ, lái xe. <b>Học máy (Machine Learning – ML)</b> là nhánh quan trọng nhất của AI hiện nay: thay vì lập trình từng luật, ta đưa cho máy <b>rất nhiều ví dụ</b> và để máy <b>tự rút ra quy luật</b>. <b>Học sâu (Deep Learning)</b> là học máy dùng <b>mạng nơ-ron nhiều lớp</b> — công nghệ đứng sau ChatGPT, nhận dạng ảnh, xe tự lái.</p>"""),
    dict(h="Đổi cách nghĩ: từ “viết luật” sang “học từ dữ liệu”", fig=figs.lap_trinh_vs_hoc_may(), html="""
<p>Khi viết chương trình thông thường, <b>con người</b> phải nghĩ ra luật (if nhiệt độ &gt; 30 thì bật quạt). Nhưng có những luật ta <b>không thể viết ra</b>: làm sao mô tả bằng if-else “thế nào là chữ số 7 viết tay”? Học máy đảo ngược: ta cho <b>dữ liệu + đáp án</b>, máy tìm ra <b>luật</b> — gọi là <b>mô hình (model)</b>. Sau đó dùng mô hình để <b>dự đoán</b> dữ liệu mới.</p>
<table class="tbl"><tr><th>Loại học</th><th>Dữ liệu</th><th>Ví dụ</th></tr>
<tr><td><b>Có giám sát</b> (supervised)</td><td>có nhãn (đáp án)</td><td>đoán giá nhà (<i>hồi quy</i> – ra số), lọc thư rác (<i>phân loại</i> – ra nhóm)</td></tr>
<tr><td><b>Không giám sát</b> (unsupervised)</td><td>không có nhãn</td><td>chia khách hàng thành nhóm, tìm điểm bất thường</td></tr>
<tr><td><b>Học tăng cường</b> (reinforcement)</td><td>phần thưởng / phạt</td><td>robot tự học đi, AI chơi game</td></tr></table>"""),
    dict(h="Ví dụ: máy tự tìm ngưỡng phân biệt hai loài hoa", fig=figs.scatter_iris_1d(), figcap="Mỗi chấm là một bông hoa thật trong bộ dữ liệu Iris (1936). Hai loài chồng lấn một phần nên không ngưỡng nào đúng 100%.",
         code="01-luat-va-hoc.py", notes=[
      "“Huấn luyện” ở đây chỉ là <b>thử mọi ngưỡng và giữ ngưỡng đúng nhiều nhất</b> — mọi thuật toán học máy đều là phiên bản thông minh hơn của ý tưởng này.",
      "Luật “cảm tính” 5.5 cm chỉ đúng 75%; máy nhìn dữ liệu nên tìm được 4.7 cm đúng 93%.",
      "Không đạt 100% vì hai loài có vùng chồng lấn — dùng thêm đặc trưng (chiều rộng cánh hoa…) sẽ tốt hơn (bài 4)."]),
  ],
  mistakes=["Nghĩ AI là “phép màu” — mô hình chỉ tốt bằng dữ liệu đưa vào (rác vào → rác ra).", "Nghĩ mọi bài toán đều cần AI: nếu luật đơn giản và rõ ràng, if-else nhanh và chắc chắn hơn."],
  exercises=["Kể 5 ứng dụng AI quanh em, mỗi ứng dụng xác định: dữ liệu vào là gì, đầu ra là gì, có giám sát hay không.",
             "Sửa chương trình dùng cột <b>chiều rộng cánh hoa</b> (<code>iris.data[50:, 3]</code>). Ngưỡng tốt nhất và độ chính xác là bao nhiêu?"],
))
L.append(dict(
  id="du-lieu-numpy", short="Dữ liệu & numpy", title="Dữ liệu và thư viện numpy", icon="📊", time="2 giờ",
  goal="Biểu diễn dữ liệu dưới dạng bảng/mảng, dùng numpy để thống kê, lọc, làm sạch và chuẩn hoá.",
  goals=["Hiểu mẫu – đặc trưng – nhãn, ma trận X và vectơ y", "Tạo mảng numpy, shape, axis", "Tính trung bình, độ lệch chuẩn; lọc bằng điều kiện", "Chuẩn hoá min-max và z-score"],
  sections=[
    dict(h="Dữ liệu trong học máy", fig=figs.bang_du_lieu(), html="""
<p>Mọi dữ liệu (ảnh, âm thanh, số đo cảm biến) cuối cùng đều được biến thành <b>bảng số</b>. Quy ước: <code>X</code> là ma trận đặc trưng (mỗi hàng một mẫu), <code>y</code> là vectơ nhãn. Cài thư viện: <code>pip install numpy scikit-learn</code> (hoặc dùng <a href="https://colab.research.google.com" target="_blank" rel="noopener">Google Colab</a> – có sẵn mọi thứ, chạy trên trình duyệt).</p>"""),
    dict(h="numpy: tính toán trên cả mảng", code="02-numpy-du-lieu.py", html="""
<p><b>numpy</b> lưu dữ liệu trong mảng nhiều chiều và tính toán <b>trên cả mảng một lúc</b> (vectơ hoá) — nhanh hơn vòng lặp Python hàng chục lần vì phần lõi viết bằng C. <code>axis=0</code> là tính dọc theo cột (gộp các hàng), <code>axis=1</code> tính theo hàng.</p>""",
         notes=["<code>nhiet[nhiet &gt; 32]</code>: biểu thức điều kiện tạo mảng True/False, dùng làm “mặt nạ” để lọc.",
                "<code>(nhiet &gt; 32).sum()</code> đếm số phần tử thoả mãn vì True = 1.",
                "Cảm biến hỏng hay trả về giá trị vô lý (-999, 0, 85°C với DS18B20) – luôn <b>làm sạch</b> trước khi học.",
                "<code>default_rng(42)</code>: cùng seed → cùng dãy ngẫu nhiên, kết quả lặp lại được khi chạy lại."]),
    dict(h="Vì sao phải chuẩn hoá?", fig=figs.chuan_hoa(), html="""
<p>Diện tích (30–120) và số phòng (1–5) có thang đo khác nhau rất nhiều. Các thuật toán dựa vào <b>khoảng cách</b> (kNN, k-means) hoặc <b>gradient descent</b> sẽ bị đặc trưng có số lớn “lấn át”. Chuẩn hoá đưa mọi cột về cùng thang:</p>
<ul><li><b>min-max</b>: <code>(x − min) / (max − min)</code> → khoảng 0…1 (hay dùng cho ảnh, tín hiệu).</li>
<li><b>z-score</b>: <code>(x − trung bình) / độ lệch chuẩn</code> → trung bình 0, độ lệch 1 (<code>StandardScaler</code> trong scikit-learn).</li></ul>"""),
  ],
  mistakes=["Quên <code>axis</code> → tính trung bình của cả bảng thay vì từng cột.", "Chuẩn hoá bằng min/max của <b>toàn bộ</b> dữ liệu rồi mới chia train/test — làm “rò rỉ” thông tin dữ liệu kiểm tra."],
  exercises=["Tạo mảng 30 ngày nhiệt độ ngẫu nhiên 25–38°C, in ngày nóng nhất, số ngày trên 35°C, trung bình theo từng tuần (7 ngày).",
             "Cho mảng độ ẩm có giá trị lỗi 0 và 100, thay chúng bằng trung bình các giá trị hợp lệ."],
))
L.append(dict(
  id="hoi-quy", short="Hồi quy tuyến tính", title="Hồi quy tuyến tính và gradient descent", icon="📈", time="2,5 giờ",
  goal="Hiểu mô hình đầu tiên — đường thẳng khớp dữ liệu — và cách máy “học” bằng cách giảm dần sai số.",
  goals=["Mô hình y = w·x + b, hàm mất mát MSE", "Ý tưởng gradient descent và tốc độ học", "Tự cài bằng numpy và so sánh với LinearRegression", "Đánh giá bằng R²"],
  sections=[
    dict(h="Mô hình và hàm mất mát", fig=figs.hoi_quy_plot(), html="""
<p>Ta giả sử giá nhà tỉ lệ với diện tích: <code>giá ≈ w × diện_tích + b</code>. “Học” là tìm <code>w</code>, <code>b</code> sao cho đường thẳng <b>gần các điểm nhất</b>. Đo độ “gần” bằng <b>hàm mất mát</b> (loss) — ở đây là <b>MSE</b> (Mean Squared Error):</p>
<p style="text-align:center;font-family:var(--mono);font-weight:600">MSE = trung bình của (dự_đoán − thật)²</p>
<p>Bình phương để sai âm/dương không triệt tiêu nhau và phạt nặng sai số lớn.</p>"""),
    dict(h="Gradient descent – xuống dốc từng bước", fig=figs.gradient_descent(), code="03-hoi-quy-tuyen-tinh.py", html="""
<p>Hãy tưởng tượng MSE là một thung lũng, vị trí của ta là giá trị <code>w</code> hiện tại. Đạo hàm (độ dốc) cho biết đi hướng nào thì mất mát tăng; ta bước <b>ngược</b> hướng đó. Với MSE, đạo hàm tính được bằng công thức: <code>∂MSE/∂w = 2·trung_bình(sai × x)</code>, <code>∂MSE/∂b = 2·trung_bình(sai)</code>.</p>""",
         notes=["Sau ~20 vòng MSE gần như không giảm nữa → đã tới đáy; kết quả trùng với scikit-learn (giải bằng công thức đại số).",
                "Chuẩn hoá x trước giúp thung lũng “tròn”, đi nhanh; nếu không, phải chọn tốc độ học rất nhỏ.",
                "R² = 0.919: mô hình giải thích được ~92% sự thay đổi của giá; 1 là hoàn hảo, 0 là không hơn đoán bằng trung bình.",
                "Mạng nơ-ron khổng lồ (ChatGPT) cũng học bằng đúng ý tưởng này, chỉ là có hàng tỉ tham số thay vì 2."]),
  ],
  embedded=["<b>Hiệu chuẩn cảm biến:</b> đo cảm biến rẻ (ví dụ cảm biến độ ẩm đất điện dung) song song với thiết bị chuẩn, khớp đường thẳng <code>giá_trị_thật = w × ADC + b</code>, rồi chỉ cần nạp 2 số w, b vào Arduino.", "Dự báo xu hướng: khớp đường thẳng qua 10 phút số đo mực nước để báo trước khi bể tràn."],
  mistakes=["Tốc độ học quá lớn → MSE tăng vọt (phân kỳ); quá nhỏ → hàng nghìn vòng chưa tới.", "Dùng mô hình dự đoán xa ngoài vùng dữ liệu (nhà 1000 m²) — mô hình không biết gì ở đó."],
  exercises=["Thử <code>toc_do_hoc</code> = 0.01, 0.5, 1.1 và giải thích MSE thay đổi thế nào.",
             "Thu 10 cặp (giá trị ADC, nhiệt độ nhiệt kế) từ cảm biến LM35/NTC và tìm phương trình hiệu chuẩn."],
))
L.append(dict(
  id="knn", short="Phân loại kNN", title="Phân loại với k láng giềng gần nhất (kNN)", icon="🌸", time="2 giờ",
  goal="Hiểu bài toán phân loại, cài thuật toán kNN và làm quen quy trình scikit-learn: chia dữ liệu → fit → predict → score.",
  goals=["Khoảng cách Euclid giữa hai mẫu", "Cài kNN bằng numpy, ảnh hưởng của k", "Chia train/test với train_test_split", "API chung của scikit-learn"],
  sections=[
    dict(h="Ý tưởng: “Gần mực thì đen”", fig=figs.knn_plot(), html="""
<p>Muốn biết bông hoa mới thuộc loài nào, tìm <b>k</b> bông đã biết loài <b>giống nó nhất</b> (khoảng cách nhỏ nhất) rồi cho chúng <b>bỏ phiếu</b>. Khoảng cách Euclid giữa hai điểm (a₁, a₂) và (b₁, b₂): <code>√((a₁−b₁)² + (a₂−b₂)²)</code> — chính là định lý Pythago, mở rộng được cho bất kỳ số đặc trưng nào.</p>
<p>kNN “lười”: không học gì lúc huấn luyện, chỉ nhớ dữ liệu; mọi công việc dồn vào lúc dự đoán.</p>"""),
    dict(h="Chia dữ liệu học / kiểm tra", fig=figs.chia_du_lieu(), code="04-knn.py", html="""
<p>Mọi mô hình trong scikit-learn dùng chung 3 lệnh: <code>mo_hinh.fit(X, y)</code> (học), <code>mo_hinh.predict(X_moi)</code> (dự đoán), <code>mo_hinh.score(X, y)</code> (độ chính xác). Đổi thuật toán chỉ cần đổi 1 dòng tạo mô hình.</p>""",
         notes=["<code>np.argsort</code> trả về chỉ số sắp theo khoảng cách tăng dần; lấy <code>[:k]</code> là k láng giềng.",
                "<code>stratify=y</code>: tỉ lệ các loài trong tập học và tập kiểm tra giống nhau.",
                "Bông 4.9 × 1.7 cm nằm ngay ranh giới versicolor / virginica — dễ đoán sai nhất.",
                "k nhỏ dễ bị nhiễu bởi 1 điểm lạ; k quá lớn làm mờ ranh giới. Thường chọn k lẻ để tránh hoà phiếu."]),
  ],
  mistakes=["Không chuẩn hoá khi các đặc trưng khác thang đo — kNN gần như chỉ nhìn đặc trưng có số lớn nhất.", "Chấm điểm trên chính dữ liệu học (k = 1 sẽ luôn đúng 100%!)."],
  exercises=["Dùng cả 4 đặc trưng của Iris: độ chính xác thay đổi thế nào?", "Viết hàm vẽ “bản đồ” dự đoán: chạy kNN trên lưới điểm (chiều dài 1–7, chiều rộng 0–2.5) và in ký tự S/V/G."],
))
L.append(dict(
  id="danh-gia", short="Đánh giá mô hình", title="Đánh giá mô hình: độ chính xác chưa đủ", icon="🎯", time="2 giờ",
  goal="Đánh giá đúng chất lượng mô hình bằng ma trận nhầm lẫn, precision, recall và nhận biết quá khớp.",
  goals=["Đọc ma trận nhầm lẫn", "Hiểu precision và recall, khi nào ưu tiên cái nào", "Nhận biết underfit / overfit", "Dùng pipeline chuẩn hoá + mô hình"],
  sections=[
    dict(h="Ma trận nhầm lẫn, precision, recall", fig=figs.ma_tran_nham_lan(), code="05-danh-gia-mo-hinh.py", html="""
<p>Một mô hình chẩn đoán đoán “lành” cho mọi người vẫn có thể đạt accuracy 63% (vì 63% số ca là lành) — nhưng vô dụng. Cần nhìn <b>loại lỗi</b>: bỏ sót ca bệnh (âm tính giả) nguy hiểm hơn nhiều so với báo động nhầm (dương tính giả).</p>
<ul><li><b>Precision</b> (độ chuẩn): trong những lần mô hình nói “có”, bao nhiêu % đúng. Quan trọng khi báo nhầm gây hại (lọc thư rác xoá nhầm thư thật).</li>
<li><b>Recall</b> (độ phủ): trong tất cả các ca “có” thật, mô hình tìm ra bao nhiêu %. Quan trọng khi bỏ sót gây hại (bệnh, cháy, ngã).</li></ul>""",
         notes=["<code>make_pipeline(StandardScaler(), LogisticRegression())</code>: chuẩn hoá được “học” chỉ từ dữ liệu train rồi áp cho test — tránh rò rỉ.",
                "Logistic Regression là hồi quy tuyến tính + hàm sigmoid để ra xác suất 0…1 — một nơ-ron đơn (bài 8)."]),
    dict(h="Chưa khớp và quá khớp", fig=figs.qua_khop(), html="""
<p><b>Quá khớp (overfitting)</b>: mô hình quá phức tạp “học thuộc lòng” cả nhiễu của dữ liệu học, đúng tuyệt đối trên bài cũ nhưng sai trên bài mới. <b>Chưa khớp (underfitting)</b>: mô hình quá đơn giản, sai cả trên dữ liệu học. Dấu hiệu nhận biết: sai số học <b>thấp</b> nhưng sai số kiểm tra <b>cao</b> → quá khớp.</p>
<p>Cách chống quá khớp: thêm dữ liệu, chọn mô hình đơn giản hơn, giới hạn độ sâu cây / số vòng huấn luyện, kiểm tra chéo (cross-validation).</p>"""),
  ],
  mistakes=["Chỉ báo accuracy cho dữ liệu lệch lớp (99% không cháy, 1% cháy).", "Chỉnh mô hình nhiều lần theo điểm tập test — dần dần tập test cũng bị “học thuộc”; nên tách thêm tập validation."],
  exercises=["Thay <code>LogisticRegression</code> bằng <code>KNeighborsClassifier(5)</code>, so sánh recall lớp ác tính.",
             "Dùng <code>cross_val_score(mo_hinh, X, y, cv=5)</code> và giải thích vì sao kết quả đáng tin hơn chia 1 lần."],
))
L.append(dict(
  id="cay-quyet-dinh", short="Cây quyết định", title="Cây quyết định – mô hình giải thích được", icon="🌳", time="1,5 giờ",
  goal="Huấn luyện cây quyết định, đọc các luật máy học được và biết mức độ quan trọng của từng đặc trưng.",
  goals=["Cấu trúc cây: nút hỏi, nhánh, lá", "Độ sâu cây và quá khớp", "In luật bằng export_text, feature_importances_"],
  sections=[
    dict(h="Máy tự đặt câu hỏi", fig=figs.cay_fig(), html="""
<p>Cây quyết định giống trò chơi “20 câu hỏi”: mỗi bước chọn <b>một đặc trưng và một ngưỡng</b> chia dữ liệu thành hai phần “thuần” nhất (ít lẫn lộn nhãn nhất, đo bằng chỉ số Gini). Lặp lại với từng phần tới khi đạt độ sâu tối đa. Ưu điểm lớn: <b>con người đọc hiểu được</b>, và dễ chuyển thành if-else cho vi điều khiển.</p>"""),
    dict(h="Ví dụ: hệ thống tưới cây thông minh", code="06-cay-quyet-dinh.py", notes=[
      "Máy tìm lại gần đúng “luật thật” (độ ẩm 35%, mưa 60%, nhiệt độ 35°C) chỉ từ 200 mẫu dữ liệu.",
      "Có nút chia mà hai nhánh cùng ra <code>khong_tuoi</code> — vì xác suất bên trong khác nhau, nhưng nhãn đa số như nhau; có thể cắt tỉa.",
      "<code>max_depth=3</code> giới hạn cây 3 tầng: dễ đọc và tránh quá khớp. Không giới hạn, cây có thể học thuộc từng mẫu.",
      "Random Forest = trung bình hàng trăm cây khác nhau → chính xác và ổn định hơn một cây."]),
  ],
  embedded=["Cây quyết định là mô hình lý tưởng cho <b>Arduino</b>: sau khi học, nó chỉ là vài câu <code>if</code> lồng nhau, tốn vài chục byte và chạy trong vài micro giây. Bài 10 sẽ tự động sinh code C từ cây.", "Thay vì tự “chỉnh tay” ngưỡng cho hệ tưới cây / báo cháy, thu dữ liệu thật vài ngày và để cây quyết định tìm ngưỡng."],
  exercises=["Đổi <code>max_depth</code> thành 1, 2, 5, None; ghi độ chính xác trên tập test (nhớ chia train/test).",
             "Tự tạo dữ liệu “có nên bật quạt” từ nhiệt độ, độ ẩm, có người trong phòng; huấn luyện và in cây."],
))
L.append(dict(
  id="kmeans", short="Phân cụm k-means", title="Học không giám sát: phân cụm k-means", icon="🧩", time="1,5 giờ",
  goal="Tìm các nhóm tự nhiên trong dữ liệu không có nhãn bằng thuật toán k-means.",
  goals=["Khác biệt giữa có / không giám sát", "Hai bước lặp của k-means", "Ứng dụng: chia nhóm, đặt trạm, nén màu ảnh"],
  sections=[
    dict(h="Thuật toán k-means", fig=figs.kmeans_plot(), code="07-kmeans.py", html="""
<ol><li>Chọn ngẫu nhiên <b>k</b> tâm cụm.</li><li><b>Gán</b>: mỗi điểm thuộc về tâm gần nó nhất.</li>
<li><b>Cập nhật</b>: dời mỗi tâm về trung bình các điểm của nó.</li><li>Lặp bước 2–3 tới khi tâm không còn di chuyển.</li></ol>""",
         notes=["<code>X[:, None, :] - tam[None, :, :]</code>: kỹ thuật <i>broadcasting</i> của numpy, tính 90 × 3 khoảng cách không cần vòng lặp.",
                "k-means có thể hội tụ về kết quả kém nếu tâm ban đầu xấu → scikit-learn chạy nhiều lần (<code>n_init</code>) và giữ kết quả tốt nhất.",
                "Phải tự chọn k; “phương pháp khuỷu tay” vẽ tổng khoảng cách theo k và chọn chỗ đường cong gãy."]),
  ],
  exercises=["Chạy lại với k = 2 và k = 4; nhận xét vị trí các trạm.",
             "Dùng <code>sklearn.cluster.KMeans</code> nén ảnh: phân cụm màu các điểm ảnh thành 8 màu."],
))
L.append(dict(
  id="mang-no-ron", short="Mạng nơ-ron", title="Nơ-ron nhân tạo và mạng nơ-ron", icon="🧠", time="3 giờ",
  goal="Hiểu cấu tạo một nơ-ron, vì sao cần nhiều lớp, và cách mạng học bằng lan truyền ngược — tự cài bằng numpy.",
  goals=["Nơ-ron: tổng có trọng số + hàm kích hoạt", "Perceptron học AND / OR, thất bại với XOR", "Mạng 2 lớp, lan truyền xuôi / ngược", "Tự cài mạng học XOR"],
  sections=[
    dict(h="Một nơ-ron", fig=figs.noron(), code="08a-perceptron.py", html="""
<p>Lấy cảm hứng từ tế bào thần kinh: nhận nhiều tín hiệu, mỗi tín hiệu nhân với một <b>trọng số</b> (mức quan trọng), cộng lại với <b>độ lệch</b> b, rồi qua <b>hàm kích hoạt</b> quyết định “phát xung” hay không. Một nơ-ron thực chất vẽ ra <b>một đường thẳng</b> chia mặt phẳng làm hai.</p>""",
         notes=["Luật học perceptron: nếu đoán sai, cộng/trừ trọng số theo hướng làm giảm lỗi.",
                "AND, OR học được trong vài vòng; XOR thì không bao giờ — kết quả lịch sử khiến AI “ngủ đông” cuối thập niên 1960."]),
    dict(h="Vì sao cần nhiều lớp?", fig=figs.xor_fig(), html="""
<p>XOR cần hai đường thẳng để tách. Nhiều nơ-ron ở <b>lớp ẩn</b> mỗi cái vẽ một đường, nơ-ron lớp ra kết hợp chúng thành ranh giới cong bất kỳ. Thêm lớp, thêm nơ-ron → mô hình biểu diễn được quan hệ càng phức tạp: đó là <b>học sâu</b>.</p>"""),
    dict(h="Lan truyền ngược (backpropagation)", fig=figs.lan_truyen(), code="08b-mang-no-ron.py", html="""
<p>Huấn luyện mạng nhiều lớp vẫn là gradient descent (bài 3). Khó khăn là tính đạo hàm của mất mát theo trọng số ở lớp sâu bên trong — giải bằng <b>quy tắc chuỗi</b>, đi ngược từ lớp ra về lớp vào. Đạo hàm sigmoid đẹp: <code>σ'(z) = σ(z)(1 − σ(z))</code>.</p>""",
         notes=["Trong 500 vòng đầu mất mát giảm chậm (mạng đang “tìm hướng”), sau đó giảm rất nhanh.",
                "Chỉ 17 tham số đã học được XOR. Mạng nhận dạng ảnh có hàng triệu, mô hình ngôn ngữ lớn có hàng trăm tỉ.",
                "Thư viện thực tế (PyTorch, TensorFlow/Keras) tính đạo hàm tự động — nhưng bên trong làm đúng như đoạn code này."]),
  ],
  mistakes=["Khởi tạo mọi trọng số bằng 0 → các nơ-ron ẩn giống hệt nhau, mạng không học được; phải khởi tạo ngẫu nhiên.", "Quên chuẩn hoá đầu vào → sigmoid bão hoà, đạo hàm ≈ 0, mạng “đứng yên”."],
  exercises=["Đổi lớp ẩn còn 2 nơ-ron, thử vài seed khác nhau: lúc nào học được, lúc nào kẹt?", "Thay sigmoid ở lớp ẩn bằng ReLU (<code>np.maximum(0, z)</code>, đạo hàm <code>z &gt; 0</code>)."],
))
L.append(dict(
  id="chu-so", short="Nhận dạng chữ số", title="Nhận dạng chữ số viết tay", icon="✍️", time="2 giờ",
  goal="Dùng mạng nơ-ron MLP của scikit-learn để nhận dạng ảnh, hiểu ảnh được biến thành số như thế nào.",
  goals=["Ảnh = ma trận độ sáng điểm ảnh", "Duỗi ảnh thành vectơ đặc trưng", "Huấn luyện MLPClassifier, đọc ma trận nhầm lẫn 10×10", "Giới thiệu mạng tích chập (CNN)"],
  sections=[
    dict(h="Máy tính “nhìn” ảnh thế nào?", fig=figs.chu_so_grid(), html="""
<p>Ảnh xám là bảng số độ sáng. Bộ dữ liệu <b>digits</b> (có sẵn trong scikit-learn) gồm 1797 ảnh 8×8 điểm, mỗi điểm 0…16. Ảnh màu có 3 bảng (R, G, B); ảnh camera ESP32-CAM 320×240 là 230 400 con số.</p>"""),
    dict(h="Mạng nơ-ron nhận dạng chữ số", fig=figs.anh_thanh_vecto(), code="09-nhan-dang-chu-so.py", notes=[
      "Lớp ra có 10 nơ-ron, mỗi nơ-ron là “độ tin” cho một chữ số; chọn nơ-ron lớn nhất.",
      "97% trên ảnh chưa từng thấy. Những ảnh sai thường viết xấu thật — người cũng có thể nhầm.",
      "Ma trận nhầm lẫn cho thấy số 8 hay bị nhầm thành 1 — gợi ý cần thêm dữ liệu số 8."]),
    dict(h="Mạng tích chập (CNN) – bước tiếp theo", html="""
<p>Duỗi ảnh thành vectơ làm mất thông tin “điểm nào cạnh điểm nào”. <b>Mạng tích chập (CNN)</b> trượt các bộ lọc nhỏ 3×3 trên ảnh để phát hiện cạnh, góc, rồi hình dạng — giống cách mắt người nhìn. CNN là nền tảng của nhận dạng khuôn mặt, xe tự lái. Học tiếp với <b>Keras</b> trên Google Colab và bộ dữ liệu MNIST (ảnh 28×28) — đạt trên 99%.</p>
<p>Không cần code vẫn có thể thử ngay: <a href="https://teachablemachine.withgoogle.com" target="_blank" rel="noopener">Teachable Machine</a> của Google cho phép dùng webcam dạy máy nhận dạng đồ vật trong vài phút và xuất mô hình cho web/vi điều khiển.</p>"""),
  ],
  exercises=["Đổi <code>hidden_layer_sizes</code> thành (16,), (128,), (64, 32): ghi độ chính xác và thời gian.", "Vẽ một chữ số 8×8 bằng tay (mảng numpy) và cho mô hình đoán."],
))
L.append(dict(
  id="tinyml", short="Dự án TinyML", title="Dự án: AI trên vi điều khiển (TinyML) – phát hiện ngã", icon="🏁", time="3 giờ",
  goal="Đi trọn quy trình một dự án AI nhúng: thu dữ liệu cảm biến, trích đặc trưng, huấn luyện, xuất mô hình thành code C chạy trên ESP32.",
  goals=["Quy trình TinyML", "Trích đặc trưng từ tín hiệu thời gian", "Xuất cây quyết định thành hàm C", "Biết các công cụ: Edge Impulse, TensorFlow Lite Micro"],
  sections=[
    dict(h="TinyML là gì?", fig=figs.tinyml_flow(), html="""
<p><b>TinyML</b> là chạy mô hình AI trên vi điều khiển chỉ vài trăm KB RAM, tiêu thụ vài mW: không cần Internet, phản hồi tức thì, bảo mật dữ liệu. Ví dụ: đồng hồ phát hiện ngã, cảm biến rung dự đoán hỏng máy, nhận dạng từ khoá “OK Google”. Việc <b>huấn luyện</b> (nặng) làm trên máy tính; vi điều khiển chỉ <b>suy luận</b> (nhẹ).</p>"""),
    dict(h="Đặc trưng từ cảm biến gia tốc", fig=figs.tin_hieu_gia_toc(), html="""
<p>Đưa nguyên 50 mẫu thô vào mô hình sẽ tốn bộ nhớ và cần nhiều dữ liệu. Thay vào đó tính vài <b>đặc trưng</b> đơn giản trên mỗi cửa sổ 1 giây: <b>độ lệch chuẩn</b> (mức rung lắc), <b>giá trị lớn nhất</b> (cú va đập), <b>biến thiên trung bình</b> (thay đổi nhanh hay chậm). Các phép tính này dễ viết lại trên Arduino.</p>"""),
    dict(h="Huấn luyện và xuất code C", code="10-du-an-tinyml.py", notes=[
      "Dữ liệu ở đây được <b>giả lập</b> cho dễ chạy; dự án thật cần thu dữ liệu từ MPU6050 với nhiều người, nhiều tư thế (xem khóa Arduino &amp; ESP32 bài cảm biến và Serial).",
      "Hàm sinh code duyệt cây đệ quy: nút trong → <code>if/else</code>, lá → <code>return nhãn</code>.",
      "Mô hình 7 nút: vài trăm byte Flash, chạy trong vài micro giây — ESP32 có thể kiểm tra 50 lần/giây mà không tốn sức."],
         after="""<p>Trên ESP32, mỗi giây tính 3 đặc trưng từ bộ đệm 50 mẫu rồi gọi hàm vừa sinh:</p>
<pre style="background:#0f172a;color:#e2e8f0;padding:12px 14px;border-radius:8px;overflow:auto;font-size:.82rem"><code>float buf[50];  // |a| đọc từ MPU6050 mỗi 20 ms
void kiemTra() {
  float tb = 0, mx = 0, bt = 0, dl = 0;
  for (int i = 0; i &lt; 50; i++) { tb += buf[i]; mx = max(mx, buf[i]); if (i) bt += fabs(buf[i] - buf[i - 1]); }
  tb /= 50; bt /= 49;
  for (int i = 0; i &lt; 50; i++) dl += (buf[i] - tb) * (buf[i] - tb);
  dl = sqrt(dl / 50);
  if (nhanDangHoatDong(dl, mx, bt) == 3) guiCanhBao();   // còi + MQTT tới điện thoại
}</code></pre>"""),
    dict(h="Công cụ cho dự án lớn hơn", html="""
<table class="tbl"><tr><th>Công cụ</th><th>Dùng khi</th></tr>
<tr><td><a href="https://edgeimpulse.com" target="_blank" rel="noopener">Edge Impulse</a></td><td>nền tảng web: thu dữ liệu trực tiếp từ board, huấn luyện, xuất thư viện Arduino – phù hợp nhất cho học sinh</td></tr>
<tr><td>TensorFlow Lite Micro</td><td>chạy mạng nơ-ron (kể cả CNN nhỏ) trên ESP32, Arduino Nano 33 BLE</td></tr>
<tr><td>micromlgen / m2cgen</td><td>chuyển mô hình scikit-learn (cây, SVM, random forest) thành code C</td></tr>
<tr><td>ESP32-CAM + ESP-WHO</td><td>nhận diện khuôn mặt, phát hiện người</td></tr></table>"""),
  ],
  summary=["Học máy = tìm tham số mô hình để giảm hàm mất mát trên dữ liệu; đánh giá trên dữ liệu chưa thấy.",
           "Quy trình: dữ liệu → làm sạch, chuẩn hoá → chọn mô hình → huấn luyện → đánh giá (precision/recall, quá khớp) → triển khai.",
           "Mô hình nhỏ (cây, mạng nơ-ron nhỏ) có thể chạy ngay trên ESP32 — kết hợp AI với hệ nhúng là hướng rất mạnh cho các cuộc thi KHKT, STEM."],
  exercises=["Thêm hoạt động “nhảy” (gia tốc lớn có chu kỳ) vào bộ giả lập, huấn luyện lại và xem cây thay đổi thế nào.",
             "Dự án nhóm: gắn MPU6050 lên ESP32, gửi dữ liệu qua Serial ở dạng CSV, thu ≥ 100 cửa sổ mỗi hoạt động, huấn luyện bằng chương trình trên và nạp hàm C vào board."],
))

GROUPS = [("nen-tang", "Nền tảng", "AI là gì, dữ liệu, hồi quy", L[:3]),
          ("hoc-may", "Học máy cổ điển", "kNN, đánh giá, cây quyết định, k-means", L[3:7]),
          ("hoc-sau", "Mạng nơ-ron & dự án", "Nơ-ron, nhận dạng ảnh, TinyML", L[7:])]

_road = "".join(f'<div class="road"><div class="rb">Buổi {i + 1}</div><div><a href="#{x["id"]}">{x["title"]}</a><br><small>{x["time"]}</small></div></div>' for i, x in enumerate(L))
OVERVIEW = f"""
<h3><span class="n">?</span>Khóa học dành cho ai?</h3>
<div class="prose"><p>Học sinh từ <b>lớp 8</b> trở lên đã học <a href="python-co-ban.html">Python cơ bản</a> (biến, vòng lặp, list, hàm). Không cần toán cao cấp — mọi công thức được giải thích bằng hình và code; chỉ cần biết phương trình đường thẳng và định lý Pythago.</p>
<p>Điểm khác biệt: <b>tự cài đặt</b> các thuật toán cốt lõi (gradient descent, kNN, k-means, mạng nơ-ron, lan truyền ngược) bằng numpy để hiểu bản chất, sau đó dùng <b>scikit-learn</b> như trong thực tế — và kết thúc bằng dự án <b>AI chạy trên ESP32</b>.</p></div>
<div class="grid3"><div class="card"><h5>📖 {len(L)} bài</h5><p>Mục tiêu, lý thuyết kèm hình vẽ từ dữ liệu thật, lỗi hay gặp, bài tập.</p></div>
<div class="card"><h5>▶ 11 chương trình</h5><p>Kết quả trong trang là kết quả chạy thật; chạy lại được trên máy hoặc Google Colab.</p></div>
<div class="card"><h5>🔌 AI + hệ nhúng</h5><p>Hiệu chuẩn cảm biến, cây quyết định thành code C, phát hiện ngã bằng MPU6050.</p></div></div>
<h3><span class="n">⚙</span>Chuẩn bị</h3>
<div class="prose"><p>Cách nhanh nhất: mở <a href="https://colab.research.google.com" target="_blank" rel="noopener">Google Colab</a>, dán code và chạy (có sẵn numpy, scikit-learn). Hoặc trên máy: <code>pip install numpy scikit-learn</code>.</p></div>
<h3><span class="n">⌚</span>Lộ trình gợi ý — {len(L)} buổi</h3><div class="roadmap">{_road}</div>
<h3><span class="n">→</span>Khóa liên quan</h3>
<div class="grid3"><div class="card"><h5><a href="python-co-ban.html">🐍 Python cơ bản</a></h5><p>Học trước khóa này nếu chưa biết Python.</p></div>
<div class="card"><h5><a href="arduino-esp32.html">🔌 Arduino &amp; ESP32</a></h5><p>Thu dữ liệu cảm biến, chạy mô hình trên board.</p></div>
<div class="card"><h5><a href="freertos.html">⏱ FreeRTOS</a></h5><p>Chạy song song đọc cảm biến, suy luận và gửi dữ liệu.</p></div></div>
"""

COURSE = dict(
    slug="ai-co-ban", title="AI cơ bản", short_title="AI cơ bản", icon="🤖", lang="py",
    badge=f"{len(L)} bài · lớp 8+", tagline="Trí tuệ nhân tạo từ gốc: dữ liệu, hồi quy, phân loại, đánh giá mô hình, mạng nơ-ron tự viết bằng numpy, nhận dạng chữ số — và AI chạy trên ESP32.",
    stats=[("bài học", str(len(L))), ("chương trình", "11"), ("hình từ dữ liệu thật", "21")],
    header_sub=f"Khóa học: 🤖 AI cơ bản với Python · {len(L)} buổi",
    gradient=["#4c1d95", "#7c3aed", "#ec4899"], storage="ai", overview=OVERVIEW, groups=GROUPS, code_dir=CODE, runner=run,
)

if __name__ == "__main__":
    coursekit.build(COURSE, os.path.abspath(os.path.join(HERE, "..", "..", "training", "ai-co-ban.html")))
