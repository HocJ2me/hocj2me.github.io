// Template Method – C++17. Ví dụ quen thuộc nhất với người làm nhúng:
// khung chương trình Arduino gọi setup() một lần rồi loop() mãi mãi – bạn chỉ "điền các bước".
#include <iostream>
#include <string>
#include <vector>

struct Row { std::string name; double score; };

// ===== AbstractClass =====
class ReportGenerator {
public:
    virtual ~ReportGenerator() = default;

    // TEMPLATE METHOD – không virtual, lớp con không thể đổi trình tự
    void generate() {
        std::vector<Row> rows = loadData();
        rows = filter(rows);                        // hook
        writeHeader();
        for (const Row& r : rows) writeRow(r);
        writeFooter(rows.size());
        if (shouldLog()) std::cout << "   (đã ghi log xuất báo cáo)\n";   // hook
    }

protected:
    // Hook – có mặc định, CÓ THỂ ghi đè
    virtual std::vector<Row> filter(const std::vector<Row>& rows) { return rows; }
    virtual bool shouldLog() const { return false; }

    // Primitive operations – BẮT BUỘC ghi đè (thuần ảo)
    virtual void writeHeader() = 0;
    virtual void writeRow(const Row& r) = 0;
    virtual void writeFooter(size_t count) = 0;

private:
    std::vector<Row> loadData() const { return { {"An", 9.0}, {"Bình", 6.5}, {"Chi", 4.0} }; }
};

class CsvReport : public ReportGenerator {
protected:
    void writeHeader() override           { std::cout << "ho_ten,diem\n"; }
    void writeRow(const Row& r) override  { std::cout << r.name << "," << r.score << "\n"; }
    void writeFooter(size_t n) override   { std::cout << "# " << n << " dòng\n"; }
};

class HtmlReport : public ReportGenerator {
protected:
    std::vector<Row> filter(const std::vector<Row>& rows) override {
        std::vector<Row> passed;
        for (const Row& r : rows) if (r.score >= 5) passed.push_back(r);
        return passed;
    }
    bool shouldLog() const override { return true; }
    void writeHeader() override          { std::cout << "<table><tr><th>Họ tên</th><th>Điểm</th></tr>\n"; }
    void writeRow(const Row& r) override { std::cout << "  <tr><td>" << r.name << "</td><td>" << r.score << "</td></tr>\n"; }
    void writeFooter(size_t n) override  { std::cout << "</table> <!-- " << n << " học sinh đạt -->\n"; }
};

int main() {
    CsvReport csv;
    HtmlReport html;
    ReportGenerator* generators[] = { &csv, &html };
    for (ReportGenerator* g : generators) {
        g->generate();
        std::cout << "\n";
    }
}
