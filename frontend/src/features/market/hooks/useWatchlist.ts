import { useCallback, useEffect, useState } from "react";
import { isAbort } from "@/shared/api/http";
import { marketApi } from "../api";
import type { TickerRow } from "../types";

export type WatchlistState = {
  rows: TickerRow[];
  sources: string[];
  loading: boolean;
  error: string | null;
  reload: () => void;
};

/** Tải danh sách mã và nguồn dữ liệu của backend. */
export function useWatchlist(): WatchlistState {
  const [rows, setRows] = useState<TickerRow[]>([]);
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [nonce, setNonce] = useState(0);

  useEffect(() => {
    const ctrl = new AbortController();
    setLoading(true);
    setError(null);
    Promise.all([marketApi.tickers(ctrl.signal), marketApi.health(ctrl.signal)])
      .then(([tickers, health]) => {
        setRows(tickers);
        setSources(health.sources);
      })
      .catch((e: unknown) => {
        if (!isAbort(e)) setError((e as Error).message);
      })
      .finally(() => {
        if (!ctrl.signal.aborted) setLoading(false);
      });
    return () => ctrl.abort();
  }, [nonce]);

  const reload = useCallback(() => setNonce((n) => n + 1), []);
  return { rows, sources, loading, error, reload };
}
