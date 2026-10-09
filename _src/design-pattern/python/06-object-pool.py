"""Object Pool – Python 3. Dùng contextmanager để "mượn – tự động trả" bằng câu lệnh with."""
from contextlib import contextmanager


class DbConnection:
    created = 0

    def __init__(self):
        DbConnection.created += 1
        self.id = DbConnection.created
        self.use_count = 0
        print(f"  (tạo mới kết nối #{self.id} – tốn ~200ms)")

    def query(self, sql):
        self.use_count += 1
        print(f"  #{self.id} chạy: {sql}")

    def reset(self):
        pass                                # xoá transaction dở dang...


class ConnectionPool:
    def __init__(self, max_size):
        self.max_size = max_size
        self._available = []
        self._in_use = set()

    def acquire(self):
        if self._available:
            conn = self._available.pop()
        elif len(self._in_use) < self.max_size:
            conn = DbConnection()
        else:
            return None
        self._in_use.add(conn)
        return conn

    def release(self, conn):
        if conn in self._in_use:
            self._in_use.remove(conn)
            conn.reset()
            self._available.append(conn)

    @contextmanager
    def connection(self):
        conn = self.acquire()
        try:
            yield conn
        finally:
            if conn: self.release(conn)     # luôn trả lại, kể cả khi có lỗi

    def status(self):
        print(f"  [Pool] đang dùng={len(self._in_use)}, rảnh={len(self._available)}, tối đa={self.max_size}")


if __name__ == "__main__":
    pool = ConnectionPool(2)
    a, b = pool.acquire(), pool.acquire()
    a.query("SELECT * FROM students")
    b.query("SELECT * FROM courses")
    pool.status()
    print("Lấy thêm khi pool đầy ->", pool.acquire())
    pool.release(a)
    pool.status()

    with pool.connection() as d:            # mượn bằng with, tự trả khi ra khỏi khối
        d.query("UPDATE scores SET point = 10")
        print("d có phải là a được tái sử dụng?", d is a)
        pool.status()
    pool.status()
    print("Tổng số kết nối thực sự được tạo:", DbConnection.created)
