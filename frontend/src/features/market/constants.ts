import type { Range } from "./types";

export const RANGES: { key: Range; label: string }[] = [
  { key: "1M", label: "1T" },
  { key: "3M", label: "3T" },
  { key: "6M", label: "6T" },
  { key: "1Y", label: "1N" },
  { key: "ALL", label: "Tất cả" },
];

export const DEFAULT_RANGE: Range = "6M";

// Màu đường MA, dùng chung cho biểu đồ và chú giải
export const MA_COLORS = { ma20: "#f0b90b", ma50: "#c084fc" } as const;
