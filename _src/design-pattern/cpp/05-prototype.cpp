// Prototype – C++17
#include <iostream>
#include <map>
#include <memory>
#include <string>
#include <vector>

// ===== Ví dụ 1: ExamPaper – copy constructor của C++ đã là deep copy cho std::vector =====
class ExamPaper {
public:
    explicit ExamPaper(std::string title) : title_(std::move(title)) {}
    ExamPaper clone() const { return *this; }      // gọi copy constructor mặc định
    void setCode(std::string c)    { code_ = std::move(c); }
    void addQuestion(std::string q){ questions_.push_back(std::move(q)); }
    const std::vector<std::string>* questionsPtr() const { return &questions_; }
    void print() const {
        std::cout << code_ << " (" << title_ << "): " << questions_.size() << " câu\n";
    }
private:
    std::string title_, code_ = "Đề gốc";
    std::vector<std::string> questions_;          // vector có copy constructor sao chép từng phần tử
};

// ===== Ví dụ 2: Shape – clone qua con trỏ lớp cha ("virtual constructor") =====
class Shape {
public:
    virtual ~Shape() = default;
    virtual std::unique_ptr<Shape> clone() const = 0;   // C++ không có virtual constructor -> dùng clone()
    void move(int dx, int dy) { x_ += dx; y_ += dy; }
    virtual void print() const = 0;
protected:
    int x_ = 0, y_ = 0;
    std::string color_;
};

class Circle : public Shape {
public:
    Circle(int r, std::string color) : radius_(r) { color_ = std::move(color); }
    std::unique_ptr<Shape> clone() const override { return std::make_unique<Circle>(*this); }
    void print() const override {
        std::cout << "Circle(r=" << radius_ << ", " << color_ << ", @" << x_ << "," << y_ << ")";
    }
private:
    int radius_;
};

class ShapeRegistry {
public:
    ShapeRegistry() {
        prototypes_["red-circle"] = std::make_unique<Circle>(10, "đỏ");
        prototypes_["big-blue-circle"] = std::make_unique<Circle>(40, "xanh");
    }
    std::unique_ptr<Shape> get(const std::string& key) const { return prototypes_.at(key)->clone(); }
private:
    std::map<std::string, std::unique_ptr<Shape>> prototypes_;
};

// ===== Cạm bẫy: con trỏ thô (raw pointer) -> copy mặc định là SHALLOW =====
struct SensorBuffer {
    int* data;                                     // trỏ tới mảng cấp phát động
    explicit SensorBuffer(int n) : data(new int[n]{}) {}
    // Không tự viết copy constructor => bản sao dùng CHUNG mảng data (nguy hiểm, double-free!)
};

int main() {
    ExamPaper tpl("Đề kiểm tra C++ – 45 phút");
    tpl.addQuestion("Singleton là gì?");
    tpl.addQuestion("Phân biệt Factory Method và Abstract Factory.");

    ExamPaper deA = tpl.clone();
    deA.setCode("Mã đề 101");
    deA.addQuestion("Viết Builder cho lớp Student.");
    tpl.print();
    deA.print();
    std::cout << "deA dùng chung vector với đề gốc? " << std::boolalpha
              << (deA.questionsPtr() == tpl.questionsPtr()) << "\n";

    ShapeRegistry registry;
    auto c1 = registry.get("red-circle");
    auto c2 = registry.get("red-circle");
    c2->move(50, 50);
    c1->print(); std::cout << "  |  "; c2->print();
    std::cout << "  |  cùng đối tượng? " << (c1.get() == c2.get()) << "\n";

    SensorBuffer a(4);
    SensorBuffer b = a;                            // shallow copy
    b.data[0] = 99;
    std::cout << "Shallow copy: sửa b.data[0] làm a.data[0] = " << a.data[0] << "\n";
    delete[] a.data;                               // chỉ xoá 1 lần vì dùng chung
}
