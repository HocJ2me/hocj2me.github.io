# Hướng dẫn cho giáo viên — Quản lý tài khoản khóa học Micro:bit

## 1. Cấu trúc thư mục này

```
training/
  courses.html       ← danh sách khóa học (trang sau khi đăng nhập)
  microbit.html      ← khóa học Micro:bit (bản đã có cổng đăng nhập)
  login.html
  register.html
  hash-tool.html
  auth.js
  users.json
  admin-huong-dan.md
```

Khi thêm khóa học mới, tạo thêm 1 file .html (ví dụ `khoa-moi.html`, cũng nhúng
`auth.js` + `requireAuth()` như các file khác), rồi thêm 1 thẻ khóa học mới
vào `courses.html` (sao chép thẻ `<a href="microbit.html" class="course-card">`
và sửa lại nội dung, đường link).

Toàn bộ thư mục `training/` này upload nguyên vẹn vào repo
`HocJ2me/hocj2me.github.io`. Sau đó vào `index.html` hiện tại, dán snippet
đã gửi trước đó để thêm 1 link trỏ tới `training/login.html`.

## 2. Vì sao lại như thế này

GitHub Pages chỉ phục vụ file tĩnh — không có máy chủ, không có cơ sở dữ liệu
thật. Vì vậy:

- **Không thể** để học sinh tự đăng ký và tự động ghi tài khoản mới lên
  GitHub từ trình duyệt (việc đó cần một "token" bí mật, mà đưa token vào
  trang web công khai thì ai cũng lấy được và có thể phá repo của bạn).
- Giải pháp ở đây: `users.json` là "danh sách tài khoản hợp lệ", đăng nhập
  được kiểm tra ngay trong trình duyệt bằng JavaScript. Đây là **cổng chặn
  đơn giản** — đủ để ngăn người ngoài xem ngẫu nhiên, **không phải bảo mật
  cấp doanh nghiệp**. Ai cố tình mở DevTools vẫn có thể vượt qua.
- Mật khẩu được băm SHA-256 trước khi lưu vào `users.json`, để ai đó lỡ mở
  file này ra xem cũng không thấy mật khẩu gốc.

## 3. Quy trình cấp tài khoản mới cho học sinh

1. Học sinh vào `register.html`, điền tên/lớp/tên đăng nhập mong muốn, bấm
   gửi → mở ra một **GitHub Issue** đã điền sẵn nội dung trong repo của bạn.
2. Bạn mở Issue đó, đọc thông tin (tên, lớp, username mong muốn).
3. Bạn tự nghĩ ra một mật khẩu cho học sinh (không viết mật khẩu vào Issue
   vì Issue là công khai).
4. Mở `hash-tool.html`, nhập đúng username và mật khẩu vừa nghĩ ra, bấm
   "Tạo mã hash" → công cụ trả về một dòng JSON đã đúng định dạng.
5. Mở file `users.json` trên GitHub (bấm biểu tượng bút chì để sửa trực
   tiếp trên trình duyệt), dán dòng JSON vừa copy vào, lưu (Commit changes).
6. Nhắn mật khẩu cho học sinh qua nhóm lớp/Zalo — **không** trả lời công
   khai trong GitHub Issue.
7. Đóng (Close) Issue lại.

## 4. Ví dụ nội dung `users.json`

```json
{
  "giaovien": "f386d0d2935f20e8c0a08dd33fdd83b8f611a4fa74730532932a5b60903e5742",
  "hocsinh_demo": "d3ad9315b7be5dd53b31a273b3b3aba5defe700808305aa16a3062b76658a791",
  "nguyenvana_6a1": "<dán hash mới ở đây>"
}
```

Tài khoản demo có sẵn để bạn dùng thử ngay: `hocsinh_demo` / mật khẩu
`demo123`. Nên xoá tài khoản demo này khi đưa vào dùng thật với học sinh.

## 5. Nếu muốn nâng cấp lên bảo mật thật sự sau này

Khi cần xác thực thật (mật khẩu mã hoá an toàn, chống dò mật khẩu, học sinh
tự đăng ký được ngay), có thể chuyển sang một dịch vụ xác thực miễn phí như
Firebase Authentication hoặc Supabase Auth — những dịch vụ này có gói miễn
phí, tích hợp bằng vài dòng JavaScript, không cần tự vận hành máy chủ.

## 6. Khóa Design Pattern (`design-pattern.html`)

File `design-pattern.html` được **sinh tự động** — đừng sửa tay trực tiếp. Mã nguồn nằm ở
thư mục `_src/design-pattern/` trong repo (không được xuất bản lên web):

- `content_*.py` — lý thuyết, sơ đồ UML của 24 mẫu; `content_lang.py` — giải thích code C++/Python, phần lập trình nhúng
- `cpp/`, `python/`, `java/` — 72 chương trình ví dụ
- Build lại: vào `_src/design-pattern/`, chạy `python -X utf8 build.py` (cần g++, Python 3.10+, Java 17+; kết quả chạy được lấy thật và lưu cache)

## 7. Các khóa sinh tự động khác (`cpp-co-ban.html`, `freertos.html`, `pcb-altium.html`)

Dùng chung bộ khung `_src/common/` (template giao diện, chạy code thật, tô màu cú pháp, vẽ hình SVG).
Mỗi khóa có thư mục riêng trong `_src/` gồm `course.py` (cấu hình + trang tổng quan),
`lessons*.py` (lý thuyết từng bài), `figs.py` (hình minh hoạ) và `code/` (chương trình ví dụ).
Build lại một khóa: vào thư mục của khóa, chạy `python -X utf8 course.py`.
