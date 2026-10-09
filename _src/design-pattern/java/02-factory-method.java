public class FactoryMethodDemo {
    public static void main(String[] args) {
        // Client chỉ làm việc với lớp trừu tượng NotificationService.
        // Muốn đổi kênh gửi -> đổi lớp con, không sửa logic gửi.
        NotificationService[] services = {
            new EmailService(),
            new SmsService(),
            new ZaloService()
        };
        for (NotificationService s : services) {
            s.notifyUser("Lớp Design Pattern bắt đầu lúc 19h tối nay!");
        }
    }
}

// ===== Product: giao diện chung cho mọi loại thông báo =====
interface Notification {
    void send(String message);
}

// ===== Concrete Products =====
class EmailNotification implements Notification {
    public void send(String message) { System.out.println("[EMAIL] " + message); }
}

class SmsNotification implements Notification {
    public void send(String message) {
        // SMS giới hạn độ dài -> xử lý riêng ở đây
        String text = message.length() > 30 ? message.substring(0, 30) + "..." : message;
        System.out.println("[SMS]   " + text);
    }
}

class ZaloNotification implements Notification {
    public void send(String message) { System.out.println("[ZALO]  " + message + " 👍"); }
}

// ===== Creator: chứa thuật toán chung + "factory method" trừu tượng =====
abstract class NotificationService {

    /** Factory Method – lớp con quyết định tạo đối tượng cụ thể nào. */
    protected abstract Notification createNotification();

    /** Logic nghiệp vụ dùng sản phẩm mà KHÔNG biết lớp cụ thể của nó. */
    public void notifyUser(String message) {
        Notification n = createNotification();
        System.out.print(getClass().getSimpleName() + " -> ");
        n.send(message);
    }
}

// ===== Concrete Creators =====
class EmailService extends NotificationService {
    protected Notification createNotification() { return new EmailNotification(); }
}

class SmsService extends NotificationService {
    protected Notification createNotification() { return new SmsNotification(); }
}

class ZaloService extends NotificationService {
    protected Notification createNotification() { return new ZaloNotification(); }
}
