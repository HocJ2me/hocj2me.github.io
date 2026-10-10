# -*- coding: utf-8 -*-
"""Khóa Lập trình nhúng với Arduino & ESP32.  Build: python -X utf8 course.py
Sketch .ino chạy trên bộ mô phỏng sim/ (Arduino.h giả lập: thời gian ảo, chân I/O, ADC, PWM, Serial, ngắt, thiết bị, WiFi, MQTT)."""
import glob, hashlib, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "common")]
import coursekit
import figs

CODE = os.path.join(HERE, "code")
SIM = os.path.join(HERE, "sim")
_runner = coursekit.Runner(os.path.join(HERE, "out", "run-cache.json"))


def _simver():
    h = hashlib.sha1()
    for f in sorted(glob.glob(os.path.join(SIM, "*"))):
        h.update(open(f, "rb").read())
    return h.hexdigest()[:10]


def run(path, stdin):
    """Biên dịch sketch .ino + kịch bản .sim.cpp + bộ mô phỏng bằng g++, chạy và lấy kết quả (có cache)."""
    scen = path[:-4] + ".sim.cpp"

    def go():
        exe = os.path.join(tempfile.mkdtemp(), "sketch.exe")
        cmd = ["g++", "-std=gnu++17", "-O1", "-Wall", f"-I{SIM}", "-include", "Arduino.h",
               "-x", "c++", path, "-x", "none", scen, os.path.join(SIM, "sim_main.cpp"), "-static", "-o", exe]
        c = subprocess.run(cmd, capture_output=True)
        if c.returncode:
            sys.exit(f"Lỗi biên dịch {path}:\n{c.stderr.decode('utf-8', 'replace')[-3000:]}")
        r = subprocess.run([exe], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
        print("  chạy", os.path.basename(path))
        return r.stdout.decode("utf-8", "replace").replace("\r\n", "\n").rstrip()

    out = _runner.run([open(path, "rb").read(), open(scen, "rb").read(), _simver()], go)
    return "Arduino IDE: chọn board → Upload  (kết quả bên dưới chạy trên bộ mô phỏng của khóa)", out


def sk(n):
    return n + ".ino"


L = []
L.append(dict(
  id="gioi-thieu", short="Làm quen Arduino & ESP32", title="Làm quen Arduino, ESP32 và chương trình Blink", icon="🔌", time="2 giờ",
  goal="Hiểu vi điều khiển là gì, chọn board phù hợp, cài Arduino IDE và nạp chương trình đầu tiên.",
  goals=["Phân biệt Arduino Uno và ESP32", "Cài Arduino IDE, thêm board ESP32, chọn cổng COM", "Hiểu cấu trúc setup() / loop()", "Nạp và quan sát chương trình Blink"],
  sections=[
    dict(h="Vi điều khiển là gì?", fig=figs.board_compare(), html="""
<p><b>Vi điều khiển</b> (microcontroller) là một máy tính tí hon trên một con chip: có CPU, bộ nhớ và các chân vào/ra để đọc cảm biến, điều khiển đèn, động cơ. <b>Arduino</b> là nền tảng giúp lập trình vi điều khiển dễ dàng (board + phần mềm + thư viện). <b>ESP32</b> mạnh hơn nhiều và có sẵn WiFi, Bluetooth — lựa chọn số 1 cho dự án IoT, lập trình bằng chính Arduino IDE.</p>
<div class="callout warn">⚠️ Chân ESP32 chạy ở <b>3.3 V</b>: cấp 5 V vào chân tín hiệu có thể làm hỏng chip. Cảm biến 5 V cần mạch chuyển mức hoặc cầu phân áp.</div>"""),
    dict(h="Cấu trúc chương trình và Arduino IDE", fig=figs.sketch_structure(), html="""
<ol><li>Tải Arduino IDE 2 tại arduino.cc. Với ESP32: <b>File → Preferences → Additional boards URL</b>: <code>https://espressif.github.io/arduino-esp32/package_esp32_index.json</code>, rồi <b>Boards Manager</b> → cài “esp32 by Espressif”.</li>
<li>Cắm board, chọn <b>Tools → Board</b> và <b>Tools → Port</b>. Không thấy cổng COM: cài driver CH340 hoặc CP2102.</li>
<li>Bấm <b>Upload</b>. Một số board ESP32 cần giữ nút BOOT khi hiện “Connecting…”.</li></ol>"""),
    dict(h="Blink – chương trình đầu tiên", code=sk("01-blink"), notes=[
      "Kết quả ở đây chạy trên <b>bộ mô phỏng</b> của khóa: dòng chữ thường là những gì in ra Serial Monitor, dòng <code>⚡</code> là trạng thái chân thay đổi kèm thời điểm.",
      "<code>pinMode(chân, OUTPUT)</code> phải gọi trước khi <code>digitalWrite</code>.",
      "<code>delay(500)</code> dừng toàn bộ chương trình 500 ms — đơn giản nhưng sẽ gây vấn đề ở bài 8."]),
  ],
  mistakes=["Chọn sai board/cổng COM → lỗi upload.", "Dùng cáp USB chỉ sạc (không có dây dữ liệu).", "Quên tốc độ baud Serial Monitor khớp với Serial.begin()."],
  exercises=["Đổi chu kỳ nháy thành 100 ms sáng – 900 ms tắt.", "Nháy LED theo mã Morse “SOS”."],
  refs=[("Arduino – Getting started", "https://docs.arduino.cc/learn/starting-guide/getting-started-arduino/"), ("Arduino-ESP32 docs", "https://docs.espressif.com/projects/arduino-esp32/en/latest/")],
))
L.append(dict(
  id="digital-out", short="Ngõ ra số: LED", title="Ngõ ra số: LED, điện trở và đèn giao thông", icon="🚦", time="2 giờ",
  goal="Điều khiển LED an toàn: tính điện trở hạn dòng, nối mạch đúng và viết chương trình đèn giao thông.",
  goals=["Đọc sơ đồ mạch LED, tính điện trở", "Dùng breadboard", "Viết hàm phụ để code gọn"],
  sections=[dict(h="Mạch LED", fig=figs.led_circuit(), html="<p>Mỗi chân vi điều khiển chỉ chịu dòng nhỏ (Uno ~20 mA, ESP32 ~12 mA khuyến nghị). LED luôn phải có <b>điện trở hạn dòng</b> nối tiếp. Tải lớn (động cơ, đèn 12 V, quạt) phải qua transistor, MOSFET hoặc relay.</p>"),
            dict(h="Đèn giao thông", code=sk("02-den-giao-thong"), notes=["Hàm <code>batDen()</code> đảm bảo luôn chỉ một đèn sáng — tránh lặp code 3 lần ở mỗi pha.",
                                                                          "Bộ mô phỏng chỉ ghi lại khi trạng thái chân THAY ĐỔI."])],
  exercises=["Thêm đèn cho người đi bộ (xanh khi đèn xe đỏ).", "Đèn vàng nhấp nháy ban đêm (chế độ chọn bằng biến)."],
))
L.append(dict(
  id="digital-in", short="Ngõ vào số: nút nhấn", title="Ngõ vào số: nút nhấn, điện trở kéo lên, chống dội", icon="🔘", time="2 giờ",
  goal="Đọc nút nhấn ổn định, hiểu vì sao cần điện trở kéo lên/xuống và chống dội phím.",
  goals=["digitalRead và INPUT_PULLUP", "Hiện tượng dội phím và cách chống", "Phát hiện cạnh (vừa nhấn) thay vì mức"],
  sections=[dict(h="Nút nhấn và điện trở kéo lên", fig=figs.pullup()),
            dict(h="Chống dội phím", fig=figs.bounce(), code=sk("03-nut-nhan"), notes=[
              "Kịch bản mô phỏng: nhấn 3 lần lúc 300, 900, 1600 ms; mỗi lần tiếp điểm nảy loạn 8 ms đầu.",
              "Không chống dội, mỗi lần nhấn có thể bị đếm thành 3–5 lần. Ở đây LED đổi trạng thái đúng 3 lần.",
              "Chỉ xử lý ở <b>cạnh xuống</b> (HIGH → LOW) nên giữ nút lâu cũng chỉ tính một lần."])],
  mistakes=["Dùng INPUT không có điện trở kéo → đọc lung tung.", "Nối nút giữa chân và 5 V khi dùng INPUT_PULLUP → không bao giờ thấy LOW."],
  exercises=["Nút thứ hai giảm số đếm; hiển thị số lên Serial.", "Nhấn giữ 2 giây mới bật thiết bị."],
))
L.append(dict(
  id="analog-in", short="Ngõ vào analog", title="Ngõ vào analog: ADC, biến trở, quang trở", icon="🎚️", time="2 giờ",
  goal="Đọc tín hiệu liên tục (ánh sáng, vị trí biến trở, điện áp) bằng ADC và quy đổi sang đại lượng thật.",
  goals=["Hiểu ADC 10 bit / 12 bit", "Cầu phân áp với cảm biến điện trở", "Đổi giá trị ADC ra volt, phần trăm bằng map()"],
  sections=[dict(h="Cầu phân áp và ADC", fig=figs.ldr_divider(), html="<p><code>analogRead()</code> trả về số tỉ lệ với điện áp ở chân: ESP32 0–4095 cho 0–3.3 V (12 bit), Uno 0–1023 cho 0–5 V (10 bit). Cảm biến dạng điện trở (LDR, NTC, cảm biến uốn) cần thêm một điện trở để tạo cầu phân áp.</p><div class='callout'>💡 ESP32: chỉ dùng chân ADC1 (GPIO 32–39) khi bật WiFi; ADC ESP32 hơi phi tuyến ở hai đầu thang đo — nên hiệu chuẩn.</div>"),
            dict(h="Đèn ngủ tự động", code=sk("04-den-ngu-tu-dong"), notes=["Kịch bản: trời tối dần, ánh sáng giảm từ 3200 xuống 500; biến trở đặt ngưỡng 1500.",
                                                                           "Đèn bật lúc 2000 ms khi ánh sáng xuống dưới ngưỡng.",
                                                                           "Thực tế nên thêm vùng trễ (hysteresis): bật dưới 1400, tắt trên 1600 để đèn không chập chờn."])],
  exercises=["Thêm vùng trễ cho đèn ngủ.", "Đo điện áp pin 9 V bằng cầu phân áp 20k/10k và in ra volt."],
))
L.append(dict(
  id="pwm", short="PWM, servo, động cơ", title="PWM: độ sáng LED, servo và tốc độ động cơ", icon="〰️", time="2 giờ",
  goal="Tạo “điện áp trung bình” bằng PWM để chỉnh độ sáng, tốc độ động cơ và điều khiển servo.",
  goals=["Hiểu duty cycle", "analogWrite (Uno) và ledcAttach/ledcWrite (ESP32)", "Điều khiển servo bằng thư viện", "Nối động cơ qua driver"],
  sections=[dict(h="PWM là gì?", fig=figs.pwm_waves(), code=sk("05a-pwm-den-tho"), notes=["Mỗi bước tăng 51 ≈ 20% độ sáng.", "Arduino Uno chỉ có PWM ở chân có dấu ~ (3, 5, 6, 9, 10, 11)."]),
            dict(h="Servo và động cơ DC", code=sk("05b-servo-dong-co"), html="""
<p><b>Servo</b> nhận xung 50 Hz, độ rộng 0.5–2.5 ms tương ứng 0–180° — thư viện lo hết, ta chỉ gọi <code>servo.write(goc)</code>. <b>Động cơ DC</b> kéo dòng lớn và sinh nhiễu: luôn qua <b>driver</b> (L298N, TB6612, DRV8833), PWM vào chân ENA/PWMA, hai chân IN chọn chiều quay. Nguồn động cơ tách riêng, <b>nối chung GND</b> với vi điều khiển.</p>""",
                 notes=["Kịch bản: người dùng vặn biến trở từ 0 lên hết rồi về giữa.", "Tần số PWM 20 kHz cho động cơ không còn tiếng rít nghe được."])],
  mistakes=["Cấp nguồn servo/động cơ trực tiếp từ chân 5V của board → board reset liên tục.", "Quên nối chung GND giữa nguồn động cơ và board."],
  exercises=["Đèn thở dùng hàm sin cho mượt hơn.", "Servo quét 0–180° như radar, mỗi bước 5°."],
))
L.append(dict(
  id="serial", short="Giao tiếp Serial", title="Giao tiếp Serial: in dữ liệu và nhận lệnh", icon="💬", time="1,5 giờ",
  goal="Dùng Serial để gỡ lỗi, gửi dữ liệu lên máy tính và nhận lệnh điều khiển (từ máy tính, Bluetooth, module khác).",
  goals=["Serial.print / println / printf", "Đọc lệnh theo dòng với readStringUntil", "Phân tích lệnh và trả lời"],
  sections=[dict(h="Bộ xử lý lệnh", code=sk("06-lenh-serial"), html="<p>UART (Serial) truyền từng byte trên 2 dây TX/RX. Cùng mã nhận lệnh này dùng được cho module Bluetooth HC-05 (nối vào Serial2) hoặc Bluetooth có sẵn của ESP32 (<code>BluetoothSerial</code>).</p>",
                 notes=["Kịch bản: 5 lệnh được “gõ” ở các thời điểm khác nhau, có cả lệnh viết thường và lệnh sai.", "<code>trim()</code> bỏ ký tự <code>\\r</code> thừa khi Serial Monitor gửi “Both NL &amp; CR”.",
                        "Mẫu “lệnh + tham số” (PWM 180) là cách đơn giản nhất để điều khiển robot từ máy tính hoặc app."])],
  exercises=["Thêm lệnh <code>SERVO &lt;góc&gt;</code>.", "Gửi dữ liệu cảm biến dạng CSV mỗi giây rồi vẽ đồ thị bằng Serial Plotter."],
))
L.append(dict(
  id="cam-bien", short="Cảm biến", title="Cảm biến: nhiệt độ – độ ẩm DHT22 và siêu âm HC-SR04", icon="🌡️", time="2 giờ",
  goal="Dùng thư viện cảm biến số và cảm biến đo thời gian; xử lý giá trị lỗi.",
  goals=["Cài và dùng thư viện DHT", "Kiểm tra giá trị lỗi (NaN)", "Đo khoảng cách bằng pulseIn", "Ra quyết định theo ngưỡng"],
  sections=[dict(h="DHT22", code=sk("07a-dht22"), html="<p>Cài thư viện: <b>Library Manager</b> → “DHT sensor library” (Adafruit). DHT22 chính xác hơn DHT11 (±0.5°C), đọc tối đa mỗi 2 giây; chân DATA cần điện trở kéo lên 10 kΩ (module thường có sẵn).</p>",
                 notes=["Kịch bản: phòng nóng và ẩm dần lên.", "Quạt bật khi nhiệt độ ≥ 30°C, cảnh báo khi độ ẩm ≥ 80%."]),
            dict(h="Siêu âm HC-SR04", fig=figs.ultrasonic(), code=sk("07b-sieu-am"), notes=["Kịch bản: xe lùi dần từ 80 cm tới 5 cm.", "<code>pulseIn</code> có timeout 30 ms (~5 m) để không bị treo khi không có vật cản."])],
  mistakes=["Đọc DHT liên tục không có delay → toàn NaN.", "Cấp 5 V cho chân ECHO vào ESP32 không qua phân áp."],
  exercises=["Hiển thị khoảng cách bằng 5 LED như vạch đo.", "Tính chỉ số nóng bức (heat index) từ nhiệt độ và độ ẩm."],
))
L.append(dict(
  id="da-nhiem", short="Đa nhiệm với millis()", title="Làm nhiều việc cùng lúc với millis() và máy trạng thái", icon="⏱", time="2 giờ",
  goal="Bỏ delay(), viết chương trình phản hồi nhanh làm nhiều việc song song; tổ chức logic bằng máy trạng thái.",
  goals=["Kỹ thuật “đã đủ thời gian chưa?” với millis()", "Máy trạng thái bằng enum + switch", "Chống dội không chặn"],
  sections=[dict(h="Ba việc song song", code=sk("08-da-nhiem-millis"), html="<p>Mỗi việc có biến “lần cuối làm” riêng; mỗi vòng <code>loop()</code> chỉ kiểm tra <code>millis() - lanCuoi &gt;= chuKy</code>. Không việc nào chặn việc nào, nút nhấn được phản hồi ngay.</p>",
                 notes=["Kịch bản: nhiệt độ ~32°C rồi giảm ~28°C; nút nhấn lúc 1720 ms và 2650 ms.", "LED nháy đều đặn 250 ms trong khi vẫn đọc cảm biến và nút.",
                        "Khi chương trình lớn hơn nữa, bước tiếp theo là RTOS — xem khóa <a href='freertos.html'>FreeRTOS</a>."])],
  exercises=["Thêm việc thứ tư: gửi dữ liệu lên Serial mỗi 5 giây.", "Viết lại bài đèn giao thông bằng millis() + máy trạng thái để thêm nút sang đường."],
))
L.append(dict(
  id="ngat", short="Ngắt (interrupt)", title="Ngắt ngoài: đếm xung encoder, không bỏ sót sự kiện", icon="⚡", time="1,5 giờ",
  goal="Dùng ngắt để phản ứng tức thì với sự kiện phần cứng và đếm xung tốc độ cao.",
  goals=["attachInterrupt với RISING/FALLING/CHANGE", "Viết ISR ngắn, dùng volatile", "Đọc biến chung an toàn"],
  sections=[dict(h="Đếm xung encoder", code=sk("09-ngat-dem-xung"), html="<p>Ngắt tạm dừng chương trình chính để chạy hàm phục vụ ngắt (ISR) ngay khi chân thay đổi. ISR phải <b>thật ngắn</b>: không <code>delay</code>, không <code>Serial.print</code>. Trên ESP32 thêm <code>IRAM_ATTR</code>.</p>",
                 notes=["Kịch bản: bánh xe tăng tốc, chu kỳ xung giảm từ 20 ms xuống 5 ms.", "Dù loop() bận <code>delay(500)</code>, không xung nào bị mất.",
                        "<code>noInterrupts()/interrupts()</code> bảo vệ lúc đọc biến nhiều byte dùng chung với ISR."])],
  exercises=["Đếm số lần cửa mở bằng công tắc từ (reed switch) qua ngắt.", "Tính tốc độ quạt (RPM) bằng cảm biến Hall."],
))
L.append(dict(
  id="i2c-lcd", short="I2C & màn hình LCD", title="Giao tiếp I2C và màn hình LCD 16x2", icon="🖥️", time="1,5 giờ",
  goal="Nối nhiều thiết bị chỉ với 2 dây I2C, quét địa chỉ và hiển thị dữ liệu lên LCD.",
  goals=["Hiểu bus I2C, địa chỉ thiết bị", "Quét I2C để tìm địa chỉ", "Dùng LiquidCrystal_I2C"],
  sections=[dict(h="Bus I2C", fig=figs.i2c_bus()),
            dict(h="Trạm thời tiết có màn hình", code=sk("10-lcd-i2c"), notes=["Quét bus tìm thấy LCD (0x27) và cảm biến BME280 (0x76).",
                                                                            "LCD hiển thị lại mỗi 2 giây; khung trong kết quả là nội dung 16x2 thật trên màn hình.",
                                                                            "Màn hình không hiện chữ: vặn biến trở tương phản phía sau module."])],
  exercises=["Thêm biểu tượng độ (°) bằng ký tự tự tạo (createChar).", "Thay LCD bằng màn hình OLED SSD1306 (thư viện Adafruit SSD1306)."],
))
L.append(dict(
  id="wifi-web", short="ESP32 WiFi & web", title="ESP32: WiFi và web server điều khiển thiết bị", icon="📶", time="2 giờ",
  goal="Kết nối ESP32 vào WiFi và tạo trang web điều khiển đèn, đọc nhiệt độ từ điện thoại.",
  goals=["Kết nối WiFi chế độ STA", "Tạo WebServer, gắn đường dẫn với hàm", "Đọc tham số URL, trả HTML và JSON"],
  sections=[dict(h="Web server trên ESP32", fig=figs.web_server(), code=sk("11-esp32-web-server"), notes=[
      "Kịch bản: kết nối WiFi mất 1.5 giây, sau đó trình duyệt lần lượt mở 5 đường dẫn.", "Đường dẫn trả JSON (<code>/nhiet-do</code>) để app hoặc trang web khác đọc dữ liệu.",
      "Muốn truy cập từ xa (ngoài nhà) dùng MQTT hoặc dịch vụ như Blynk, Firebase — bài 12."])],
  exercises=["Thêm thanh trượt điều chỉnh độ sáng đèn qua <code>/sang?muc=0..255</code>.", "Chế độ Access Point: ESP32 tự phát WiFi (<code>WiFi.softAP</code>)."],
))
L.append(dict(
  id="iot-du-an", short="IoT & dự án nhà thông minh", title="IoT với MQTT và dự án nhà thông minh", icon="🏠", time="3 giờ",
  goal="Đưa dữ liệu lên Internet bằng MQTT, nhận lệnh từ app, kết hợp mọi kỹ năng trong một dự án hoàn chỉnh.",
  goals=["Hiểu mô hình publish/subscribe, topic, broker", "Dùng PubSubClient gửi JSON và nhận lệnh", "Thiết kế chế độ tự động / thủ công"],
  sections=[dict(h="MQTT", fig=figs.mqtt(), html="<p>Broker miễn phí để thử: <code>broker.hivemq.com</code>, <code>test.mosquitto.org</code>. App điện thoại: <b>IoT MQTT Panel</b>, <b>MQTT Dash</b>; dashboard: Node-RED, Home Assistant. Thư viện: <b>PubSubClient</b> (Nick O'Leary).</p>"),
            dict(h="Dự án nhà thông minh", code=sk("12-du-an-nha-thong-minh"), notes=[
              "Kịch bản: nhiệt độ tăng dần, lúc 4.5 s app chuyển chế độ thủ công và bật đèn, trời tối lúc 5 s, lúc 7.8 s trả về tự động.",
              "Ở chế độ thủ công, logic tự động không ghi đè lệnh người dùng.", "Dữ liệu gửi dạng JSON để app/dashboard dễ đọc."])],
  summary=["Ngõ ra/vào số, analog, PWM là 4 kỹ năng nền của mọi dự án.", "Bỏ delay(): dùng millis(), máy trạng thái, ngắt.",
           "Giao tiếp: Serial, I2C, WiFi/HTTP, MQTT.", "Học tiếp: <a href='freertos.html'>FreeRTOS</a>, <a href='pcb-altium.html'>thiết kế mạch PCB</a> để làm sản phẩm hoàn chỉnh."],
  exercises=["Thêm cảm biến khí gas MQ-2: vượt ngưỡng thì bật còi và gửi cảnh báo MQTT ngay.", "Lưu cấu hình (ngưỡng, chế độ) vào bộ nhớ Preferences của ESP32 để không mất khi mất điện."],
))

GROUPS = [("co-ban", "Vào/ra cơ bản", "LED, nút, analog, PWM", L[:5]), ("giao-tiep", "Cảm biến & lập trình", "Serial, cảm biến, millis, ngắt, I2C", L[5:10]),
          ("iot", "ESP32 & IoT", "WiFi, web server, MQTT, dự án", L[10:])]

_road = "".join(f'<div class="road"><div class="rb">Buổi {i + 1}</div><div><a href="#{x["id"]}">{x["title"]}</a><br><small>{x["time"]}</small></div></div>' for i, x in enumerate(L))
OVERVIEW = f"""
<h3><span class="n">?</span>Khóa học dành cho ai?</h3>
<div class="prose"><p>Học sinh THCS–THPT đã biết lập trình cơ bản (Python, C++ hoặc kéo thả) muốn làm <b>sản phẩm thật</b>: robot, nhà thông minh, trạm quan trắc, dự án thi Khoa học kỹ thuật. Khóa dùng Arduino IDE (ngôn ngữ C/C++), áp dụng cho cả Arduino Uno và ESP32.</p></div>
<div class="grid3"><div class="card"><h5>🧰 Bộ linh kiện gợi ý</h5><p>ESP32 DevKit, breadboard, dây cắm, LED, điện trở, nút nhấn, biến trở, LDR, DHT22, HC-SR04, servo SG90, LCD I2C, driver động cơ.</p></div>
<div class="card"><h5>▶ Chạy được ngay cả khi chưa có linh kiện</h5><p>Mọi sketch trong khóa có kết quả từ <b>bộ mô phỏng Arduino</b> viết riêng cho khóa: thấy rõ chân nào bật lúc mấy ms, Serial in gì.</p></div>
<div class="card"><h5>🏠 Dự án IoT</h5><p>Kết thúc bằng nhà thông minh điều khiển qua app, dữ liệu lên Internet bằng MQTT.</p></div></div>
<div class="callout">💡 Muốn mô phỏng mạch trực quan trên trình duyệt: <a href="https://wokwi.com" target="_blank" rel="noopener">wokwi.com</a> hỗ trợ cả Arduino Uno và ESP32 — dán code của khóa vào là chạy.</div>
<h3><span class="n">⌚</span>Lộ trình gợi ý — {len(L)} buổi</h3><div class="roadmap">{_road}</div>
"""

COURSE = dict(
    slug="arduino-esp32", title="Lập trình nhúng với Arduino & ESP32", short_title="Arduino & ESP32", icon="🔌",
    badge=f"{len(L)} bài · 14 sketch", tagline="LED, nút nhấn, cảm biến, PWM, servo, động cơ, Serial, ngắt, I2C, WiFi, web server, MQTT — từ Blink tới nhà thông minh IoT.",
    stats=[("bài học", str(len(L))), ("sketch mẫu", "14"), ("dự án IoT", "1")],
    header_sub=f"Khóa học: 🔌 Lập trình nhúng với Arduino &amp; ESP32 · {len(L)} buổi",
    gradient=["#155e75", "#0d9488", "#65a30d"], storage="ard", overview=OVERVIEW, groups=GROUPS, code_dir=CODE, runner=run,
)

if __name__ == "__main__":
    coursekit.build(COURSE, os.path.abspath(os.path.join(HERE, "..", "..", "training", "arduino-esp32.html")))
