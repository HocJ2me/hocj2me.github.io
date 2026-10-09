// Interpreter – C++17. Ứng dụng nhúng: firmware nhận "công thức" qua Serial
// (ví dụ ngưỡng bật quạt = "x 2 + y 1 - *") mà không cần nạp lại chương trình.
#include <cctype>
#include <iostream>
#include <map>
#include <memory>
#include <sstream>
#include <stack>
#include <string>

using Context = std::map<std::string, int>;

// ===== AbstractExpression =====
class Expression {
public:
    virtual ~Expression() = default;
    virtual int interpret(const Context& ctx) const = 0;
    virtual std::string str() const = 0;
};
using ExprPtr = std::unique_ptr<Expression>;

// ===== Terminal Expressions =====
class NumberExpr : public Expression {
public:
    explicit NumberExpr(int v) : value_(v) {}
    int interpret(const Context&) const override { return value_; }
    std::string str() const override { return std::to_string(value_); }
private:
    int value_;
};
class VariableExpr : public Expression {
public:
    explicit VariableExpr(std::string n) : name_(std::move(n)) {}
    int interpret(const Context& ctx) const override {
        auto it = ctx.find(name_);
        return it == ctx.end() ? 0 : it->second;
    }
    std::string str() const override { return name_; }
private:
    std::string name_;
};

// ===== Nonterminal Expression – một lớp mẫu dùng cho cả + - * =====
template <char Op>
class BinaryExpr : public Expression {
public:
    BinaryExpr(ExprPtr l, ExprPtr r) : l_(std::move(l)), r_(std::move(r)) {}
    int interpret(const Context& ctx) const override {
        int a = l_->interpret(ctx), b = r_->interpret(ctx);
        if constexpr (Op == '+') return a + b;
        else if constexpr (Op == '-') return a - b;
        else return a * b;
    }
    std::string str() const override { return "(" + l_->str() + " " + Op + " " + r_->str() + ")"; }
private:
    ExprPtr l_, r_;
};
using AddExpr = BinaryExpr<'+'>;
using SubtractExpr = BinaryExpr<'-'>;
using MultiplyExpr = BinaryExpr<'*'>;

// ===== Parser: chuỗi hậu tố -> cây cú pháp (AST) =====
ExprPtr parse(const std::string& source) {
    std::stack<ExprPtr> st;
    std::istringstream in(source);
    std::string tok;
    auto pop = [&] { ExprPtr e = std::move(st.top()); st.pop(); return e; };
    while (in >> tok) {
        if (tok == "+" || tok == "-" || tok == "*") {
            ExprPtr r = pop(), l = pop();
            if (tok == "+")      st.push(std::make_unique<AddExpr>(std::move(l), std::move(r)));
            else if (tok == "-") st.push(std::make_unique<SubtractExpr>(std::move(l), std::move(r)));
            else                 st.push(std::make_unique<MultiplyExpr>(std::move(l), std::move(r)));
        } else if (std::isdigit(static_cast<unsigned char>(tok[0]))) {
            st.push(std::make_unique<NumberExpr>(std::stoi(tok)));
        } else {
            st.push(std::make_unique<VariableExpr>(tok));
        }
    }
    return pop();
}

int main() {
    Context ctx{ {"x", 5}, {"y", 3} };
    for (const char* p : { "2 3 +", "x y * 4 -", "x 2 + y 1 - *" }) {
        ExprPtr ast = parse(p);
        std::cout << p << "  =>  cây: " << ast->str() << " = " << ast->interpret(ctx) << "\n";
    }
    ctx["x"] = 10;                                // đổi ngữ cảnh, giữ nguyên cây
    ExprPtr ast = parse("x 2 + y 1 - *");
    std::cout << "Khi x = 10: " << ast->str() << " = " << ast->interpret(ctx) << "\n";
}
