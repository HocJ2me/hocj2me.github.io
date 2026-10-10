# -*- coding: utf-8 -*-
"""Hình minh hoạ cho khóa Arduino & ESP32."""
from svg import svg, box, text, arrow, path


def board_compare():
    rows = [("Vi xử lý", "ATmega328P 8 bit, 16 MHz", "Xtensa LX6 32 bit, 2 nhân, 240 MHz"), ("Bộ nhớ", "32 KB Flash, 2 KB RAM", "4 MB Flash, 520 KB RAM"),
            ("Điện áp chân", "5 V", "3.3 V (KHÔNG chịu 5 V)"), ("ADC", "6 kênh, 10 bit (0–1023)", "18 kênh, 12 bit (0–4095)"),
            ("PWM", "6 chân (~)", "hầu hết GPIO (bộ LEDC)"), ("Kết nối", "—", "WiFi + Bluetooth"), ("Giá tham khảo", "~120 nghìn", "~100 nghìn")]
    b = [box(10, 10, 170, 30, "bx-g", rx=4, text="", tcls="s"), box(180, 10, 250, 30, "bx-a", rx=4, text="Arduino Uno R3", tcls="t"),
         box(430, 10, 270, 30, "bx-d", rx=4, text="ESP32 DevKit V1", tcls="t")]
    for i, (k, u, e) in enumerate(rows):
        y = 40 + i * 28
        b.append(f'<rect x="10" y="{y}" width="690" height="28" fill="{"#f8fafc" if i % 2 else "#fff"}" stroke="#e2e8f0"/>')
        b.append(text(20, y + 19, k, "s"))
        b.append(text(190, y + 19, u, "xs"))
        b.append(text(440, y + 19, e, "xs"))
    return svg(710, 40 + len(rows) * 28 + 10, "".join(b), "So sánh Arduino Uno và ESP32")


def led_circuit():
    b = [box(20, 40, 110, 120, "bx-a", rx=6, text="Arduino", sub="chân 4", tcls="t")]
    b.append('<polyline class="ln" points="130,70 200,70"/>')
    b.append('<rect x="200" y="60" width="70" height="20" fill="#fef3c7" stroke="#b45309"/>')
    b.append(text(235, 52, "R = 220 Ω", "xs", "middle"))
    b.append('<polyline class="ln" points="270,70 330,70"/>')
    b.append('<polygon points="330,55 330,85 360,70" fill="#fecaca" stroke="#dc2626" stroke-width="1.5"/><line x1="360" y1="55" x2="360" y2="85" stroke="#dc2626" stroke-width="2"/>')
    b.append(text(345, 104, "LED", "xs", "middle"))
    b.append('<polyline class="ln" points="360,70 420,70 420,140 130,140"/>')
    b.append(text(160, 134, "GND", "xs"))
    b.append(text(450, 60, "R = (Vnguồn − V_LED) / I", "mono"))
    b.append(text(450, 84, "  = (5 − 2) / 0.015 ≈ 200 Ω → chọn 220 Ω", "mono"))
    b.append(text(450, 108, "ESP32: (3.3 − 2) / 0.01 ≈ 130 Ω → 150 Ω", "mono"))
    b.append(text(450, 136, "Chân dài (+) của LED về phía chân tín hiệu.", "xs mute"))
    return svg(760, 170, "".join(b), "Mạch LED")


def pullup():
    b = [text(10, 18, "Nút nhấn với điện trở kéo lên TRONG chip (INPUT_PULLUP)", "s")]
    b.append(box(260, 40, 160, 130, "bx-a", rx=6))
    b.append(text(340, 60, "Vi điều khiển", "s", "middle"))
    b.append('<polyline class="ln" points="300,74 300,96"/><rect x="292" y="96" width="16" height="34" fill="#fef3c7" stroke="#b45309"/><polyline class="ln" points="300,130 300,150 260,150"/>')
    b.append(text(316, 116, "~40 kΩ", "xs"))
    b.append(text(296, 70, "VCC", "xs", "end"))
    b.append('<polyline class="ln" points="260,150 160,150"/>')
    b.append('<line class="ln" x1="160" y1="150" x2="130" y2="132"/><polyline class="ln" points="120,150 60,150 60,170"/>')
    b.append(text(140, 124, "nút", "xs", "middle"))
    b.append('<line class="ln" x1="45" y1="170" x2="75" y2="170"/><line class="ln" x1="52" y1="176" x2="68" y2="176"/>')
    b.append(text(60, 194, "GND", "xs", "middle"))
    b.append(text(440, 100, "Không nhấn: chân bị kéo lên → HIGH", "s"))
    b.append(text(440, 124, "Nhấn: chân nối GND → LOW", "s"))
    b.append(text(440, 148, "Không có điện trở kéo: chân “thả nổi”,", "xs mute"))
    b.append(text(440, 164, "đọc ngẫu nhiên do nhiễu.", "xs mute"))
    return svg(720, 206, "".join(b), "Nút nhấn và điện trở kéo lên")


def bounce():
    b = [text(10, 18, "Dội phím: khi nhấn, tiếp điểm kim loại nảy nhiều lần trong vài ms", "s")]
    pts = "20,50 120,50 120,110 128,110 128,50 134,50 134,110 141,110 141,58 146,58 146,110 420,110 420,50 560,50"
    b.append(f'<polyline points="{pts}" fill="none" stroke="#2563eb" stroke-width="2.5"/>')
    b.append(text(20, 42, "HIGH", "xs mute"))
    b.append(text(20, 128, "LOW", "xs mute"))
    b.append('<rect x="118" y="36" width="34" height="88" fill="#dc2626" opacity="0.12"/>')
    b.append(text(135, 146, "nảy ~5–10 ms", "xs", "middle"))
    b.append(text(280, 146, "chỉ tin trạng thái khi giữ ổn định > 30 ms", "xs", "middle"))
    return svg(580, 156, "".join(b), "Dội phím")


def ldr_divider():
    b = [text(10, 18, "Cầu phân áp đọc quang trở (LDR)", "s")]
    b.append('<polyline class="ln" points="80,40 80,60"/>')
    b.append(text(80, 36, "3.3 V", "xs", "middle"))
    b.append('<rect x="70" y="60" width="20" height="50" fill="#fef3c7" stroke="#b45309"/>')
    b.append(text(98, 90, "LDR", "xs"))
    b.append('<polyline class="ln" points="80,110 80,130 200,130"/>')
    b.append(box(200, 116, 110, 28, "bx-a", rx=4, text="ADC (chân 34)", tcls="xs"))
    b.append('<polyline class="ln" points="80,130 80,150"/><rect x="70" y="150" width="20" height="50" fill="#e2e8f0" stroke="#475569"/>')
    b.append(text(98, 180, "10 kΩ", "xs"))
    b.append('<polyline class="ln" points="80,200 80,220"/><line class="ln" x1="65" y1="220" x2="95" y2="220"/>')
    b.append(text(340, 70, "Vout = 3.3 · R10k / (R_LDR + R10k)", "mono"))
    b.append(text(340, 96, "Sáng: R_LDR ≈ 1 kΩ  → Vout ≈ 3.0 V → ADC ≈ 3700", "xs"))
    b.append(text(340, 116, "Tối  : R_LDR ≈ 50 kΩ → Vout ≈ 0.55 V → ADC ≈ 680", "xs"))
    b.append(text(340, 146, "ADC 12 bit: giá trị = Vout / 3.3 × 4095", "xs mute"))
    return svg(720, 232, "".join(b), "Cầu phân áp LDR")


def pwm_waves():
    b = []
    for i, d in enumerate([0.25, 0.5, 0.75]):
        y = 20 + i * 52
        b.append(text(10, y + 26, f"duty {int(d * 100)}% → analogWrite {int(d * 255)}", "xs"))
        x = 190
        pts = []
        for k in range(4):
            x0 = x + k * 100
            pts += [f"{x0},{y + 36}", f"{x0},{y + 6}", f"{x0 + 100 * d},{y + 6}", f"{x0 + 100 * d},{y + 36}", f"{x0 + 100},{y + 36}"]
        b.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#2563eb" stroke-width="2"/>')
        b.append(text(600, y + 26, ["LED mờ", "LED vừa", "LED sáng"][i], "xs mute"))
    b.append(text(190, 180, "Chân chỉ bật/tắt rất nhanh (~500 Hz – 20 kHz); mắt và động cơ “cảm nhận” giá trị trung bình.", "xs mute"))
    return svg(680, 190, "".join(b), "Dạng sóng PWM")


def ultrasonic():
    b = [box(20, 50, 120, 70, "bx-a", rx=6, text="HC-SR04", sub="TRIG  ECHO", tcls="t")]
    b.append('<rect x="460" y="30" width="20" height="110" fill="#94a3b8"/>')
    b.append(text(470, 160, "vật cản", "xs", "middle"))
    for k in range(3):
        b.append(f'<path d="M{160 + k * 40},65 q10,20 0,40" fill="none" stroke="#2563eb" stroke-width="2"/>')
        b.append(f'<path d="M{420 - k * 40},75 q-10,20 0,40" fill="none" stroke="#d97706" stroke-width="2"/>')
    b.append(text(250, 46, "sóng siêu âm 40 kHz đi →", "xs", "middle"))
    b.append(text(330, 140, "← tiếng vọng trở về", "xs", "middle"))
    b.append(text(20, 188, "khoảng cách (cm) = thời gian ECHO (µs) × 0.0343 / 2      (âm thanh 343 m/s, chia 2 vì đi + về)", "mono"))
    return svg(640, 200, "".join(b), "Cảm biến siêu âm")


def i2c_bus():
    b = [box(20, 60, 120, 60, "bx-a", rx=6, text="ESP32", sub="master", tcls="t")]
    b.append('<line x1="140" y1="74" x2="640" y2="74" stroke="#2563eb" stroke-width="2.5"/><line x1="140" y1="104" x2="640" y2="104" stroke="#d97706" stroke-width="2.5"/>')
    b.append(text(150, 68, "SDA (dữ liệu) – GPIO 21", "xs"))
    b.append(text(150, 120, "SCL (xung nhịp) – GPIO 22", "xs"))
    for i, (n, a) in enumerate([("LCD 16x2", "0x27"), ("BME280", "0x76"), ("OLED", "0x3C"), ("RTC DS3231", "0x68")]):
        x = 250 + i * 100
        b.append(f'<line class="ln thin" x1="{x + 40}" y1="74" x2="{x + 40}" y2="140"/><line class="ln thin" x1="{x + 50}" y1="104" x2="{x + 50}" y2="140"/>')
        b.append(box(x, 140, 90, 44, "bx-c", rx=6, text=n, sub=a, tcls="xs"))
    b.append(text(20, 210, "Chỉ 2 dây cho nhiều thiết bị; mỗi thiết bị có một ĐỊA CHỈ riêng. Cần điện trở kéo lên 4.7 kΩ (module thường có sẵn).", "xs mute"))
    return svg(680, 220, "".join(b), "Bus I2C")


def web_server():
    b = [box(20, 50, 140, 70, "bx-g", rx=8, text="📱 Điện thoại", sub="trình duyệt", tcls="t"),
         box(270, 40, 160, 90, "bx-d", rx=8, text="Router WiFi", sub="192.168.1.1", tcls="t"),
         box(540, 40, 160, 90, "bx-a", rx=8, text="ESP32", sub="WebServer cổng 80 · 192.168.1.25", tcls="t")]
    b.append(arrow(160, 70, 268, 70, label="GET /den?bat=1"))
    b.append(arrow(430, 70, 538, 70))
    b.append(arrow(538, 105, 432, 105))
    b.append(arrow(268, 105, 162, 105, label="200 OK “Đèn đã BẬT”", ly=124))
    b.append(text(20, 160, "Điện thoại và ESP32 phải cùng mạng WiFi. Mỗi đường dẫn (/, /den, /nhiet-do) được gắn với một hàm xử lý bằng server.on().", "xs mute"))
    return svg(720, 170, "".join(b), "ESP32 web server")


def mqtt():
    b = [box(260, 60, 180, 70, "bx-c", rx=8, text="MQTT Broker", sub="broker.hivemq.com", tcls="t")]
    b.append(box(20, 30, 170, 56, "bx-a", rx=8, text="ESP32 nhà 1", sub="publish nha/cam-bien", tcls="s"))
    b.append(box(20, 110, 170, 56, "bx-a", rx=8, text="ESP32 vườn", sub="publish vuon/do-am", tcls="s"))
    b.append(box(510, 30, 180, 56, "bx-d", rx=8, text="📱 App điện thoại", sub="subscribe nha/#", tcls="s"))
    b.append(box(510, 110, 180, 56, "bx-d", rx=8, text="Node-RED / Dashboard", sub="subscribe #", tcls="s"))
    b.append(arrow(190, 58, 258, 84))
    b.append(arrow(190, 138, 258, 110))
    b.append(arrow(440, 84, 508, 58))
    b.append(arrow(440, 110, 508, 138))
    b.append(path("M600,30 C600,0 350,0 350,58", "ln dash"))
    b.append(text(470, 12, "app publish nha/dieu-khien → ESP32 subscribe", "xs mute", "middle"))
    b.append(text(20, 196, "Publish/Subscribe: thiết bị không cần biết nhau, chỉ cần biết TÊN TOPIC. Broker chuyển tin tới mọi nơi đã đăng ký.", "xs mute"))
    return svg(710, 206, "".join(b), "Mô hình MQTT")


def sketch_structure():
    b = [box(20, 20, 220, 50, "bx-g", rx=8, text="Cấp điện / nhấn RESET", tcls="s")]
    b.append(arrow(130, 70, 130, 94))
    b.append(box(20, 96, 220, 50, "bx-a", rx=8, text="setup()", sub="chạy 1 lần: pinMode, Serial.begin", tcls="t"))
    b.append(arrow(130, 146, 130, 170))
    b.append(box(20, 172, 220, 50, "bx-b", rx=8, text="loop()", sub="lặp mãi mãi", tcls="t"))
    b.append(path("M240,197 C300,197 300,150 300,150 C300,240 130,250 130,224", "ln"))
    b.append(text(310, 200, "quay lại đầu loop()", "xs mute"))
    b.append(text(380, 60, "Arduino IDE: Tools → Board → chọn đúng board", "xs"))
    b.append(text(380, 82, "Tools → Port → chọn cổng COM của board", "xs"))
    b.append(text(380, 104, "Upload (→): biên dịch + nạp vào Flash", "xs"))
    b.append(text(380, 126, "Serial Monitor: xem dữ liệu Serial.print", "xs"))
    b.append(text(380, 148, "ESP32: thêm board qua Boards Manager", "xs"))
    return svg(720, 240, "".join(b), "Cấu trúc chương trình Arduino")
