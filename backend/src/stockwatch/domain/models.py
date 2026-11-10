"""Mô hình nghiệp vụ thuần túy, không phụ thuộc framework hay hạ tầng."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

# Cột chuẩn của dữ liệu giá ngày (mọi provider phải trả về đúng các cột này)
PRICE_COLUMNS = ["ticker", "date", "open", "high", "low", "close", "volume"]
BAR_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


class PriceRange(StrEnum):
    M1 = "1M"
    M3 = "3M"
    M6 = "6M"
    Y1 = "1Y"
    ALL = "ALL"

    @property
    def days(self) -> int | None:
        """Số ngày lịch của khoảng thời gian; None nghĩa là toàn bộ lịch sử."""
        return _RANGE_DAYS[self]


_RANGE_DAYS: dict[PriceRange, int | None] = {
    PriceRange.M1: 31,
    PriceRange.M3: 93,
    PriceRange.M6: 186,
    PriceRange.Y1: 366,
    PriceRange.ALL: None,
}


@dataclass(frozen=True)
class Candle:
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    ma20: float | None
    ma50: float | None


@dataclass(frozen=True)
class PriceSeries:
    ticker: str
    source: str
    range: PriceRange
    candles: list[Candle]


@dataclass(frozen=True)
class TickerSummary:
    ticker: str
    source: str
    date: str
    close: float
    change: float | None
    change_pct: float | None
    volume: float
    spark: list[float]


@dataclass(frozen=True)
class Health:
    status: str
    tickers: int
    sources: list[str]
