import { fmtChange, fmtDate, fmtPct, fmtPrice, fmtVol, tone } from "@/shared/lib/format";
import type { Candle, TickerRow } from "../types";

type Props = { row: TickerRow; last: Candle | null };

function Stat({ label, value, className = "" }: { label: string; value: string; className?: string }) {
  return (
    <div className="min-w-[72px]">
      <dt className="text-xs text-mute">{label}</dt>
      <dd className={`num text-sm font-medium ${className}`}>{value}</dd>
    </div>
  );
}

export default function SymbolHeader({ row, last }: Props) {
  return (
    <header className="flex flex-wrap items-end gap-x-8 gap-y-3 px-4 py-3">
      <div>
        <h1 className="text-xl font-bold">{row.ticker}</h1>
        <p className="text-xs text-mute">Phiên {fmtDate(row.date)} · đơn vị: đồng</p>
      </div>
      <div>
        <div className={`num text-2xl font-semibold leading-none ${tone(row.change)}`}>
          {fmtPrice(row.close)}
        </div>
        <div className={`num mt-1 text-sm ${tone(row.change)}`}>
          {fmtChange(row.change)} ({fmtPct(row.change_pct)})
        </div>
      </div>
      <dl className="flex flex-wrap gap-x-6 gap-y-2">
        <Stat label="Mở cửa" value={fmtPrice(last?.open)} />
        <Stat label="Cao nhất" value={fmtPrice(last?.high)} className="text-up" />
        <Stat label="Thấp nhất" value={fmtPrice(last?.low)} className="text-down" />
        <Stat label="Khối lượng" value={fmtVol(row.volume)} />
      </dl>
    </header>
  );
}
