// Proxy – C++17
#include <cstdio>
#include <iostream>
#include <map>
#include <memory>
#include <optional>
#include <string>

// ===== Ví dụ 1: Virtual Proxy =====
class Image {
public:
    virtual ~Image() = default;
    virtual void display() = 0;
};

class RealImage : public Image {
public:
    explicit RealImage(std::string file) : file_(std::move(file)) {
        std::cout << "  ⏳ Đang tải " << file_ << " từ thẻ SD (rất chậm)...\n";
    }
    void display() override { std::cout << "  🖼️  Hiển thị " << file_ << "\n"; }
private:
    std::string file_;
};

class LazyImageProxy : public Image {
public:
    explicit LazyImageProxy(std::string file) : file_(std::move(file)) {}
    void display() override {
        if (!real_) real_ = std::make_unique<RealImage>(file_);   // chỉ tạo khi cần
        real_->display();
    }
private:
    std::string file_;
    std::unique_ptr<RealImage> real_;
};

// ===== Ví dụ 2: Protection + Caching Proxy =====
class ScoreService {
public:
    virtual ~ScoreService() = default;
    virtual std::string getScore(const std::string& student) = 0;
    virtual void updateScore(const std::string& student, double score) = 0;
};

class RealScoreService : public ScoreService {
public:
    std::string getScore(const std::string& s) override {
        std::cout << "  (truy vấn cơ sở dữ liệu...)\n";
        char buf[64];
        std::snprintf(buf, sizeof buf, "%s: %.1f", s.c_str(), db_[s]);
        return buf;
    }
    void updateScore(const std::string& s, double v) override {
        db_[s] = v;
        std::cout << "  Đã cập nhật điểm " << s << " = " << v << "\n";
    }
private:
    std::map<std::string, double> db_{ {"An", 8.0} };
};

class ScoreServiceProxy : public ScoreService {
public:
    ScoreServiceProxy(RealScoreService& real, std::string role) : real_(real), role_(std::move(role)) {}

    std::string getScore(const std::string& s) override {           // caching
        auto it = cache_.find(s);
        if (it != cache_.end()) return it->second;
        return cache_[s] = real_.getScore(s);
    }
    void updateScore(const std::string& s, double v) override {     // protection
        if (role_ != "giaovien") {
            std::cout << "  ⛔ " << role_ << " không có quyền sửa điểm!\n";
            return;
        }
        real_.updateScore(s, v);
        cache_.erase(s);                                              // làm mới cache
    }
private:
    RealScoreService& real_;
    std::string role_;
    std::map<std::string, std::string> cache_;
};

int main() {
    LazyImageProxy photo("anh-lop-hoc-4k.jpg");
    std::cout << "Đã tạo proxy, ảnh CHƯA được tải.\n";
    photo.display();
    photo.display();

    std::cout << "-----\n";
    RealScoreService db;
    ScoreServiceProxy teacher(db, "giaovien");
    ScoreServiceProxy student(db, "hocsinh");
    std::cout << teacher.getScore("An") << "\n";
    std::cout << teacher.getScore("An") << "\n";
    teacher.updateScore("An", 9.5);
    std::cout << teacher.getScore("An") << "\n";
    student.updateScore("An", 10);
}
