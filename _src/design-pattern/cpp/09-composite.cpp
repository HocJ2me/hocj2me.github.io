// Composite – C++17
#include <iostream>
#include <memory>
#include <string>
#include <vector>

// ===== Component =====
class FileSystemItem {
public:
    virtual ~FileSystemItem() = default;
    virtual std::string getName() const = 0;
    virtual int getSize() const = 0;                       // KB
    virtual void print(const std::string& indent) const = 0;
};

// ===== Leaf =====
class FileItem : public FileSystemItem {
public:
    FileItem(std::string name, int size) : name_(std::move(name)), size_(size) {}
    std::string getName() const override { return name_; }
    int getSize() const override { return size_; }
    void print(const std::string& indent) const override {
        std::cout << indent << "📄 " << name_ << " (" << size_ << " KB)\n";
    }
private:
    std::string name_;
    int size_;
};

// ===== Composite – SỞ HỮU các con qua unique_ptr (huỷ cha sẽ tự huỷ cả cây) =====
class Folder : public FileSystemItem {
public:
    explicit Folder(std::string name) : name_(std::move(name)) {}

    // Trả về con trỏ thô (không sở hữu) để tiện thêm tiếp vào thư mục con
    template <typename T, typename... Args>
    T* add(Args&&... args) {
        auto child = std::make_unique<T>(std::forward<Args>(args)...);
        T* raw = child.get();
        children_.push_back(std::move(child));
        return raw;
    }

    std::string getName() const override { return name_; }

    int getSize() const override {                         // đệ quy
        int total = 0;
        for (const auto& c : children_) total += c->getSize();
        return total;
    }

    void print(const std::string& indent) const override {
        std::cout << indent << "📁 " << name_ << "/ (" << getSize() << " KB)\n";
        for (const auto& c : children_) c->print(indent + "   ");
    }
private:
    std::string name_;
    std::vector<std::unique_ptr<FileSystemItem>> children_;
};

int main() {
    Folder root("du-an-robot");
    Folder* src = root.add<Folder>("src");
    src->add<FileItem>("main.cpp", 12);
    src->add<FileItem>("motor.cpp", 8);
    Folder* docs = root.add<Folder>("docs");
    docs->add<FileItem>("bao-cao.pdf", 2048);
    Folder* images = docs->add<Folder>("images");
    images->add<FileItem>("so-do-mach.png", 512);
    root.add<FileItem>("README.md", 3);

    root.print("");
    std::cout << "Tổng dung lượng dự án: " << root.getSize() << " KB\n";
    std::cout << "Dung lượng thư mục docs: " << docs->getSize() << " KB\n";
}
