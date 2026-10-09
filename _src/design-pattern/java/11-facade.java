public class FacadeDemo {
    public static void main(String[] args) {
        // Không có Facade: client phải tự gọi đúng thứ tự 6–7 hệ thống con.
        // Có Facade: chỉ 1 dòng lệnh.
        SmartHomeFacade home = new SmartHomeFacade(
                new Lights(), new AirConditioner(), new Curtains(), new Projector(), new SoundSystem());

        home.startMovieMode("Big Hero 6");
        System.out.println("-----");
        home.leaveHome();
    }
}

// ===== Các hệ thống con (subsystems) – mỗi lớp có API riêng, chi tiết =====
class Lights {
    void dim(int percent) { System.out.println("  💡 Đèn giảm còn " + percent + "%"); }
    void off()            { System.out.println("  💡 Tắt đèn"); }
}
class AirConditioner {
    void setTemperature(int c) { System.out.println("  ❄️  Điều hoà đặt " + c + "°C"); }
    void off()                 { System.out.println("  ❄️  Tắt điều hoà"); }
}
class Curtains {
    void close() { System.out.println("  🪟 Kéo rèm"); }
}
class Projector {
    void on()                 { System.out.println("  📽️  Bật máy chiếu"); }
    void setInput(String src) { System.out.println("  📽️  Chọn nguồn " + src); }
    void off()                { System.out.println("  📽️  Tắt máy chiếu"); }
}
class SoundSystem {
    void on()               { System.out.println("  🔊 Bật loa"); }
    void setVolume(int v)   { System.out.println("  🔊 Âm lượng " + v); }
    void off()              { System.out.println("  🔊 Tắt loa"); }
}

// ===== Facade – một giao diện đơn giản che giấu sự phức tạp phía sau =====
class SmartHomeFacade {
    private final Lights lights;
    private final AirConditioner ac;
    private final Curtains curtains;
    private final Projector projector;
    private final SoundSystem sound;

    SmartHomeFacade(Lights l, AirConditioner a, Curtains c, Projector p, SoundSystem s) {
        this.lights = l; this.ac = a; this.curtains = c; this.projector = p; this.sound = s;
    }

    void startMovieMode(String movie) {
        System.out.println("🎬 Chế độ xem phim: " + movie);
        curtains.close();
        lights.dim(10);
        ac.setTemperature(26);
        projector.on();
        projector.setInput("HDMI-1");
        sound.on();
        sound.setVolume(40);
    }

    void leaveHome() {
        System.out.println("🚪 Chế độ ra khỏi nhà");
        projector.off();
        sound.off();
        ac.off();
        lights.off();
    }
}
