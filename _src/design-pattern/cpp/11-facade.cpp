// Facade – C++17. Trong firmware: các hàm như digitalWrite(), WiFi.begin()
// chính là facade che giấu hàng chục thao tác thanh ghi phía dưới.
#include <iostream>
#include <string>

// ===== Subsystems – mỗi lớp điều khiển một khối phần cứng =====
class Lights {
public:
    void dim(int p) { std::cout << "  💡 Đèn giảm còn " << p << "% (PWM)\n"; }
    void off()      { std::cout << "  💡 Tắt đèn\n"; }
};
class AirConditioner {
public:
    void setTemperature(int c) { std::cout << "  ❄️  Điều hoà đặt " << c << "°C (gửi mã IR)\n"; }
    void off()                 { std::cout << "  ❄️  Tắt điều hoà\n"; }
};
class Curtains {
public:
    void close() { std::cout << "  🪟 Kéo rèm (động cơ bước)\n"; }
};
class Projector {
public:
    void on()                          { std::cout << "  📽️  Bật máy chiếu\n"; }
    void setInput(const std::string& s){ std::cout << "  📽️  Chọn nguồn " << s << "\n"; }
    void off()                         { std::cout << "  📽️  Tắt máy chiếu\n"; }
};
class SoundSystem {
public:
    void on()             { std::cout << "  🔊 Bật loa\n"; }
    void setVolume(int v) { std::cout << "  🔊 Âm lượng " << v << "\n"; }
    void off()            { std::cout << "  🔊 Tắt loa\n"; }
};

// ===== Facade =====
class SmartHomeFacade {
public:
    SmartHomeFacade(Lights& l, AirConditioner& a, Curtains& c, Projector& p, SoundSystem& s)
        : lights_(l), ac_(a), curtains_(c), projector_(p), sound_(s) {}

    void startMovieMode(const std::string& movie) {
        std::cout << "🎬 Chế độ xem phim: " << movie << "\n";
        curtains_.close();
        lights_.dim(10);
        ac_.setTemperature(26);
        projector_.on();
        projector_.setInput("HDMI-1");
        sound_.on();
        sound_.setVolume(40);
    }

    void leaveHome() {
        std::cout << "🚪 Chế độ ra khỏi nhà\n";
        projector_.off();
        sound_.off();
        ac_.off();
        lights_.off();
    }
private:
    Lights& lights_;
    AirConditioner& ac_;
    Curtains& curtains_;
    Projector& projector_;
    SoundSystem& sound_;
};

int main() {
    // Các đối tượng phần cứng tạo tĩnh một lần (thường là biến toàn cục trong sketch Arduino)
    Lights lights; AirConditioner ac; Curtains curtains; Projector projector; SoundSystem sound;
    SmartHomeFacade home(lights, ac, curtains, projector, sound);

    home.startMovieMode("Big Hero 6");
    std::cout << "-----\n";
    home.leaveHome();
}
