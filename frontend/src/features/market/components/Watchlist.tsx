import { useMemo, useState } from "react";
import { fmtPct, fmtPrice, tone } from "@/shared/lib/format";
import type { TickerRow } from "../types";
import Sparkline from "./Sparkline";

type Props = {
  rows: TickerRow[];
  selected: string | null;
  onSelect: (ticker: string) => void;
  loading: boolean;
};

export default function Watchlist({ rows, selected, onSelect, loading }: Props) {
  const [q, setQ] = useState("");
  const filtered = useMemo(
    () => rows.filter((r) => r.ticker.includes(q.trim().toUpperCase())),
    [rows, q],
  );

  return (
    <section className="flex min-h-0 flex-col bg-panel" aria-label="Danh sách theo dõi">
      <div className="flex items-center justify-between px-4 pt-3 pb-2">
        <h2 className="text-sm font-semibold">Danh sách theo dõi</h2>
        <span className="text-xs text-mute">{rows.length} mã</span>
      </div>
      <div className="px-3 pb-2">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Tìm mã (VD: FPT)"
          aria-label="Tìm mã cổ phiếu"
          className="w-full rounded-md border border-line bg-panel2 px-3 py-1.5 text-sm outline-none placeholder:text-mute focus:border-accent"
        />
      </div>
      <div className="grid grid-cols-[1fr_auto_auto_72px] gap-x-3 px-4 pb-1 text-xs text-mute">
        <span>Mã</span>
        <span className="text-right">Giá</span>
        <span className="w-16 text-right">+/-%</span>
        <span className="text-right">30 phiên</span>
      </div>
      <ul className="min-h-0 flex-1 overflow-y-auto">
        {loading &&
          Array.from({ length: 8 }).map((_, i) => (
            <li key={i} className="mx-3 my-1 h-9 animate-pulse rounded bg-panel2" />
          ))}
        {!loading && filtered.length === 0 && (
          <li className="px-4 py-6 text-center text-sm text-mute">Không có mã phù hợp</li>
        )}
        {filtered.map((r) => {
          const active = r.ticker === selected;
          return (
            <li key={r.ticker}>
              <button
                type="button"
                onClick={() => onSelect(r.ticker)}
                aria-current={active ? "true" : undefined}
                className={`grid w-full grid-cols-[1fr_auto_auto_72px] items-center gap-x-3 border-l-2 px-4 py-2 text-left transition-colors hover:bg-panel2 ${
                  active ? "border-accent bg-panel2" : "border-transparent"
                }`}
              >
                <span className="text-sm font-semibold">{r.ticker}</span>
                <span className={`num text-right text-sm ${tone(r.change)}`}>
                  {fmtPrice(r.close)}
                </span>
                <span className={`num w-16 text-right text-sm ${tone(r.change_pct)}`}>
                  {fmtPct(r.change_pct)}
                </span>
                <span className="flex justify-end">
                  <Sparkline values={r.spark} />
                </span>
              </button>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
