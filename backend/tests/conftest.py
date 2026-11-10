"""Fixture dùng chung cho mọi test."""

from __future__ import annotations

import pandas as pd
import pytest

from stockwatch.providers.normalize import normalize_prices
from stockwatch.repositories.sql import SqlPriceRepository, make_engine


@pytest.fixture()
def make_prices():
    """Tạo DataFrame giá chuẩn hóa: giá đóng cửa tăng dần 1 đơn vị mỗi phiên."""

    def _make(ticker: str, n: int, start_close: float = 100.0) -> pd.DataFrame:
        dates = pd.bdate_range("2024-01-01", periods=n)
        close = [start_close + i for i in range(n)]
        raw = pd.DataFrame(
            {
                "time": dates.strftime("%Y-%m-%d"),
                "open": close,
                "high": [c + 1 for c in close],
                "low": [c - 1 for c in close],
                "close": close,
                "volume": [1000 + i for i in range(n)],
            }
        )
        return normalize_prices(raw, ticker)

    return _make


@pytest.fixture()
def sql_repo(tmp_path) -> SqlPriceRepository:
    return SqlPriceRepository(make_engine(f"sqlite:///{tmp_path / 't.db'}"))
