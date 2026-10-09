import java.util.ArrayDeque;
import java.util.Deque;

public class CommandDemo {
    public static void main(String[] args) {
        // Receivers – các thiết bị thật
        Light light = new Light("phòng khách");
        Fan fan = new Fan();

        // Invoker – chiếc điều khiển không hề biết bên trong lệnh làm gì
        RemoteControl remote = new RemoteControl();

        remote.press(new LightOnCommand(light));
        remote.press(new FanSpeedCommand(fan, 3));
        remote.press(new FanSpeedCommand(fan, 1));
        remote.press(new LightOffCommand(light));

        System.out.println("--- Hoàn tác (Undo) từng bước ---");
        remote.undo();
        remote.undo();
        remote.undo();
        remote.undo();
        remote.undo(); // không còn gì để hoàn tác
    }
}

/** Command */
interface Command {
    void execute();
    void undo();
    String name();
}

// ===== Receivers =====
class Light {
    private final String room;
    Light(String room) { this.room = room; }
    void on()  { System.out.println("  💡 Bật đèn " + room); }
    void off() { System.out.println("  💡 Tắt đèn " + room); }
}
class Fan {
    private int speed = 0;
    int getSpeed()         { return speed; }
    void setSpeed(int s)   { speed = s; System.out.println("  🌀 Quạt số " + s); }
}

// ===== Concrete Commands – đóng gói "receiver + hành động + tham số" =====
class LightOnCommand implements Command {
    private final Light light;
    LightOnCommand(Light l) { light = l; }
    public void execute() { light.on(); }
    public void undo()    { light.off(); }
    public String name()  { return "Bật đèn"; }
}
class LightOffCommand implements Command {
    private final Light light;
    LightOffCommand(Light l) { light = l; }
    public void execute() { light.off(); }
    public void undo()    { light.on(); }
    public String name()  { return "Tắt đèn"; }
}
class FanSpeedCommand implements Command {
    private final Fan fan;
    private final int newSpeed;
    private int prevSpeed;                 // lưu trạng thái cũ để undo
    FanSpeedCommand(Fan f, int s) { fan = f; newSpeed = s; }
    public void execute() { prevSpeed = fan.getSpeed(); fan.setSpeed(newSpeed); }
    public void undo()    { fan.setSpeed(prevSpeed); }
    public String name()  { return "Quạt số " + newSpeed; }
}

/** Invoker – lưu lịch sử lệnh để hoàn tác. */
class RemoteControl {
    private final Deque<Command> history = new ArrayDeque<>();

    void press(Command c) {
        System.out.println("▶ " + c.name());
        c.execute();
        history.push(c);
    }
    void undo() {
        if (history.isEmpty()) { System.out.println("↩ Không còn lệnh để hoàn tác"); return; }
        Command c = history.pop();
        System.out.println("↩ Hoàn tác: " + c.name());
        c.undo();
    }
}
