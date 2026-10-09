public class ChainDemo {
    public static void main(String[] args) {
        // Xây dựng chuỗi xử lý: Tổ trưởng -> Hiệu phó -> Hiệu trưởng
        Approver chain = new TeamLeader();
        chain.setNext(new VicePrincipal())
             .setNext(new Principal());

        chain.handle(new LeaveRequest("Cô Lan", 1, "Đi khám bệnh"));
        chain.handle(new LeaveRequest("Thầy Nam", 4, "Tập huấn chuyên môn"));
        chain.handle(new LeaveRequest("Cô Hoa", 10, "Nghỉ phép năm"));
        chain.handle(new LeaveRequest("Thầy Bình", 45, "Đi du học"));
    }
}

/** Request – dữ liệu được chuyền qua chuỗi. */
record LeaveRequest(String teacher, int days, String reason) { }

/** Handler – định nghĩa giao diện xử lý + liên kết tới mắt xích kế tiếp. */
abstract class Approver {
    private Approver next;

    /** Trả về next để có thể nối chuỗi kiểu a.setNext(b).setNext(c). */
    public Approver setNext(Approver next) {
        this.next = next;
        return next;
    }

    /** Template: tự xử lý nếu được, không thì chuyển tiếp. */
    public final void handle(LeaveRequest r) {
        if (canApprove(r)) {
            System.out.printf("✅ %-14s duyệt: %s nghỉ %d ngày (%s)%n", role(), r.teacher(), r.days(), r.reason());
        } else if (next != null) {
            System.out.printf("   %-14s chuyển tiếp đơn của %s...%n", role(), r.teacher());
            next.handle(r);
        } else {
            System.out.printf("❌ Không ai đủ thẩm quyền duyệt đơn %d ngày của %s%n", r.days(), r.teacher());
        }
    }

    protected abstract boolean canApprove(LeaveRequest r);
    protected abstract String role();
}

/** Concrete Handlers */
class TeamLeader extends Approver {
    protected boolean canApprove(LeaveRequest r) { return r.days() <= 2; }
    protected String role() { return "Tổ trưởng"; }
}
class VicePrincipal extends Approver {
    protected boolean canApprove(LeaveRequest r) { return r.days() <= 5; }
    protected String role() { return "Hiệu phó"; }
}
class Principal extends Approver {
    protected boolean canApprove(LeaveRequest r) { return r.days() <= 30; }
    protected String role() { return "Hiệu trưởng"; }
}
