public class AbstractFactoryDemo {
    public static void main(String[] args) {
        // Chọn "họ" sản phẩm một lần duy nhất ở đây (có thể đọc từ cấu hình)
        render(new LightThemeFactory());
        System.out.println("-----");
        render(new DarkThemeFactory());
    }

    /** Client: chỉ biết các interface, không biết lớp cụ thể nào. */
    static void render(UIFactory factory) {
        Button button = factory.createButton();
        Checkbox checkbox = factory.createCheckbox();
        button.paint();
        checkbox.paint();
    }
}

// ===== Abstract Products =====
interface Button   { void paint(); }
interface Checkbox { void paint(); }

// ===== Concrete Products – họ Light =====
class LightButton implements Button {
    public void paint() { System.out.println("[ Nút nền trắng, chữ đen ]"); }
}
class LightCheckbox implements Checkbox {
    public void paint() { System.out.println("[x] Checkbox viền xám nhạt"); }
}

// ===== Concrete Products – họ Dark =====
class DarkButton implements Button {
    public void paint() { System.out.println("[ Nút nền đen, chữ trắng ]"); }
}
class DarkCheckbox implements Checkbox {
    public void paint() { System.out.println("[x] Checkbox viền trắng phát sáng"); }
}

// ===== Abstract Factory: tạo ra cả một HỌ sản phẩm liên quan =====
interface UIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

// ===== Concrete Factories: mỗi factory đảm bảo các sản phẩm "hợp tông" =====
class LightThemeFactory implements UIFactory {
    public Button createButton()     { return new LightButton(); }
    public Checkbox createCheckbox() { return new LightCheckbox(); }
}

class DarkThemeFactory implements UIFactory {
    public Button createButton()     { return new DarkButton(); }
    public Checkbox createCheckbox() { return new DarkCheckbox(); }
}
