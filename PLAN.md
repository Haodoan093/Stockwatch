# Kế hoạch dự án: Nền tảng theo dõi chứng khoán + phân tích tin tức bằng AI (học DevOps & ML)

> Dự án thử nghiệm / học tập. Đầu ra của mô hình là **tín hiệu phân tích**, không phải khuyến nghị đầu tư.

## 1. Mục tiêu

| # | Mục tiêu | Tiêu chí hoàn thành |
|---|----------|---------------------|
| 1 | Theo dõi giá cổ phiếu (VN + quốc tế) theo watchlist của người dùng | Dữ liệu giá cập nhật mỗi ngày, hiển thị trên dashboard |
| 2 | Thu thập và phân tích tin tức theo từng mã | Mỗi tin có điểm cảm xúc + tóm tắt, gắn đúng mã |
| 3 | Mô hình đưa "nhận định" dựa trên biểu đồ + tin tức | Có đánh giá walk-forward, báo cáo rõ độ tin cậy |
| 4 | Vận hành theo chuẩn DevOps | Docker, CI/CD, IaC, giám sát, deploy được lên AWS |

**Ngoài phạm vi (giai đoạn đầu):** giao dịch tự động, dữ liệu real-time tick, ứng dụng mobile, đăng nhập nhiều người dùng phức tạp.

## 2. Kiến trúc tổng quan

```
[Nguồn giá: vnstock / yfinance / Alpha Vantage]──┐
[Nguồn tin: RSS, API tin tức]────────────────────┤
                                                  ▼
                                   Ingestion jobs (Python, lịch chạy hằng ngày)
                                                  ▼
                       Raw storage (S3 / thư mục local)  →  PostgreSQL (dữ liệu đã chuẩn hóa)
                                                  ▼
                       Feature + NLP pipeline (chỉ báo kỹ thuật, sentiment, tóm tắt)
                                                  ▼
                       Model service (FastAPI) ← model registry (file/MLflow)
                                                  ▼
                       Dashboard (Streamlit hoặc Next.js) + Grafana (giám sát)
```

## 3. Công nghệ đề xuất

- **Ngôn ngữ:** Python 3.12
- **Dữ liệu giá:** `vnstock` (VN), `yfinance` hoặc Alpha Vantage (quốc tế). Bọc sau một lớp `PriceProvider` để đổi nguồn dễ dàng.
- **Tin tức:** RSS của các trang tài chính VN/quốc tế, hoặc API tin tức. Kiểm tra điều khoản sử dụng từng nguồn.
- **NLP:** FinBERT (EN), PhoBERT (VI) cho sentiment; LLM (ví dụ Claude API) cho tóm tắt.
- **Cơ sở dữ liệu:** SQLite lúc đầu, chuyển PostgreSQL khi lên Docker Compose.
- **API:** FastAPI. **Dashboard:** Streamlit (nhanh) rồi cân nhắc Next.js sau.
- **Lập lịch:** cron / APScheduler lúc đầu, Airflow hoặc EventBridge khi cần.
- **DevOps:** Docker, Docker Compose, GitHub Actions, Terraform, Prometheus + Grafana.
- **ML tracking:** MLflow (tùy chọn).

## 4. Cấu trúc thư mục

Đã chia thành 2 phần độc lập (chi tiết kiến trúc: `backend/README.md`, `frontend/README.md`).
Các thư mục đánh dấu (sau) là dự kiến cho các giai đoạn tới.

```
.
├── PLAN.md, README.md, HUONG_DAN_CHAY.md
├── docker-compose.yml
├── backend/                 # Python / FastAPI
│   ├── pyproject.toml, config/, tests/{unit,api}/
│   └── src/stockwatch/
│       ├── api/             # routes, schemas, errors
│       ├── services/        # nghiệp vụ
│       ├── domain/          # models, ports
│       ├── providers/       # nguồn dữ liệu (demo, vnstock)
│       ├── repositories/    # memory, sql (SQLite/PostgreSQL)
│       ├── features/        # chỉ báo kỹ thuật
│       ├── core/            # settings, errors, retry
│       ├── news/            # (sau) thu thập tin, gắn mã
│       └── ml/              # (sau) sentiment, mô hình nhận định
├── frontend/                # React + Vite + TypeScript
│   └── src/{app,features/{market,insights},shared,styles}
├── infra/terraform/         # (sau) hạ tầng AWS
├── .github/workflows/       # (sau) ci.yml, deploy.yml
└── monitoring/              # (sau) prometheus, grafana
```

Đã đổi so với kế hoạch ban đầu: dashboard là web React thay cho Streamlit; mỗi phần có
môi trường và cấu hình riêng.

## 5. Lộ trình theo giai đoạn

Thời gian ước tính cho người làm bán thời gian (~8–10 giờ/tuần). Điều chỉnh theo thực tế.

### Giai đoạn 0 — Chuẩn bị (3–5 ngày)
- Cài Python, Docker Desktop, Git; tạo repo, `pyproject.toml`, pre-commit (ruff, black).
- Quyết định thị trường ban đầu (VN, Mỹ hay cả hai) và danh sách 10–20 mã thử nghiệm.
- **Hoàn thành khi:** `pytest` chạy được (dù chỉ 1 test), repo có README.

### Giai đoạn 1 — Thu thập dữ liệu giá (1–2 tuần)
- Lớp `PriceProvider` + 2 triển khai (vnstock, yfinance). Retry có backoff khi gặp lỗi 429/timeout.
- Lưu dữ liệu thô (OHLCV) và bảng chuẩn hóa. Xử lý ngày nghỉ, mã bị đổi/hủy niêm yết, điều chỉnh cổ tức/chia tách.
- Job chạy hằng ngày, idempotent (chạy lại không trùng dữ liệu).
- **Hoàn thành khi:** có ít nhất 2–3 năm dữ liệu cho watchlist, có test cho từng provider (dùng dữ liệu mẫu, không gọi mạng).

### Giai đoạn 2 — Chỉ báo kỹ thuật + dashboard cơ bản (1 tuần)
- Tính MA, RSI, MACD, biến động, khối lượng bất thường.
- Dashboard Streamlit: chọn mã, biểu đồ nến, chỉ báo.
- **Hoàn thành khi:** xem được biểu đồ và chỉ báo của mọi mã trong watchlist.

### Giai đoạn 3 — Docker hóa + CI (1 tuần)
- Dockerfile cho từng thành phần, `docker-compose.yml` (app, db, dashboard).
- GitHub Actions: lint, test, build image trên mỗi push/PR.
- **Hoàn thành khi:** `docker compose up` chạy toàn bộ hệ thống trên máy sạch; CI xanh.

### Giai đoạn 4 — Pipeline tin tức + sentiment (2 tuần)
- Thu thập tin theo mã (RSS/API), loại trùng, gắn tin vào mã (khớp tên công ty, ticker, từ đồng nghĩa).
- Sentiment: bắt đầu bằng mô hình có sẵn (FinBERT/PhoBERT), đo thử trên ~200 tin tự gán nhãn, sau đó fine-tune nếu cần.
- Tóm tắt tin bằng LLM, lưu cùng điểm sentiment.
- **Hoàn thành khi:** mỗi mã có danh sách tin, điểm cảm xúc, tóm tắt; có báo cáo độ chính xác sentiment trên tập tự gán nhãn.

### Giai đoạn 5 — Mô hình nhận định (2–3 tuần)
- Định nghĩa bài toán rõ ràng, ví dụ: dự đoán hướng giá sau N ngày (tăng/giảm) hoặc phân loại "tín hiệu mạnh/yếu".
- Đặc trưng: chỉ báo kỹ thuật, sentiment tổng hợp theo ngày, khối lượng.
- Baseline đơn giản trước (logistic regression, gradient boosting), so sánh với "luôn đoán tăng".
- Đánh giá bằng **walk-forward validation**, tính cả phí giao dịch và trượt giá; tránh look-ahead bias và survivorship bias.
- **Hoàn thành khi:** có báo cáo so sánh với baseline; nếu mô hình không vượt baseline, ghi nhận kết quả và điều chỉnh bài toán thay vì ép kết quả đẹp.

### Giai đoạn 6 — Model service + tích hợp dashboard (1 tuần)
- FastAPI endpoint: `/predict?ticker=`, `/news?ticker=`, `/health`.
- Dashboard hiển thị nhận định kèm xác suất, độ tin cậy và cảnh báo "không phải khuyến nghị đầu tư".
- **Hoàn thành khi:** người dùng chọn mã và xem được giá, tin, nhận định trong một màn hình.

### Giai đoạn 7 — Giám sát + hạ tầng như code (1–2 tuần)
- Prometheus metrics: số job thành công/thất bại, độ trễ API, dữ liệu thiếu.
- Grafana dashboard + cảnh báo (email/Telegram) khi pipeline lỗi hoặc dữ liệu cũ.
- Viết Terraform cho hạ tầng AWS (mục 6).
- **Hoàn thành khi:** cố ý làm hỏng một job và nhận được cảnh báo.

### Giai đoạn 8 — Deploy lên AWS (1–2 tuần)
- CD bằng GitHub Actions: build image → push ECR → cập nhật ECS service.
- Bật AWS Budgets, đặt ngưỡng cảnh báo chi phí.
- **Hoàn thành khi:** truy cập được dashboard qua URL công khai (hoặc VPN riêng), job hằng ngày chạy tự động.

## 6. Kế hoạch deploy AWS

| Thành phần | Dịch vụ | Ghi chú |
|------------|---------|---------|
| Container app/API | ECS Fargate (hoặc App Runner) | Bắt đầu với 1 service nhỏ |
| Job hằng ngày | EventBridge + ECS task / Lambda | Lambda nếu job ngắn |
| Dữ liệu thô, model | S3 | Bật versioning |
| Dữ liệu chuẩn hóa | RDS PostgreSQL (db.t4g.micro) | Nhớ tắt khi không dùng nếu dev |
| Train model | SageMaker hoặc EC2 (spot) | Chỉ khi cần GPU; ưu tiên train local trước |
| Secrets | AWS Secrets Manager / SSM Parameter Store | Không commit key vào repo |
| Registry | ECR | |

**Quản lý chi phí:** bật AWS Budgets, gắn tag theo dự án, tắt tài nguyên không dùng, kiểm tra giá bằng AWS Pricing Calculator trước khi tạo. Nếu muốn rẻ hơn lúc đầu: Render/Railway/Fly.io cho app, Hugging Face Spaces cho demo model.

## 7. Chiến lược kiểm thử

- **Unit test:** provider (mock dữ liệu), tính chỉ báo, gắn tin vào mã.
- **Integration test:** DB + ingestion job bằng Docker Compose.
- **Kiểm tra dữ liệu:** không có ngày thiếu bất thường, không có giá âm/0, không trùng bản ghi.
- **Kiểm tra mô hình:** walk-forward, so baseline, kiểm tra data leakage.

## 8. Rủi ro và cách giảm

| Rủi ro | Giảm thiểu |
|--------|-----------|
| Nguồn dữ liệu miễn phí đổi API / bị chặn | Lớp provider, lưu dữ liệu thô, có nguồn dự phòng |
| Rate limit (429) | Retry + backoff, cache, chạy theo lô |
| Mô hình overfit, kết quả ảo | Walk-forward, baseline, tính phí giao dịch |
| Điều khoản sử dụng dữ liệu/tin tức | Kiểm tra từng nguồn, chỉ dùng cho mục đích cá nhân/học tập |
| Chi phí cloud vượt dự kiến | AWS Budgets, tắt tài nguyên, dùng free tier cẩn thận |
| Lộ API key | Secrets Manager, `.env` trong `.gitignore`, quét secret trong CI |
| Người dùng hiểu nhầm là lời khuyên đầu tư | Cảnh báo rõ ràng trên giao diện, không dùng ngôn ngữ "nên mua/bán" |

## 9. Quyết định cần chốt

Đã chốt: **thị trường ban đầu = Việt Nam** (2026-11-10). Giai đoạn 0 đã dựng khung; giai đoạn 1 đã có
`PriceProvider`, chuẩn hóa dữ liệu, lưu SQLite idempotent, CLI và test. **Vướng:** gói `vnstock` hiện
không cài được từ PyPI (xem README), nên chưa lấy được dữ liệu thật.

1. ~~Thị trường ban đầu: VN, Mỹ hay cả hai?~~ → Việt Nam
2. Số mã trong watchlist đầu tiên và khung thời gian dự đoán (ví dụ 1 ngày, 5 ngày)?
3. Nguồn tin tức cụ thể (cần kiểm tra điều khoản sử dụng).
4. Dashboard: Streamlit (nhanh) hay web app riêng (Next.js)?
5. Ngân sách AWS tối đa mỗi tháng?

## 10. Bước tiếp theo ngay

1. Chốt các quyết định ở mục 9.
2. Khởi tạo repo và cấu trúc thư mục (Giai đoạn 0).
3. Viết `PriceProvider` cho vnstock/yfinance và lấy thử dữ liệu 5 mã (Giai đoạn 1).
