function Soon({ title, hint, lines }: { title: string; hint: string; lines: number }) {
  return (
    <section className="rounded-lg border border-line bg-panel2 p-3">
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-semibold">{title}</h2>
        <span className="rounded bg-line px-1.5 py-0.5 text-[11px] text-mute">Sắp có</span>
      </div>
      <p className="mb-3 text-xs text-mute">{hint}</p>
      <div className="space-y-2" aria-hidden="true">
        {Array.from({ length: lines }).map((_, i) => (
          <div key={i} className="h-3 rounded bg-line/70" style={{ width: `${92 - i * 14}%` }} />
        ))}
      </div>
    </section>
  );
}

export default function InsightsPanel() {
  return (
    <aside
      className="grid min-h-0 gap-3 overflow-y-auto bg-panel p-3 lg:grid-cols-2 xl:flex xl:flex-1 xl:flex-col"
      aria-label="Phân tích"
    >
      <Soon
        title="Nhận định AI"
        hint="Tóm tắt tín hiệu từ biểu đồ và tin tức cho mã đang xem."
        lines={4}
      />
      <Soon
        title="Tin tức liên quan"
        hint="Tin theo mã kèm điểm cảm xúc và tóm tắt."
        lines={5}
      />
      <p className="text-[11px] leading-relaxed text-mute lg:col-span-2 xl:col-span-1 xl:mt-auto">
        Công cụ học tập, thử nghiệm. Nội dung không phải khuyến nghị đầu tư.
      </p>
    </aside>
  );
}
