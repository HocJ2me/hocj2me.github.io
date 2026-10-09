import java.util.ArrayDeque;
import java.util.Deque;

public class MementoDemo {
    public static void main(String[] args) {
        Editor editor = new Editor();
        History history = new History(editor);

        history.backup();
        editor.type("Design Pattern");
        history.backup();
        editor.type(" là các giải pháp");
        editor.setFontSize(16);
        history.backup();
        editor.type(" ĐÃ VIẾT NHẦM!!!");
        editor.setFontSize(40);
        System.out.println("Hiện tại : " + editor);

        history.undo();
        System.out.println("Undo 1   : " + editor);
        history.undo();
        System.out.println("Undo 2   : " + editor);
        history.undo();
        System.out.println("Undo 3   : " + editor);
    }
}

/** Originator – đối tượng có trạng thái cần lưu/khôi phục. */
class Editor {
    private String content = "";
    private int fontSize = 12;

    void type(String text)      { content += text; }
    void setFontSize(int size)  { fontSize = size; }

    /** Tạo memento chứa ảnh chụp trạng thái hiện tại. */
    Memento save() { return new Memento(content, fontSize); }

    /** Khôi phục trạng thái từ memento. */
    void restore(Memento m) {
        this.content = m.content();
        this.fontSize = m.fontSize();
    }

    @Override public String toString() { return "\"" + content + "\" [cỡ chữ " + fontSize + "]"; }

    /**
     * Memento – bất biến (record). Được khai báo lồng trong Editor và các field
     * chỉ đọc, nên Caretaker giữ nó nhưng không thể thay đổi nội dung bên trong.
     */
    record Memento(String content, int fontSize) { }
}

/** Caretaker – chỉ lưu giữ memento, không đọc/sửa nội dung của nó. */
class History {
    private final Editor editor;
    private final Deque<Editor.Memento> stack = new ArrayDeque<>();
    History(Editor editor) { this.editor = editor; }

    void backup() { stack.push(editor.save()); }

    void undo() {
        if (stack.isEmpty()) return;
        editor.restore(stack.pop());
    }
}
