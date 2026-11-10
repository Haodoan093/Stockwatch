// Giá trong dữ liệu tính bằng nghìn đồng (VD 95.6 = 95.600đ)
const vn = "vi-VN";

export function fmtPrice(v: number | null | undefined): string {
  if (v == null) return "—";
  return (v * 1000).toLocaleString(vn, { maximumFractionDigits: 0 });
}

export function fmtChange(v: number | null | undefined): string {
  if (v == null) return "—";
  const s = (Math.abs(v) * 1000).toLocaleString(vn, { maximumFractionDigits: 0 });
  return `${v > 0 ? "+" : v < 0 ? "-" : ""}${s}`;
}

export function fmtPct(v: number | null | undefined): string {
  if (v == null) return "—";
  const s = Math.abs(v).toLocaleString(vn, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  return `${v > 0 ? "+" : v < 0 ? "-" : ""}${s}%`;
}

export function fmtVol(v: number | null | undefined): string {
  if (v == null) return "—";
  const f = (n: number) => n.toLocaleString(vn, { maximumFractionDigits: 1 });
  if (v >= 1e9) return `${f(v / 1e9)} Tỷ`;
  if (v >= 1e6) return `${f(v / 1e6)} Tr`;
  if (v >= 1e3) return `${f(v / 1e3)} N`;
  return f(v);
}

/** Lớp màu theo chiều biến động: xanh tăng, đỏ giảm, xám đứng giá */
export function tone(v: number | null | undefined): string {
  if (v == null || v === 0) return "text-mute";
  return v > 0 ? "text-up" : "text-down";
}

export function fmtDate(iso: string): string {
  const [y, m, d] = iso.split("-");
  return `${d}/${m}/${y}`;
}
