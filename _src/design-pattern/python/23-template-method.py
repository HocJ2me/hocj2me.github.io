"""Template Method – Python 3."""
from abc import ABC, abstractmethod


class ReportGenerator(ABC):
    def generate(self):                             # TEMPLATE METHOD (Python không có final – quy ước không ghi đè)
        rows = self._load_data()
        rows = self.filter(rows)                    # hook
        self.write_header()
        for r in rows:
            self.write_row(r)
        self.write_footer(len(rows))
        if self.should_log():                       # hook
            print("   (đã ghi log xuất báo cáo)")

    def _load_data(self):
        return [("An", 9.0), ("Bình", 6.5), ("Chi", 4.0)]

    # Hooks
    def filter(self, rows): return rows
    def should_log(self): return False

    # Primitive operations
    @abstractmethod
    def write_header(self): ...

    @abstractmethod
    def write_row(self, r): ...

    @abstractmethod
    def write_footer(self, n): ...


class CsvReport(ReportGenerator):
    def write_header(self): print("ho_ten,diem")
    def write_row(self, r): print(f"{r[0]},{r[1]}")
    def write_footer(self, n): print(f"# {n} dòng")


class HtmlReport(ReportGenerator):
    def filter(self, rows): return [r for r in rows if r[1] >= 5]
    def should_log(self): return True
    def write_header(self): print("<table><tr><th>Họ tên</th><th>Điểm</th></tr>")
    def write_row(self, r): print(f"  <tr><td>{r[0]}</td><td>{r[1]}</td></tr>")
    def write_footer(self, n): print(f"</table> <!-- {n} học sinh đạt -->")


if __name__ == "__main__":
    for g in (CsvReport(), HtmlReport()):
        g.generate()
        print()
