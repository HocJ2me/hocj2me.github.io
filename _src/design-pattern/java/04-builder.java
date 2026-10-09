import java.util.ArrayList;
import java.util.List;

public class BuilderDemo {
    public static void main(String[] args) {
        // 1. Dùng Builder trực tiếp với "fluent API" – dễ đọc, không cần nhớ thứ tự tham số
        Robot custom = new Robot.Builder("BK-01", "ESP32")
                .wheels(4)
                .addSensor("Siêu âm HC-SR04")
                .addSensor("Dò line TCRT5000")
                .battery(3000)
                .bluetooth(true)
                .build();
        System.out.println(custom);

        // 2. Dùng Director để đóng gói các "công thức" lắp ráp hay dùng
        RobotDirector director = new RobotDirector();
        System.out.println(director.makeLineFollower());
        System.out.println(director.makeSumoRobot());

        // 3. Builder kiểm tra dữ liệu trước khi tạo đối tượng
        try {
            new Robot.Builder("LOI", "Arduino Uno").wheels(3).build();
        } catch (IllegalStateException e) {
            System.out.println("Lỗi: " + e.getMessage());
        }
    }
}

/** Product – bất biến (immutable): mọi field là final, không có setter. */
final class Robot {
    private final String name;          // bắt buộc
    private final String board;         // bắt buộc
    private final int wheels;           // tuỳ chọn
    private final int batteryMah;       // tuỳ chọn
    private final boolean bluetooth;    // tuỳ chọn
    private final List<String> sensors; // tuỳ chọn

    private Robot(Builder b) {          // chỉ Builder mới gọi được
        this.name = b.name;
        this.board = b.board;
        this.wheels = b.wheels;
        this.batteryMah = b.batteryMah;
        this.bluetooth = b.bluetooth;
        this.sensors = List.copyOf(b.sensors);
    }

    @Override
    public String toString() {
        return String.format("Robot %-6s| mạch=%-12s| bánh=%d | pin=%dmAh | BT=%-5s| cảm biến=%s",
                name, board, wheels, batteryMah, bluetooth, sensors);
    }

    /** Builder – static nested class. */
    public static class Builder {
        private final String name;
        private final String board;
        private int wheels = 2;
        private int batteryMah = 1000;
        private boolean bluetooth = false;
        private final List<String> sensors = new ArrayList<>();

        public Builder(String name, String board) {      // tham số bắt buộc đưa vào constructor
            this.name = name;
            this.board = board;
        }
        public Builder wheels(int n)          { this.wheels = n; return this; }
        public Builder battery(int mAh)       { this.batteryMah = mAh; return this; }
        public Builder bluetooth(boolean on)  { this.bluetooth = on; return this; }
        public Builder addSensor(String s)    { this.sensors.add(s); return this; }

        public Robot build() {
            if (wheels != 2 && wheels != 4)
                throw new IllegalStateException("Robot chỉ hỗ trợ 2 hoặc 4 bánh, nhận được " + wheels);
            return new Robot(this);
        }
    }
}

/** Director – biết TRÌNH TỰ các bước để tạo ra những cấu hình chuẩn. */
class RobotDirector {
    Robot makeLineFollower() {
        return new Robot.Builder("LINE", "Arduino Nano")
                .addSensor("Dò line x5")
                .battery(1200)
                .build();
    }
    Robot makeSumoRobot() {
        return new Robot.Builder("SUMO", "STM32")
                .wheels(4)
                .addSensor("Hồng ngoại x4")
                .battery(2200)
                .build();
    }
}
