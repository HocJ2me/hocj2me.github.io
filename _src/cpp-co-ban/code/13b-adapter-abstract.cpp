// Con trỏ lớp trong thiết kế: Adapter (bọc lớp có sẵn) và Abstract (làm việc qua con trỏ lớp trừu tượng)
#include <iostream>
#include <memory>
#include <vector>

// ===== Interface mà chương trình của ta dùng =====
class IKhoangCach {
public:
    virtual ~IKhoangCach() = default;
    virtual float docCm() = 0;
};

class SieuAmHcSr04 : public IKhoangCach {                  // đã tương thích sẵn
public:
    float docCm() override { return 42.0f; }
};

// ===== Thư viện bên thứ ba: trả về MILIMET với tên hàm khác, không sửa được =====
class VL53L0X {
public:
    int readRangeMillimeters() { return 875; }
};

// ===== Adapter: giữ CON TRỎ tới đối tượng cũ, chuyển lời gọi + đổi đơn vị =====
class VL53Adapter : public IKhoangCach {
public:
    explicit VL53Adapter(VL53L0X* cb) : cb_(cb) {}
    float docCm() override { return cb_->readRangeMillimeters() / 10.0f; }
private:
    VL53L0X* cb_;
};

// ===== Abstract: robot chỉ cầm con trỏ tới IKhoangCach =====
class RobotTranhVatCan {
public:
    void them(std::unique_ptr<IKhoangCach> cb) { camBien_.push_back(std::move(cb)); }
    void buoc() {
        float gan = 1e9;
        for (auto& cb : camBien_) {                       // gọi qua con trỏ lớp trừu tượng
            float d = cb->docCm();
            std::cout << "  cảm biến báo " << d << " cm\n";
            if (d < gan) gan = d;
        }
        std::cout << "  -> vật cản gần nhất " << gan << " cm: " << (gan < 50 ? "RẼ" : "đi thẳng") << "\n";
    }
private:
    std::vector<std::unique_ptr<IKhoangCach>> camBien_;
};

int main() {
    static VL53L0X laser;                                  // đối tượng thư viện
    RobotTranhVatCan robot;
    robot.them(std::make_unique<SieuAmHcSr04>());
    robot.them(std::make_unique<VL53Adapter>(&laser));   // bọc bằng adapter rồi dùng như mọi cảm biến khác
    robot.buoc();

    std::cout << "\n  Xem thêm khóa Design Pattern: Adapter, Singleton, Strategy, State.\n";
}
