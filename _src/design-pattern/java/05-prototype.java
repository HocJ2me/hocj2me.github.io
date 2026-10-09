import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PrototypeDemo {
    public static void main(String[] args) {
        // 1. Tạo "bản mẫu" một lần (giả sử việc tạo rất tốn kém: đọc file, query DB...)
        ExamPaper template = new ExamPaper("Đề kiểm tra Java – 45 phút");
        template.addQuestion("Singleton là gì?");
        template.addQuestion("Phân biệt Factory Method và Abstract Factory.");

        // 2. Clone ra các đề con rồi chỉnh riêng từng đề
        ExamPaper deA = template.clone();
        deA.setCode("Mã đề 101");
        deA.addQuestion("Viết Builder cho lớp Student.");

        ExamPaper deB = template.clone();
        deB.setCode("Mã đề 102");
        deB.addQuestion("Vẽ UML của Prototype.");

        System.out.println(template);
        System.out.println(deA);
        System.out.println(deB);
        System.out.println("deA.questions == template.questions ? " + deA.sameQuestionsAs(template));

        // 3. Prototype Registry: lưu sẵn các bản mẫu, cần thì clone theo tên
        ShapeRegistry registry = new ShapeRegistry();
        Shape c1 = registry.get("red-circle");
        Shape c2 = registry.get("red-circle");
        c2.move(50, 50);
        System.out.println(c1 + "  |  " + c2 + "  |  cùng đối tượng? " + (c1 == c2));
    }
}

/** Prototype interface của Java chính là Cloneable + clone(). Ở đây tự định nghĩa cho rõ. */
interface Prototype<T> { T clone(); }

class ExamPaper implements Prototype<ExamPaper> {
    private final String title;
    private String code = "Đề gốc";
    private List<String> questions = new ArrayList<>();

    ExamPaper(String title) { this.title = title; }

    /** Copy constructor dùng cho clone – sao chép SÂU (deep copy) danh sách câu hỏi. */
    private ExamPaper(ExamPaper src) {
        this.title = src.title;
        this.code = src.code;
        this.questions = new ArrayList<>(src.questions); // nếu gán thẳng src.questions => shallow copy, các đề sẽ dùng chung list!
    }

    @Override public ExamPaper clone() { return new ExamPaper(this); }

    void setCode(String code)    { this.code = code; }
    void addQuestion(String q)   { questions.add(q); }
    boolean sameQuestionsAs(ExamPaper o) { return this.questions == o.questions; }

    @Override public String toString() {
        return code + " (" + title + "): " + questions.size() + " câu " + questions;
    }
}

abstract class Shape implements Prototype<Shape> {
    protected int x, y;
    protected String color;
    void move(int dx, int dy) { x += dx; y += dy; }
    @Override public abstract Shape clone();   // ghi đè Object.clone() (protected) thành public
}

class Circle extends Shape {
    int radius;
    Circle(int radius, String color) { this.radius = radius; this.color = color; }
    private Circle(Circle s) { this.x = s.x; this.y = s.y; this.color = s.color; this.radius = s.radius; }
    @Override public Circle clone() { return new Circle(this); }
    @Override public String toString() { return "Circle(r=" + radius + ", " + color + ", @" + x + "," + y + ")"; }
}

class ShapeRegistry {
    private final Map<String, Shape> prototypes = new HashMap<>();
    ShapeRegistry() {
        prototypes.put("red-circle", new Circle(10, "đỏ"));
        prototypes.put("big-blue-circle", new Circle(40, "xanh"));
    }
    Shape get(String key) { return prototypes.get(key).clone(); } // luôn trả về BẢN SAO
}
