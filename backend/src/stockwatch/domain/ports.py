"""Các giao diện (port) mà tầng service/job phụ thuộc vào; hạ tầng cung cấp triển khai cụ thể."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

import pandas as pd


class PriceProvider(ABC):
    """Nguồn dữ liệu giá bên ngoài (vnstock, demo, API khác...)."""

    name: str = "unknown"

    @abstractmethod
    def fetch_daily(self, ticker: str, start: str, end: str | None = None) -> pd.DataFrame:
        """Giá ngày đã chuẩn hóa (cột PRICE_COLUMNS) từ start đến end (YYYY-MM-DD)."""


class PriceRepository(Protocol):
    """Đọc giá đã có. Cột trả về: date (YYYY-MM-DD), open, high, low, close, volume."""

    def tickers(self) -> list[str]: ...

    def prices(self, ticker: str) -> pd.DataFrame: ...

    def source(self, ticker: str) -> str: ...


class PriceSink(Protocol):
    """Ghi giá (dùng bởi job lấy dữ liệu)."""

    def last_date(self, ticker: str) -> str | None: ...

    def upsert(self, df: pd.DataFrame, source: str) -> int: ...
