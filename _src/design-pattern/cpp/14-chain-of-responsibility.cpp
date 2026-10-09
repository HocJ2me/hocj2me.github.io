// Chain of Responsibility – C++17
#include <iostream>
#include <string>

struct LeaveRequest {
    std::string teacher;
    int days;
    std::string reason;
};

// ===== Handler =====
class Approver {
public:
    virtual ~Approver() = default;

    // Trả về next để nối chuỗi: a.setNext(b).setNext(c)
    Approver& setNext(Approver& next) { next_ = &next; return next; }

    // Không virtual: lớp con không thể phá logic chuyển tiếp
    void handle(const LeaveRequest& r) const {
        if (canApprove(r)) {
            std::cout << "✅ " << role() << " duyệt: " << r.teacher << " nghỉ " << r.days
                      << " ngày (" << r.reason << ")\n";
        } else if (next_) {
            std::cout << "   " << role() << " chuyển tiếp đơn của " << r.teacher << "...\n";
            next_->handle(r);
        } else {
            std::cout << "❌ Không ai đủ thẩm quyền duyệt đơn " << r.days << " ngày của " << r.teacher << "\n";
        }
    }

protected:
    virtual bool canApprove(const LeaveRequest& r) const = 0;
    virtual const char* role() const = 0;

private:
    Approver* next_ = nullptr;                // con trỏ không sở hữu – các handler sống ở nơi khác
};

// ===== Concrete Handlers =====
class TeamLeader : public Approver {
protected:
    bool canApprove(const LeaveRequest& r) const override { return r.days <= 2; }
    const char* role() const override { return "Tổ trưởng"; }
};
class VicePrincipal : public Approver {
protected:
    bool canApprove(const LeaveRequest& r) const override { return r.days <= 5; }
    const char* role() const override { return "Hiệu phó"; }
};
class Principal : public Approver {
protected:
    bool canApprove(const LeaveRequest& r) const override { return r.days <= 30; }
    const char* role() const override { return "Hiệu trưởng"; }
};

int main() {
    TeamLeader lead;
    VicePrincipal vice;
    Principal principal;
    lead.setNext(vice).setNext(principal);   // lắp chuỗi – không cấp phát động

    lead.handle({"Cô Lan", 1, "Đi khám bệnh"});
    lead.handle({"Thầy Nam", 4, "Tập huấn chuyên môn"});
    lead.handle({"Cô Hoa", 10, "Nghỉ phép năm"});
    lead.handle({"Thầy Bình", 45, "Đi du học"});
}
