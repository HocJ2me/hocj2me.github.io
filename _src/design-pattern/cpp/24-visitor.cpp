// Visitor – C++17. Bản cổ điển dùng double dispatch; cuối file có bản hiện đại
// dùng std::variant + std::visit (C++17) – không cần hàm ảo hay cấp phát động.
#include <cmath>
#include <cstdio>
#include <memory>
#include <string>
#include <variant>
#include <vector>

constexpr double PI = 3.14159265358979323846;   // M_PI không thuộc chuẩn C++

struct Circle; struct Rectangle; struct Triangle;

// ===== Visitor =====
class ShapeVisitor {
public:
    virtual ~ShapeVisitor() = default;
    virtual void visit(const Circle& c) = 0;
    virtual void visit(const Rectangle& r) = 0;
    virtual void visit(const Triangle& t) = 0;
};

// ===== Element =====
struct Shape {
    virtual ~Shape() = default;
    virtual void accept(ShapeVisitor& v) const = 0;
};

// ===== Concrete Elements – double dispatch =====
struct Circle : Shape {
    double r;
    explicit Circle(double r) : r(r) {}
    void accept(ShapeVisitor& v) const override { v.visit(*this); }
};
struct Rectangle : Shape {
    double w, h;
    Rectangle(double w, double h) : w(w), h(h) {}
    void accept(ShapeVisitor& v) const override { v.visit(*this); }
};
struct Triangle : Shape {
    double base, height;
    Triangle(double b, double h) : base(b), height(h) {}
    void accept(ShapeVisitor& v) const override { v.visit(*this); }
};

// ===== Concrete Visitors =====
class AreaVisitor : public ShapeVisitor {
public:
    void visit(const Circle& c) override    { add("Hình tròn", PI * c.r * c.r); }
    void visit(const Rectangle& r) override { add("Chữ nhật", r.w * r.h); }
    void visit(const Triangle& t) override  { add("Tam giác", t.base * t.height / 2); }
    double total() const { return total_; }
private:
    void add(const char* n, double a) { std::printf("  %6.2f  <- %s\n", a, n); total_ += a; }
    double total_ = 0;
};

class JsonExportVisitor : public ShapeVisitor {
public:
    void visit(const Circle& c) override    { items_.push_back("{\"type\":\"circle\",\"r\":" + num(c.r) + "}"); }
    void visit(const Rectangle& r) override { items_.push_back("{\"type\":\"rect\",\"w\":" + num(r.w) + ",\"h\":" + num(r.h) + "}"); }
    void visit(const Triangle& t) override  { items_.push_back("{\"type\":\"triangle\",\"base\":" + num(t.base) + ",\"height\":" + num(t.height) + "}"); }
    std::string result() const {
        std::string s = "[\n";
        for (size_t i = 0; i < items_.size(); ++i) s += "  " + items_[i] + (i + 1 < items_.size() ? ",\n" : "\n");
        return s + "]";
    }
private:
    static std::string num(double d) { char b[32]; std::snprintf(b, sizeof b, "%g", d); return b; }
    std::vector<std::string> items_;
};

// ===== Bản hiện đại: std::variant + std::visit =====
struct CircleV { double r; };
struct RectV   { double w, h; };
using ShapeV = std::variant<CircleV, RectV>;
template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };
template <class... Ts> overloaded(Ts...) -> overloaded<Ts...>;

int main() {
    std::vector<std::unique_ptr<Shape>> drawing;
    drawing.push_back(std::make_unique<Circle>(2));
    drawing.push_back(std::make_unique<Rectangle>(3, 4));
    drawing.push_back(std::make_unique<Triangle>(6, 5));

    AreaVisitor area;
    for (const auto& s : drawing) s->accept(area);
    std::printf("Tổng diện tích: %.2f\n", area.total());

    std::printf("-- Xuất JSON --\n");
    JsonExportVisitor json;
    for (const auto& s : drawing) s->accept(json);
    std::printf("%s\n", json.result().c_str());

    std::printf("-- std::variant + std::visit --\n");
    ShapeV shapes[] = { CircleV{2}, RectV{3, 4} };      // không heap, không hàm ảo
    for (const ShapeV& s : shapes)
        std::visit(overloaded{
            [](const CircleV& c) { std::printf("  tròn  %.2f\n", PI * c.r * c.r); },
            [](const RectV& r)   { std::printf("  chữ nhật %.2f\n", r.w * r.h); },
        }, s);
}
