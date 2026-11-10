"""Repository trong bộ nhớ: lấy giá từ provider khi cần, KHÔNG ghi ra đĩa hay database."""

from __future__ import annotations

import threading

import pandas as pd

from stockwatch.domain.models import BAR_COLUMNS
from stockwatch.domain.ports import PriceProvider


class MemoryPriceRepository:
    def __init__(self, provider: PriceProvider, tickers: list[str], start: str):
        self._provider = provider
        self._tickers = [t.upper() for t in tickers]
        self._start = start
        self._cache: dict[str, pd.DataFrame] = {}
        self._lock = threading.Lock()

    def tickers(self) -> list[str]:
        return sorted(self._tickers)

    def prices(self, ticker: str) -> pd.DataFrame:
        t = ticker.upper()
        if t not in self._tickers:
            return pd.DataFrame(columns=BAR_COLUMNS)
        with self._lock:
            if t not in self._cache:
                df = self._provider.fetch_daily(t, self._start)
                self._cache[t] = df.drop(columns=["ticker"]).reset_index(drop=True)
            return self._cache[t].copy()

    def source(self, ticker: str) -> str:
        return self._provider.name
