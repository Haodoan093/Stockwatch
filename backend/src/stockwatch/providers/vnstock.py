"""Lấy giá cổ phiếu Việt Nam qua thư viện vnstock (nguồn bên thứ ba, không chính thức)."""

from __future__ import annotations

import pandas as pd

from stockwatch.core.retry import retry
from stockwatch.domain.ports import PriceProvider
from stockwatch.providers.normalize import normalize_prices


class VnstockProvider(PriceProvider):
    name = "vnstock"

    def __init__(self, source: str = "VCI", attempts: int = 4):
        self.source = source
        self.attempts = attempts

    def fetch_daily(self, ticker: str, start: str, end: str | None = None) -> pd.DataFrame:
        from vnstock import Vnstock  # import muộn để phần còn lại chạy được khi chưa cài vnstock

        end = end or pd.Timestamp.today().strftime("%Y-%m-%d")

        def _call() -> pd.DataFrame:
            stock = Vnstock().stock(symbol=ticker.upper(), source=self.source)
            return stock.quote.history(start=start, end=end, interval="1D")

        raw = retry(_call, attempts=self.attempts)
        return normalize_prices(raw, ticker)
