# [hocj2me.github.io](https://hocj2me.github.io)

Trang cá nhân và tài liệu giảng dạy của Lê Chí Tuyền.

## Cấu trúc thư mục

```
index.html              Trang chủ
assets/
  img/                  Ảnh trang chủ: lớp học, sự kiện, giảng dạy (bản -t.jpg là ảnh thu nhỏ)
  du-an/                Ảnh các dự án, cuộc thi
training/               Cổng khóa học (cần đăng nhập)
  courses.html          Danh sách khóa học — /training/ tự chuyển tới đây
  microbit.html, thuyen-tu-dong.html, kinh-thong-minh.html
  design-pattern.html, cpp-co-ban.html   (sinh tự động từ _src/)
  login.html, register.html, auth.js, users.json, hash-tool.html
  admin-huong-dan.md    Hướng dẫn cấp tài khoản, thêm khóa học
bai-giang/              Bài giảng mở, không cần đăng nhập (có trang mục lục)
  ml-co-ban/            Machine Learning cơ bản
  quy-trinh-phan-mem/   Bài tập Quy trình phần mềm
_src/                   Mã nguồn sinh các trang khóa học (không xuất bản)
  common/               Bộ khung dùng chung: template, chạy code, tô màu cú pháp, vẽ SVG
  cpp-co-ban/           Khóa C++  → python -X utf8 course.py
  design-pattern/       Khóa Design Pattern → python -X utf8 build.py
_luu-tru/               Ảnh/file cũ không còn dùng (không xuất bản)
QuyTrinhPhanMem/, ML_cơ bản/   Chỉ còn trang chuyển hướng để link cũ vẫn chạy
```

Thư mục bắt đầu bằng `_` không được GitHub Pages (Jekyll) xuất bản lên web.

## Thêm khóa học mới

1. Tạo `training/ten-khoa.html` (nhúng `auth.js` + `requireAuth()` như các khóa khác).
2. Thêm thẻ khóa học vào `training/courses.html` **và** vào lưới `olc-grid` trong mục Khóa học của `index.html`.
