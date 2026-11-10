"""Schema phản hồi của API (hợp đồng với frontend). Tách biệt với mô hình nghiệp vụ."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from stockwatch.domain.models import PriceRange


class _Out(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class HealthOut(_Out):
    status: str
    tickers: int
    sources: list[str]


class TickerOut(_Out):
    ticker: str
    source: str
    date: str
    close: float
    change: float | None
    change_pct: float | None
    volume: float
    spark: list[float]


class CandleOut(_Out):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    ma20: float | None
    ma50: float | None


class PricesOut(_Out):
    ticker: str
    source: str
    range: PriceRange
    candles: list[CandleOut]
