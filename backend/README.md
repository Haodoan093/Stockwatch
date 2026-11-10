# Backend — stockwatch API (Python / FastAPI)

Độc lập hoàn toàn với `frontend/`: chỉ giao tiếp qua HTTP (`/api/*`). Cách chạy xem
[../HUONG_DAN_CHAY.md](../HUONG_DAN_CHAY.md).

## Kiến trúc phân lớp

```
src/stockwatch/
├── api/            Tầng giao tiếp HTTP: routes/, schemas.py (hợp đồng với FE), errors.py, deps.py
├── services/       Nghiệp vụ (MarketService) — chỉ phụ thuộc giao diện repository
├── domain/         models.py (dataclass, enum) và ports.py (PriceProvider, PriceRepository, PriceSink)
├── providers/      Nguồn dữ liệu bên ngoài: demo, vnstock; normalize.py; factory.py
├── repositories/   Nơi đọc/ghi giá: memory.py (không lưu), sql.py (SQLite/PostgreSQL)
├── features/       Tính toán thuần: chỉ báo kỹ thuật (indicators.py)
├── core/           settings.py (biến môi trường), errors.py, retry.py, watchlist.py
├── bootstrap.py    Composition root: chọn triển khai theo Settings
└── cli.py          Lệnh `stockwatch fetch` (lấy giá và lưu DB)
```

Quy tắc phụ thuộc (mũi tên = "được phép import"):

```
api → services → domain ← providers / repositories      core: dùng được ở mọi tầng
        bootstrap lắp ghép tất cả; chỉ api/app.py và cli.py gọi tới
```

- `domain` không import FastAPI, SQLAlchemy hay vnstock.
- `services` không biết dữ liệu đến từ provider nào hay lưu ở đâu.
- Muốn thêm nguồn dữ liệu: viết class `PriceProvider` trong `providers/` rồi đăng ký ở `factory.py`.
- Muốn thêm endpoint: thêm service method, schema trong `api/schemas.py`, route trong `api/routes/`.
- Thêm tính năng lớn (tin tức, mô hình AI): thêm package cùng cấp (ví dụ `news/`, `ml/`) với port
  riêng trong `domain/ports.py`, rồi nối ở `bootstrap.py`.

## Test

```
tests/
├── conftest.py     Fixture dùng chung (make_prices, sql_repo)
├── unit/           Test từng thành phần, không cần mạng
└── api/            Test hợp đồng HTTP bằng TestClient
```

## Cấu hình

Biến môi trường: xem [.env.example](.env.example). Danh sách mã: `config/watchlist.toml`.
