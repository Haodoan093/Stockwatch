// Hợp đồng dữ liệu với backend (xem backend/src/stockwatch/api/schemas.py)

export type Range = "1M" | "3M" | "6M" | "1Y" | "ALL";

export type TickerRow = {
  ticker: string;
  source: string;
  date: string;
  close: number;
  change: number | null;
  change_pct: number | null;
  volume: number;
  spark: number[];
};

export type Candle = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  ma20: number | null;
  ma50: number | null;
};

export type PricesResponse = {
  ticker: string;
  source: string;
  range: Range;
  candles: Candle[];
};

export type Health = { status: string; tickers: number; sources: string[] };
