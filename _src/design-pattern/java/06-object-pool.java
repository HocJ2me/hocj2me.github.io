import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashSet;
import java.util.Set;

public class ObjectPoolDemo {
    public static void main(String[] args) {
        ConnectionPool pool = new ConnectionPool(2); // tối đa 2 kết nối

        DbConnection a = pool.acquire();
        DbConnection b = pool.acquire();
        a.query("SELECT * FROM students");
        b.query("SELECT * FROM courses");
        pool.printStatus();

        DbConnection c = pool.acquire();             // pool đã cạn
        System.out.println("Lấy thêm khi pool đầy -> " + c);

        pool.release(a);                             // trả lại -> có thể tái sử dụng
        pool.printStatus();

        DbConnection d = pool.acquire();
        d.query("UPDATE scores SET point = 10");
        System.out.println("d có phải là kết nối a được tái sử dụng? " + (d == a));
        pool.printStatus();
        System.out.println("Tổng số kết nối thực sự được tạo: " + DbConnection.created);
    }
}

/** Đối tượng "đắt" – tạo mới tốn thời gian (mở socket, bắt tay, xác thực...). */
class DbConnection {
    static int created = 0;
    private final int id;
    private int useCount = 0;

    DbConnection() {
        id = ++created;
        System.out.println("  (tạo mới kết nối #" + id + " – tốn ~200ms)");
    }
    void query(String sql) { useCount++; System.out.println("  #" + id + " chạy: " + sql); }
    void reset()           { /* xoá transaction dở dang, đặt lại trạng thái */ }
    @Override public String toString() { return "Conn#" + id + "(đã dùng " + useCount + " lần)"; }
}

/** Object Pool – quản lý tập đối tượng có thể tái sử dụng. */
class ConnectionPool {
    private final int maxSize;
    private final Deque<DbConnection> available = new ArrayDeque<>();
    private final Set<DbConnection> inUse = new HashSet<>();

    ConnectionPool(int maxSize) { this.maxSize = maxSize; }

    public synchronized DbConnection acquire() {
        DbConnection conn;
        if (!available.isEmpty()) {
            conn = available.pop();                  // ưu tiên tái sử dụng
        } else if (inUse.size() < maxSize) {
            conn = new DbConnection();               // còn hạn mức -> tạo mới
        } else {
            return null;                             // hết -> trả null (thực tế: chờ hoặc ném lỗi)
        }
        inUse.add(conn);
        return conn;
    }

    public synchronized void release(DbConnection conn) {
        if (inUse.remove(conn)) {
            conn.reset();                            // làm sạch trước khi cho mượn lại
            available.push(conn);
        }
    }

    void printStatus() {
        System.out.println("  [Pool] đang dùng=" + inUse.size() + ", rảnh=" + available.size() + ", tối đa=" + maxSize);
    }
}
