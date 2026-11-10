# Hướng dẫn chạy frontend + backend

Dự án gồm 2 phần độc lập, chạy ở 2 cửa sổ terminal:

| Phần | Thư mục | Công nghệ | Cổng mặc định |
|------|---------|-----------|---------------|
| Backend | `backend/` | Python 3.11+ / FastAPI | 8000 |
| Frontend | `frontend/` | Node 20+ / React + Vite | 5173 |

Lệnh dưới đây viết cho **Windows PowerShell**. Mặc định dùng **dữ liệu demo**, không cần database.

## 1. Chạy backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn stockwatch.api.app:app_factory --factory --port 8000 --reload
```

Nếu PowerShell chặn script kích hoạt venv, chạy một lần:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. Hoặc bỏ qua bước kích hoạt và gọi trực tiếp
`.\.venv\Scripts\python.exe -m uvicorn stockwatch.api.app:app_factory --factory --port 8000`.

Kiểm tra: mở http://127.0.0.1:8000/api/health, kết quả mong đợi:

```json
{"status":"ok","tickers":10,"sources":["demo"]}
```

Tài liệu API tự sinh: http://127.0.0.1:8000/docs

## 2. Chạy frontend

Mở terminal thứ hai:

```powershell
cd frontend
npm install
npm run dev
```

Mở http://localhost:5173. Dev server tự chuyển các request `/api/*` sang backend ở cổng 8000.

## 3. Test và kiểm tra chất lượng

Backend (trong `backend/`, đã kích hoạt venv):

```powershell
pytest
ruff check src tests
```

Frontend (trong `frontend/`):

```powershell
npx tsc --noEmit
npm run build
```

## 4. Cấu hình

### Backend (biến môi trường, xem `backend/.env.example`)

| Biến | Giá trị | Ý nghĩa |
|------|---------|---------|
| `STOCKWATCH_PROVIDER` | `demo` (mặc định), `vnstock` | Nguồn giá |
| `STOCKWATCH_REPOSITORY` | `memory` (mặc định), `db` | `db` đọc từ `DATABASE_URL` |
| `DATABASE_URL` | SQLite hoặc PostgreSQL | Chỉ dùng khi `db` hoặc lệnh `stockwatch fetch` |
| `STOCKWATCH_WATCHLIST` | đường dẫn file | Mặc định `config/watchlist.toml` |
| `STOCKWATCH_CORS_ORIGINS` | danh sách, cách nhau dấu phẩy | Nguồn được gọi API từ trình duyệt |

Đặt biến trong PowerShell trước khi chạy uvicorn, ví dụ:
`$env:STOCKWATCH_PROVIDER = "vnstock"`.

Sửa danh sách mã theo dõi ở `backend/config/watchlist.toml` rồi khởi động lại backend.

### Frontend (xem `frontend/.env.example`)

| Biến | Ý nghĩa |
|------|---------|
| `VITE_PROXY_TARGET` | Backend mà `npm run dev` proxy tới (mặc định `http://127.0.0.1:8000`) |
| `VITE_API_BASE_URL` | Địa chỉ API khi deploy frontend tách khỏi backend; để trống khi dev |

## 5. Dữ liệu thật (vnstock)

Tại thời điểm tạo dự án (2026-11-10), `pip install vnstock` báo "No matching distribution" (trang
gói trên PyPI trả 404). Cần tự kiểm tra:

1. Thử lại `pip install -e ".[vn]"` trong `backend/` (có thể là lỗi tạm thời).
2. Đọc README/issue của repo vnstock xem tên gói hoặc cách cài hiện tại.
3. Nếu cài từ git, xem lại mã nguồn trước khi chạy.

Khi cài được, đặt `STOCKWATCH_PROVIDER=vnstock` rồi khởi động lại backend. Giao diện sẽ bỏ nhãn
"Dữ liệu demo" khi nguồn không còn là demo.

## 6. Lưu dữ liệu vào PostgreSQL (tuỳ chọn, chưa bật mặc định)

Cần bật Docker Desktop. Từ thư mục gốc dự án:

```powershell
docker compose up -d db
cd backend
$env:DATABASE_URL = "postgresql://stockwatch:stockwatch@localhost:5432/stockwatch"
python -m stockwatch.cli fetch --provider demo
$env:STOCKWATCH_REPOSITORY = "db"
uvicorn stockwatch.api.app:app_factory --factory --port 8000
```

Mật khẩu trong `docker-compose.yml` chỉ dành cho máy dev local. Có thể trỏ `DATABASE_URL` tới
Supabase (PostgreSQL host sẵn) mà không cần sửa code.

## 7. Xử lý sự cố

| Triệu chứng | Cách xử lý |
|-------------|-----------|
| Trang báo "Không kết nối được máy chủ dữ liệu" | Backend chưa chạy hoặc khác cổng. Kiểm tra http://127.0.0.1:8000/api/health |
| `npm run dev` báo cổng 5173 đã dùng | Tắt tiến trình đang giữ cổng hoặc chạy `npm run dev -- --port 5174` |
| Lỗi `ModuleNotFoundError: stockwatch` | Chưa cài: chạy `pip install -e ".[dev]"` trong `backend/` với venv đã kích hoạt |
| `pip install vnstock` lỗi | Xem mục 5 |
| Biểu đồ trống | Mở F12 → Console/Network xem request `/api/prices/...` trả mã gì |
