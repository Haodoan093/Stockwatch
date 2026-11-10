# Frontend — stockwatch web (React + Vite + TypeScript + Tailwind)

Độc lập hoàn toàn với `backend/`: chỉ gọi API qua HTTP. Cách chạy xem
[../HUONG_DAN_CHAY.md](../HUONG_DAN_CHAY.md).

## Cấu trúc theo tính năng

```
src/
├── main.tsx            Điểm vào
├── app/                Khung ứng dụng: App.tsx, layout/TopBar.tsx
├── features/
│   ├── market/         Danh sách theo dõi, biểu đồ nến, thông tin mã
│   │   ├── api.ts, types.ts, constants.ts
│   │   ├── hooks/      useWatchlist, useCandles (tải dữ liệu, huỷ request cũ)
│   │   ├── components/ Watchlist, PriceChart, SymbolHeader, RangeSelector, Sparkline
│   │   └── MarketPage.tsx
│   └── insights/       Nhận định AI, tin tức (hiện là chỗ giữ chỗ)
├── shared/             Dùng chung: api/http.ts, config/env.ts, lib/format.ts, ui/Message.tsx
└── styles/index.css    Tailwind + bảng màu (design tokens)
```

Quy tắc:

- Mỗi `features/<tên>` tự chứa api, types, hooks, components và chỉ xuất ra ngoài qua `index.ts`.
- Feature không import lẫn nhau trừ qua `index.ts` công khai; `shared/` không import từ `features/`.
- Import bằng alias `@/` (trỏ tới `src/`).
- Hợp đồng dữ liệu với backend nằm ở `features/market/types.ts` (khớp `backend/.../api/schemas.py`).

## Cấu hình

Xem [.env.example](.env.example): `VITE_API_BASE_URL` (địa chỉ API khi deploy),
`VITE_PROXY_TARGET` (backend mà dev server proxy tới).
