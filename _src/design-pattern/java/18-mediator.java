import java.util.ArrayList;
import java.util.List;

public class MediatorDemo {
    public static void main(String[] args) {
        // Các thành viên KHÔNG giữ tham chiếu tới nhau, chỉ biết phòng chat (mediator)
        ChatRoom room = new ClassChatRoom("Lớp 10A1");

        User teacher = new Teacher("Thầy Tuyền", room);
        User an = new Student("An", room);
        User binh = new Student("Bình", room);
        User chi = new Student("Chi", room);

        an.send("Mọi người làm bài tập Builder chưa?");
        teacher.send("Hạn nộp là 20h tối nay nhé!");
        binh.sendPrivate("Chi", "Cho mình mượn vở ghi với");
        chi.send("Bài này dài quá :(");
    }
}

/** Mediator */
interface ChatRoom {
    void join(User user);
    void broadcast(String message, User from);
    void sendPrivate(String message, User from, String toName);
}

/** ConcreteMediator – chứa toàn bộ logic điều phối. */
class ClassChatRoom implements ChatRoom {
    private final String name;
    private final List<User> users = new ArrayList<>();
    ClassChatRoom(String name) { this.name = name; }

    public void join(User u) {
        users.add(u);
        System.out.println("[" + name + "] " + u.getName() + " đã tham gia");
    }

    public void broadcast(String message, User from) {
        // Quy tắc nghiệp vụ nằm ở mediator: tin của giáo viên được đánh dấu quan trọng
        String tag = (from instanceof Teacher) ? "📌 " : "";
        for (User u : users) {
            if (u != from) u.receive(tag + message, from.getName());
        }
    }

    public void sendPrivate(String message, User from, String toName) {
        users.stream()
             .filter(u -> u.getName().equals(toName))
             .findFirst()
             .ifPresent(u -> u.receive("(riêng) " + message, from.getName()));
    }
}

/** Colleague */
abstract class User {
    protected final String name;
    protected final ChatRoom room;
    User(String name, ChatRoom room) { this.name = name; this.room = room; room.join(this); }
    String getName() { return name; }

    void send(String msg) {
        System.out.println(name + " gửi: " + msg);
        room.broadcast(msg, this);
    }
    void sendPrivate(String to, String msg) {
        System.out.println(name + " nhắn riêng " + to + ": " + msg);
        room.sendPrivate(msg, this, to);
    }
    void receive(String msg, String from) {
        System.out.println("    -> " + name + " nhận từ " + from + ": " + msg);
    }
}

/** ConcreteColleagues */
class Student extends User { Student(String n, ChatRoom r) { super(n, r); } }
class Teacher extends User { Teacher(String n, ChatRoom r) { super(n, r); } }
