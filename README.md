# stockwatch

Dự án học tập: theo dõi cổ phiếu Việt Nam, phân tích tin tức bằng AI, vận hành theo chuẩn DevOps.
Đây là công cụ thử nghiệm, **không phải khuyến nghị đầu tư**.

| Tài liệu | Nội dung |
|----------|----------|
| [HUONG_DAN_CHAY.md](HUONG_DAN_CHAY.md) | Hướng dẫn chạy frontend + backend từng bước |
| [PLAN.md](PLAN.md) | Kế hoạch chi tiết các giai đoạn |
| [backend/README.md](backend/README.md) | Kiến trúc backend |
| [frontend/README.md](frontend/README.md) | Kiến trúc frontend |

## Cấu trúc thư mục

```
.
├── backend/              API Python (FastAPI) — độc lập, có venv, test và cấu hình riêng
├── frontend/             Web React + Vite + TypeScript — độc lập, có package.json riêng
├── docker-compose.yml    PostgreSQL cho dev (chưa bật mặc định)
├── PLAN.md
└── HUONG_DAN_CHAY.md
```

Hai phần chỉ giao tiếp qua HTTP (`/api/*`), có thể phát triển, test, build và deploy riêng.

## Trạng thái

- Dữ liệu hiện là **demo tự sinh** (nhãn "Dữ liệu demo" hiện trên giao diện), giữ trong bộ nhớ.
- Lớp lưu trữ PostgreSQL/SQLite đã có và có test nhưng chưa bật làm mặc định.
- Gói `vnstock` chưa cài được từ PyPI (2026-11-10), nên chưa có dữ liệu thật. Xem
  [HUONG_DAN_CHAY.md](HUONG_DAN_CHAY.md#dữ-liệu-thật-vnstock).
