public class BridgeDemo {
    public static void main(String[] args) {
        // 2 loại điều khiển × 2 loại thiết bị = 4 tổ hợp, nhưng chỉ cần 2 + 2 = 4 lớp.
        // Nếu dùng kế thừa thuần: BasicRemoteTv, BasicRemoteRadio, AdvancedRemoteTv, ... (bùng nổ lớp)
        Device tv = new Tv();
        RemoteControl basic = new RemoteControl(tv);
        basic.togglePower();
        basic.volumeUp();
        tv.printStatus();

        System.out.println("-----");
        Device radio = new Radio();
        AdvancedRemote advanced = new AdvancedRemote(radio);
        advanced.togglePower();
        advanced.volumeUp();
        advanced.mute();
        radio.printStatus();
    }
}

// ===== Implementor: phía "thực thi" =====
interface Device {
    boolean isEnabled();
    void enable();
    void disable();
    int getVolume();
    void setVolume(int percent);
    void printStatus();
}

// ===== Concrete Implementors =====
abstract class BaseDevice implements Device {
    private boolean on = false;
    private int volume = 30;
    public boolean isEnabled()       { return on; }
    public void enable()             { on = true; }
    public void disable()            { on = false; }
    public int getVolume()           { return volume; }
    public void setVolume(int p)     { volume = Math.max(0, Math.min(100, p)); }
    public void printStatus() {
        System.out.println("  " + getClass().getSimpleName() + ": " + (on ? "BẬT" : "TẮT") + ", âm lượng " + volume + "%");
    }
}
class Tv extends BaseDevice { }
class Radio extends BaseDevice { }

// ===== Abstraction: phía "điều khiển", giữ tham chiếu tới Implementor (cây cầu) =====
class RemoteControl {
    protected final Device device;
    RemoteControl(Device device) { this.device = device; }

    void togglePower() {
        if (device.isEnabled()) device.disable(); else device.enable();
        System.out.println("Nút nguồn -> " + (device.isEnabled() ? "bật" : "tắt"));
    }
    void volumeUp()   { device.setVolume(device.getVolume() + 10); System.out.println("Tăng âm lượng"); }
    void volumeDown() { device.setVolume(device.getVolume() - 10); System.out.println("Giảm âm lượng"); }
}

// ===== Refined Abstraction: mở rộng phía điều khiển mà không đụng tới thiết bị =====
class AdvancedRemote extends RemoteControl {
    AdvancedRemote(Device device) { super(device); }
    void mute() { device.setVolume(0); System.out.println("Tắt tiếng (mute)"); }
}
