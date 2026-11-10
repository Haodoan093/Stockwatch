import { MA_COLORS, RANGES } from "../constants";
import type { Range } from "../types";

type Props = { value: Range; onChange: (r: Range) => void };

export default function RangeSelector({ value, onChange }: Props) {
  return (
    <div
      className="flex items-center gap-1 border-y border-line px-3 py-1.5"
      role="group"
      aria-label="Khoảng thời gian"
    >
      {RANGES.map((r) => (
        <button
          key={r.key}
          type="button"
          onClick={() => onChange(r.key)}
          aria-pressed={value === r.key}
          className={`rounded px-2.5 py-1 text-xs font-medium transition-colors ${
            value === r.key ? "bg-panel2 text-ink" : "text-mute hover:bg-panel2 hover:text-ink"
          }`}
        >
          {r.label}
        </button>
      ))}
      <span className="ml-auto flex items-center gap-3 pr-1 text-[11px] text-mute">
        {(["ma20", "ma50"] as const).map((k) => (
          <span key={k}>
            <i
              className="mr-1 inline-block h-0.5 w-3 align-middle"
              style={{ background: MA_COLORS[k] }}
            />
            {k.toUpperCase()}
          </span>
        ))}
      </span>
    </div>
  );
}
