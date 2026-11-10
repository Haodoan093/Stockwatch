type Props = { sources: string[] };

const NAV = [
  { label: "Thị trường", active: true },
  { label: "Danh mục", active: false },
  { label: "Tin tức", active: false },
  { label: "Nhận định AI", active: false },
];

export default function TopBar({ sources }: Props) {
  const demo = sources.includes("demo");
  return (
    <div className="flex flex-wrap items-center gap-x-6 gap-y-2 border-b border-line bg-panel px-4 py-2.5">
      <div className="flex items-center gap-2">
        <div className="grid h-7 w-7 place-items-center rounded-md bg-accent text-sm font-bold">S</div>
        <span className="text-base font-semibold tracking-tight">StockWatch</span>
      </div>
      <nav aria-label="Điều hướng chính" className="flex gap-1 text-sm">
        {NAV.map((n) => (
          <span
            key={n.label}
            aria-current={n.active ? "page" : undefined}
            title={n.active ? undefined : "Sắp có"}
            className={`rounded-md px-3 py-1.5 ${
              n.active ? "bg-panel2 font-medium text-ink" : "cursor-not-allowed text-mute/60"
            }`}
          >
            {n.label}
          </span>
        ))}
      </nav>
      <div className="ml-auto flex items-center gap-2 text-xs">
        {demo ? (
          <span
            role="status"
            className="rounded-md border border-warn/40 bg-warn/10 px-2.5 py-1 font-medium text-warn"
          >
            Dữ liệu demo — không phải giá thị trường
          </span>
        ) : (
          sources.length > 0 && <span className="text-mute">Nguồn: {sources.join(", ")}</span>
        )}
      </div>
    </div>
  );
}
