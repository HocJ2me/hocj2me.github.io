// Memento – C++17. Trong nhúng: lưu cấu hình vào EEPROM/Flash trước khi thử
// thông số mới (PID, ngưỡng cảm biến), nếu không ổn thì khôi phục.
#include <iostream>
#include <stack>
#include <string>

// ===== Originator =====
class Editor {
public:
    // ===== Memento – chỉ Editor được đọc nội dung (friend), mọi thứ khác là private =====
    class Memento {
        friend class Editor;
        Memento(std::string c, int f) : content_(std::move(c)), fontSize_(f) {}
        std::string content_;
        int fontSize_;
    };

    void type(const std::string& text) { content_ += text; }
    void setFontSize(int size)         { fontSize_ = size; }

    Memento save() const { return Memento(content_, fontSize_); }
    void restore(const Memento& m) { content_ = m.content_; fontSize_ = m.fontSize_; }

    void print(const char* label) const {
        std::cout << label << "\"" << content_ << "\" [cỡ chữ " << fontSize_ << "]\n";
    }
private:
    std::string content_;
    int fontSize_ = 12;
};

// ===== Caretaker – giữ memento nhưng KHÔNG đọc được bên trong (biên dịch sẽ báo lỗi nếu thử) =====
class History {
public:
    explicit History(Editor& e) : editor_(e) {}
    void backup() { stack_.push(editor_.save()); }
    void undo() {
        if (stack_.empty()) return;
        editor_.restore(stack_.top());
        stack_.pop();
    }
private:
    Editor& editor_;
    std::stack<Editor::Memento> stack_;
};

int main() {
    Editor editor;
    History history(editor);

    history.backup();
    editor.type("Design Pattern");
    history.backup();
    editor.type(" là các giải pháp");
    editor.setFontSize(16);
    history.backup();
    editor.type(" ĐÃ VIẾT NHẦM!!!");
    editor.setFontSize(40);
    editor.print("Hiện tại : ");

    history.undo(); editor.print("Undo 1   : ");
    history.undo(); editor.print("Undo 2   : ");
    history.undo(); editor.print("Undo 3   : ");
}
