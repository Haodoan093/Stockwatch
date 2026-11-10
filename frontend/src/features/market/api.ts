import { getJson } from "@/shared/api/http";
import type { Health, PricesResponse, Range, TickerRow } from "./types";

export const marketApi = {
  health: (signal?: AbortSignal) => getJson<Health>("/api/health", signal),
  tickers: (signal?: AbortSignal) => getJson<TickerRow[]>("/api/tickers", signal),
  prices: (ticker: string, range: Range, signal?: AbortSignal) =>
    getJson<PricesResponse>(`/api/prices/${encodeURIComponent(ticker)}?range=${range}`, signal),
};
