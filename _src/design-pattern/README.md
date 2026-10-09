# Nguồn khóa học Design Pattern

Sinh ra `training/design-pattern.html` của site (thư mục `_src/` không được GitHub Pages xuất bản).

```
python -X utf8 build.py            # biên dịch + chạy 72 ví dụ (có cache), vẽ UML, ghép template.html
```

- `content_creational.py`, `content_structural.py`, `content_behavioral.py`: lý thuyết + đặc tả UML
- `content_lang.py`: giải thích code C++ / Python, áp dụng nhúng, thư viện thực tế
- `cpp/` (C++17, ngôn ngữ chính), `python/`, `java/`: code ví dụ cùng kịch bản và tên lớp
- `uml.py` vẽ sơ đồ lớp, `illus.py` hình minh hoạ, `highlight.py` tô màu cú pháp, `template.html` giao diện
