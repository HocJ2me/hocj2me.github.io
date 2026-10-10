# Lập trình hướng đối tượng cơ bản: class, __init__, phương thức, kế thừa


class HocSinh:
    truong = "THCS Bách Khoa"                 # thuộc tính chung của lớp

    def __init__(self, ten, lop):              # hàm khởi tạo, chạy khi tạo đối tượng
        self.ten = ten                         # self = chính đối tượng đang tạo
        self.lop = lop
        self.diem = []

    def them_diem(self, d):
        if 0 <= d <= 10:
            self.diem.append(d)

    def diem_tb(self):
        return round(sum(self.diem) / len(self.diem), 2) if self.diem else 0

    def __str__(self):                         # quy định cách in đối tượng
        return f"{self.ten} ({self.lop}) – TB {self.diem_tb()}"


an = HocSinh("An", "7A")
chi = HocSinh("Chi", "7B")
for d in (8, 9, 7.5, 12):                      # 12 bị bỏ qua vì không hợp lệ
    an.them_diem(d)
chi.them_diem(10)
print(an)
print(chi)
print("Trường:", an.truong, "| điểm của An:", an.diem)


# ----- Kế thừa: lớp con dùng lại và mở rộng lớp cha -----
class ThietBi:
    def __init__(self, ten):
        self.ten = ten
        self.bat = False

    def bat_tat(self):
        self.bat = not self.bat
        print(f"{self.ten}: {'BẬT' if self.bat else 'TẮT'}")


class Quat(ThietBi):
    def __init__(self, ten, so=1):
        super().__init__(ten)                  # gọi khởi tạo của lớp cha
        self.so = so

    def doi_so(self, so):
        self.so = so
        print(f"{self.ten}: số {so}")


class Den(ThietBi):
    def bat_tat(self):                         # ghi đè (override) hành vi của lớp cha
        super().bat_tat()
        print(f"  -> đèn {'sáng' if self.bat else 'tối'}")


nha = [Den("Đèn phòng khách"), Quat("Quạt trần", 2)]
for tb in nha:                                 # đa hình: cùng gọi bat_tat()
    tb.bat_tat()
nha[1].doi_so(3)
print("Quạt là ThietBi?", isinstance(nha[1], ThietBi))
