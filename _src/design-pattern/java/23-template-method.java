import java.util.List;

public class TemplateMethodDemo {
    public static void main(String[] args) {
        ReportGenerator[] generators = { new CsvReport(), new HtmlReport() };
        for (ReportGenerator g : generators) {
            g.generate();
            System.out.println();
        }
    }
}

/** AbstractClass – định nghĩa "khung" thuật toán, các bước cụ thể để lớp con lo. */
abstract class ReportGenerator {

    /** TEMPLATE METHOD – final để lớp con không phá vỡ trình tự các bước. */
    public final void generate() {
        List<String[]> rows = loadData();      // bước chung
        rows = filter(rows);                   // hook (tuỳ chọn ghi đè)
        writeHeader();                         // bước trừu tượng
        for (String[] r : rows) writeRow(r);   // bước trừu tượng
        writeFooter(rows.size());              // bước trừu tượng
        if (shouldLog()) System.out.println("   (đã ghi log xuất báo cáo)");   // hook
    }

    /** Bước chung, cài đặt sẵn. */
    private List<String[]> loadData() {
        return List.of(
                new String[]{"An", "9.0"},
                new String[]{"Bình", "6.5"},
                new String[]{"Chi", "4.0"});
    }

    /** Hook – có cài đặt mặc định, lớp con CÓ THỂ ghi đè. */
    protected List<String[]> filter(List<String[]> rows) { return rows; }
    protected boolean shouldLog() { return false; }

    /** Primitive operations – lớp con BẮT BUỘC cài đặt. */
    protected abstract void writeHeader();
    protected abstract void writeRow(String[] row);
    protected abstract void writeFooter(int count);
}

class CsvReport extends ReportGenerator {
    protected void writeHeader()          { System.out.println("ho_ten,diem"); }
    protected void writeRow(String[] r)   { System.out.println(r[0] + "," + r[1]); }
    protected void writeFooter(int count) { System.out.println("# " + count + " dòng"); }
}

class HtmlReport extends ReportGenerator {
    /** Ghi đè hook: chỉ lấy học sinh đạt (>= 5). */
    @Override protected List<String[]> filter(List<String[]> rows) {
        return rows.stream().filter(r -> Double.parseDouble(r[1]) >= 5).toList();
    }
    @Override protected boolean shouldLog() { return true; }

    protected void writeHeader()          { System.out.println("<table><tr><th>Họ tên</th><th>Điểm</th></tr>"); }
    protected void writeRow(String[] r)   { System.out.println("  <tr><td>" + r[0] + "</td><td>" + r[1] + "</td></tr>"); }
    protected void writeFooter(int count) { System.out.println("</table> <!-- " + count + " học sinh đạt -->"); }
}
