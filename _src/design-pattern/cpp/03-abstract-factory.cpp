// Abstract Factory – C++17
// (Trong firmware, ý tưởng tương tự: một factory cho màn hình OLED, một factory cho LCD.)
// Ở đây: mỗi "họ" giao diện Light/Dark gồm Button + Checkbox cùng phong cách.
#include <iostream>
#include <memory>

// ===== Abstract Products =====
class Button   { public: virtual ~Button() = default;   virtual void paint() const = 0; };
class Checkbox { public: virtual ~Checkbox() = default; virtual void paint() const = 0; };

// ===== Họ Light =====
class LightButton : public Button {
public: void paint() const override { std::cout << "[ Nút nền trắng, chữ đen ]\n"; }
};
class LightCheckbox : public Checkbox {
public: void paint() const override { std::cout << "[x] Checkbox viền xám nhạt\n"; }
};

// ===== Họ Dark =====
class DarkButton : public Button {
public: void paint() const override { std::cout << "[ Nút nền đen, chữ trắng ]\n"; }
};
class DarkCheckbox : public Checkbox {
public: void paint() const override { std::cout << "[x] Checkbox viền trắng phát sáng\n"; }
};

// ===== Abstract Factory =====
class UIFactory {
public:
    virtual ~UIFactory() = default;
    virtual std::unique_ptr<Button>   createButton() const = 0;
    virtual std::unique_ptr<Checkbox> createCheckbox() const = 0;
};

// ===== Concrete Factories =====
class LightThemeFactory : public UIFactory {
public:
    std::unique_ptr<Button>   createButton() const override   { return std::make_unique<LightButton>(); }
    std::unique_ptr<Checkbox> createCheckbox() const override { return std::make_unique<LightCheckbox>(); }
};
class DarkThemeFactory : public UIFactory {
public:
    std::unique_ptr<Button>   createButton() const override   { return std::make_unique<DarkButton>(); }
    std::unique_ptr<Checkbox> createCheckbox() const override { return std::make_unique<DarkCheckbox>(); }
};

// Client – chỉ biết interface
void render(const UIFactory& factory) {
    auto button = factory.createButton();
    auto checkbox = factory.createCheckbox();
    button->paint();
    checkbox->paint();
}

int main() {
    // Thực tế: chọn factory theo chân cấu hình phần cứng hoặc macro lúc biên dịch
    LightThemeFactory light;
    DarkThemeFactory dark;
    render(light);
    std::cout << "-----\n";
    render(dark);
}
