import { useMemo, useState } from "react";
import { InsightsPanel } from "@/features/insights";
import Message from "@/shared/ui/Message";
import PriceChart from "./components/PriceChart";
import RangeSelector from "./components/RangeSelector";
import SymbolHeader from "./components/SymbolHeader";
import Watchlist from "./components/Watchlist";
import { DEFAULT_RANGE } from "./constants";
import { useCandles } from "./hooks/useCandles";
import type { WatchlistState } from "./hooks/useWatchlist";
import type { Range } from "./types";

type Props = { watchlist: WatchlistState };

export default function MarketPage({ watchlist }: Props) {
  const { rows, loading, error, reload } = watchlist;
  const [picked, setPicked] = useState<string | null>(null);
  const [range, setRange] = useState<Range>(DEFAULT_RANGE);

  // Mã đang xem: lựa chọn của người dùng, mặc định là mã đầu danh sách
  const selected = picked ?? rows[0]?.ticker ?? null;
  const row = useMemo(() => rows.find((r) => r.ticker === selected) ?? null, [rows, selected]);
  const { candles, loading: chartLoading, error: chartError } = useCandles(selected, range);
  const last = candles.length ? candles[candles.length - 1] : null;

  if (error) {
    return (
      <Message title="Không kết nối được máy chủ dữ liệu">
        <p className="mb-3">{error}. Hãy chắc chắn backend đang chạy (mặc định cổng 8000).</p>
        <button
          type="button"
          onClick={reload}
          className="rounded-md bg-accent px-3 py-1.5 text-sm font-medium text-white hover:opacity-90"
        >
          Thử lại
        </button>
      </Message>
    );
  }
  if (!loading && rows.length === 0) {
    return (
      <Message title="Chưa có dữ liệu">
        Kiểm tra <code className="text-ink">backend/config/watchlist.toml</code> và nguồn dữ liệu
        của backend.
      </Message>
    );
  }

  return (
    <main className="grid min-h-0 flex-1 gap-px bg-line lg:grid-cols-[320px_minmax(0,1fr)] lg:grid-rows-[minmax(0,1fr)_auto] xl:grid-cols-[320px_minmax(0,1fr)_300px] xl:grid-rows-1">
      <div className="order-2 flex min-h-[320px] flex-col lg:order-1 lg:min-h-0">
        <Watchlist rows={rows} selected={selected} onSelect={setPicked} loading={loading} />
      </div>

      <section className="order-1 flex min-h-0 flex-col overflow-hidden bg-panel lg:order-2">
        {row ? <SymbolHeader row={row} last={last} /> : <div className="h-[88px]" />}
        <RangeSelector value={range} onChange={setRange} />
        {chartError ? (
          <Message title="Không tải được biểu đồ">{chartError}</Message>
        ) : (
          <div className="relative flex min-h-[320px] flex-1 flex-col lg:min-h-0">
            <PriceChart candles={candles} />
            {chartLoading && (
              <div
                role="status"
                className="absolute inset-0 z-20 grid place-items-center bg-panel/60 text-sm text-mute"
              >
                Đang tải…
              </div>
            )}
          </div>
        )}
      </section>

      <div className="order-3 flex flex-col lg:col-span-2 xl:col-span-1 xl:min-h-0">
        <InsightsPanel />
      </div>
    </main>
  );
}
