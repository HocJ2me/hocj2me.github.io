// Flyweight – C++17. Trên MCU có vài chục KB RAM, Flyweight rất đáng giá:
// ví dụ font chữ/bitmap icon nằm 1 lần trong Flash, mỗi ký tự trên màn hình chỉ giữ (x, y, con trỏ).
#include <cstdio>
#include <map>
#include <memory>
#include <random>
#include <string>
#include <vector>

// ===== Flyweight – trạng thái NỘI TẠI, dùng chung, bất biến =====
class TreeType {
public:
    static constexpr size_t APPROX_BYTES = 2000;        // giả sử texture ~2KB
    TreeType(std::string name, std::string color) : name_(std::move(name)), color_(std::move(color)) {}
    void draw(int x, int y) const {                     // trạng thái NGOẠI TẠI truyền vào
        std::printf("  Vẽ cây %s (%s) tại (%d, %d)\n", name_.c_str(), color_.c_str(), x, y);
    }
private:
    const std::string name_, color_;
};

// ===== Flyweight Factory =====
class TreeFactory {
public:
    static const TreeType* get(const std::string& name, const std::string& color) {
        auto key = name + "|" + color;
        auto it = cache().find(key);
        if (it == cache().end())
            it = cache().emplace(key, std::make_unique<TreeType>(name, color)).first;
        return it->second.get();
    }
    static size_t count() { return cache().size(); }
private:
    static std::map<std::string, std::unique_ptr<TreeType>>& cache() {
        static std::map<std::string, std::unique_ptr<TreeType>> c;
        return c;
    }
};

// ===== Context – rất nhỏ: 2 số nguyên + 1 con trỏ =====
struct Tree {
    short x, y;                                         // tiết kiệm: short thay vì int
    const TreeType* type;                               // con trỏ tới flyweight dùng chung
    void draw() const { type->draw(x, y); }
};

int main() {
    std::vector<Tree> forest;
    forest.reserve(100000);
    std::mt19937 rng(42);                               // seed cố định -> kết quả lặp lại
    const char* kinds[][2] = { {"Phượng", "đỏ"}, {"Bàng", "xanh đậm"}, {"Thông", "xanh lá"} };

    for (int i = 0; i < 100000; ++i) {
        auto& k = kinds[rng() % 3];
        forest.push_back({ short(rng() % 1000), short(rng() % 1000), TreeFactory::get(k[0], k[1]) });
    }

    for (int i = 0; i < 3; ++i) forest[i].draw();
    std::printf("Số cây đã trồng          : %zu\n", forest.size());
    std::printf("Số TreeType thực sự tạo  : %zu\n", TreeFactory::count());
    std::printf("sizeof(Tree)             : %zu byte\n", sizeof(Tree));
    size_t without = forest.size() * (sizeof(Tree) + TreeType::APPROX_BYTES);
    size_t with = forest.size() * sizeof(Tree) + TreeFactory::count() * TreeType::APPROX_BYTES;
    std::printf("Bộ nhớ ước tính KHÔNG dùng Flyweight: %zu KB\n", without / 1024);
    std::printf("Bộ nhớ ước tính CÓ dùng Flyweight   : %zu KB\n", with / 1024);
}
