import java.util.List;

public class VisitorDemo {
    public static void main(String[] args) {
        // Cấu trúc đối tượng: bản vẽ gồm nhiều hình
        List<Shape> drawing = List.of(
                new Circle(2),
                new Rectangle(3, 4),
                new Triangle(6, 5));

        // Thêm "phép toán mới" bằng cách tạo Visitor mới – KHÔNG sửa các lớp Shape
        AreaVisitor area = new AreaVisitor();
        for (Shape s : drawing) s.accept(area);
        System.out.printf("Tổng diện tích: %.2f%n", area.getTotal());

        System.out.println("-- Xuất JSON --");
        JsonExportVisitor json = new JsonExportVisitor();
        for (Shape s : drawing) s.accept(json);
        System.out.println(json.result());
    }
}

/** Element – chỉ có duy nhất phương thức accept(visitor). */
interface Shape {
    void accept(ShapeVisitor v);
}

/** Visitor – mỗi loại Element có một phương thức visit riêng. */
interface ShapeVisitor {
    void visit(Circle c);
    void visit(Rectangle r);
    void visit(Triangle t);
}

/** ConcreteElements – double dispatch: gọi v.visit(this) để Java chọn đúng overload. */
record Circle(double r) implements Shape {
    public void accept(ShapeVisitor v) { v.visit(this); }
}
record Rectangle(double w, double h) implements Shape {
    public void accept(ShapeVisitor v) { v.visit(this); }
}
record Triangle(double base, double height) implements Shape {
    public void accept(ShapeVisitor v) { v.visit(this); }
}

/** ConcreteVisitor 1 – tính diện tích (có trạng thái tích luỹ). */
class AreaVisitor implements ShapeVisitor {
    private double total = 0;
    public void visit(Circle c) {
        double a = Math.PI * c.r() * c.r();
        System.out.printf("  Hình tròn r=%.0f      -> %.2f%n", c.r(), a);
        total += a;
    }
    public void visit(Rectangle r) {
        double a = r.w() * r.h();
        System.out.printf("  Chữ nhật %.0fx%.0f       -> %.2f%n", r.w(), r.h(), a);
        total += a;
    }
    public void visit(Triangle t) {
        double a = t.base() * t.height() / 2;
        System.out.printf("  Tam giác đáy %.0f cao %.0f -> %.2f%n", t.base(), t.height(), a);
        total += a;
    }
    double getTotal() { return total; }
}

/** ConcreteVisitor 2 – xuất JSON. */
class JsonExportVisitor implements ShapeVisitor {
    private final StringBuilder sb = new StringBuilder("[\n");
    public void visit(Circle c)    { sb.append("  {\"type\":\"circle\",\"r\":").append(c.r()).append("},\n"); }
    public void visit(Rectangle r) { sb.append("  {\"type\":\"rect\",\"w\":").append(r.w()).append(",\"h\":").append(r.h()).append("},\n"); }
    public void visit(Triangle t)  { sb.append("  {\"type\":\"triangle\",\"base\":").append(t.base()).append(",\"height\":").append(t.height()).append("},\n"); }
    String result() { return sb.substring(0, sb.length() - 2) + "\n]"; }
}
