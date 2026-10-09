import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;

public class InterpreterDemo {
    public static void main(String[] args) {
        // Ngữ pháp (BNF) của ngôn ngữ mini – biểu thức hậu tố (Reverse Polish Notation):
        //   expression ::= number | variable | expression expression operator
        //   operator   ::= '+' | '-' | '*'
        Map<String, Integer> context = new HashMap<>();
        context.put("x", 5);
        context.put("y", 3);

        String[] programs = {
                "2 3 +",              // 2 + 3
                "x y * 4 -",          // x * y - 4
                "x 2 + y 1 - *"       // (x + 2) * (y - 1)
        };
        for (String p : programs) {
            Expression ast = Parser.parse(p);
            System.out.printf("%-16s => cây: %-22s = %d%n", p, ast, ast.interpret(context));
        }

        // Đổi ngữ cảnh -> cùng một cây cú pháp, kết quả khác
        context.put("x", 10);
        Expression ast = Parser.parse("x 2 + y 1 - *");
        System.out.println("Khi x = 10: " + ast + " = " + ast.interpret(context));
    }
}

/** AbstractExpression */
interface Expression {
    int interpret(Map<String, Integer> ctx);
}

/** TerminalExpression – số */
record NumberExpr(int value) implements Expression {
    public int interpret(Map<String, Integer> ctx) { return value; }
    public String toString() { return String.valueOf(value); }
}

/** TerminalExpression – biến, tra giá trị trong Context */
record VariableExpr(String name) implements Expression {
    public int interpret(Map<String, Integer> ctx) { return ctx.getOrDefault(name, 0); }
    public String toString() { return name; }
}

/** NonterminalExpressions – mỗi quy tắc ngữ pháp là một lớp */
record AddExpr(Expression l, Expression r) implements Expression {
    public int interpret(Map<String, Integer> ctx) { return l.interpret(ctx) + r.interpret(ctx); }
    public String toString() { return "(" + l + " + " + r + ")"; }
}
record SubtractExpr(Expression l, Expression r) implements Expression {
    public int interpret(Map<String, Integer> ctx) { return l.interpret(ctx) - r.interpret(ctx); }
    public String toString() { return "(" + l + " - " + r + ")"; }
}
record MultiplyExpr(Expression l, Expression r) implements Expression {
    public int interpret(Map<String, Integer> ctx) { return l.interpret(ctx) * r.interpret(ctx); }
    public String toString() { return "(" + l + " * " + r + ")"; }
}

/** Parser – chuyển chuỗi thành cây cú pháp (AST) bằng ngăn xếp. */
class Parser {
    static Expression parse(String source) {
        Deque<Expression> stack = new ArrayDeque<>();
        for (String token : source.trim().split("\\s+")) {
            switch (token) {
                case "+" -> { Expression r = stack.pop(), l = stack.pop(); stack.push(new AddExpr(l, r)); }
                case "-" -> { Expression r = stack.pop(), l = stack.pop(); stack.push(new SubtractExpr(l, r)); }
                case "*" -> { Expression r = stack.pop(), l = stack.pop(); stack.push(new MultiplyExpr(l, r)); }
                default  -> stack.push(token.matches("-?\\d+")
                        ? new NumberExpr(Integer.parseInt(token))
                        : new VariableExpr(token));
            }
        }
        return stack.pop();
    }
}
