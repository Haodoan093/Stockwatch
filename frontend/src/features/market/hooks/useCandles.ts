import { useEffect, useState } from "react";
import { isAbort } from "@/shared/api/http";
import { marketApi } from "../api";
import type { Candle, Range } from "../types";

/** Tải nến của một mã theo khoảng thời gian; tự huỷ request cũ khi đổi tham số. */
export function useCandles(ticker: string | null, range: Range) {
  const [candles, setCandles] = useState<Candle[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!ticker) return;
    const ctrl = new AbortController();
    setLoading(true);
    setError(null);
    marketApi
      .prices(ticker, range, ctrl.signal)
      .then((res) => setCandles(res.candles))
      .catch((e: unknown) => {
        if (!isAbort(e)) setError((e as Error).message);
      })
      .finally(() => {
        if (!ctrl.signal.aborted) setLoading(false);
      });
    return () => ctrl.abort();
  }, [ticker, range]);

  return { candles, loading, error };
}
