"""Chain of Responsibility – Python 3."""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class LeaveRequest:
    teacher: str
    days: int
    reason: str


class Approver(ABC):
    role = "?"

    def __init__(self):
        self._next = None

    def set_next(self, nxt):
        self._next = nxt
        return nxt

    def handle(self, r: LeaveRequest):
        if self.can_approve(r):
            print(f"✅ {self.role:<12} duyệt: {r.teacher} nghỉ {r.days} ngày ({r.reason})")
        elif self._next:
            print(f"   {self.role:<12} chuyển tiếp đơn của {r.teacher}...")
            self._next.handle(r)
        else:
            print(f"❌ Không ai đủ thẩm quyền duyệt đơn {r.days} ngày của {r.teacher}")

    @abstractmethod
    def can_approve(self, r) -> bool: ...


class TeamLeader(Approver):
    role = "Tổ trưởng"
    def can_approve(self, r): return r.days <= 2


class VicePrincipal(Approver):
    role = "Hiệu phó"
    def can_approve(self, r): return r.days <= 5


class Principal(Approver):
    role = "Hiệu trưởng"
    def can_approve(self, r): return r.days <= 30


if __name__ == "__main__":
    chain = TeamLeader()
    chain.set_next(VicePrincipal()).set_next(Principal())
    for req in (LeaveRequest("Cô Lan", 1, "Đi khám bệnh"),
                LeaveRequest("Thầy Nam", 4, "Tập huấn chuyên môn"),
                LeaveRequest("Cô Hoa", 10, "Nghỉ phép năm"),
                LeaveRequest("Thầy Bình", 45, "Đi du học")):
        chain.handle(req)
