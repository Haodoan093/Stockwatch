"""Nghiệp vụ thị trường: tổng hợp danh sách mã và chuỗi giá kèm chỉ báo.

Service chỉ phụ thuộc vào giao diện PriceRepository, không biết dữ liệu đến từ đâu.
"""

from __future__ import annotations

import pandas as pd

from stockwatch.core.errors import NotFoundError
from stockwatch.domain.models import Candle, Health, PriceRange, PriceSeries, TickerSummary
from stockwatch.domain.ports import PriceRepository
from stockwatch.features.indicators import sma

SPARK_POINTS = 30


def _num(value: object) -> float | None:
    """NaN -> None để JSON hợp lệ."""
    return None if value is None or pd.isna(value) else float(value)  # type: ignore[arg-type]


class MarketService:
    def __init__(self, repository: PriceRepository):
        self._repo = repository

    def health(self) -> Health:
        names = self._repo.tickers()
        return Health(
            status="ok",
            tickers=len(names),
            sources=sorted({self._repo.source(t) for t in names}),
        )

    def list_tickers(self) -> list[TickerSummary]:
        out: list[TickerSummary] = []
        for ticker in self._repo.tickers():
            df = self._repo.prices(ticker)
            if df.empty:
                continue
            last = df.iloc[-1]
            prev_close = float(df["close"].iloc[-2]) if len(df) > 1 else None
            change = None if prev_close is None else float(last["close"]) - prev_close
            out.append(
                TickerSummary(
                    ticker=ticker,
                    source=self._repo.source(ticker),
                    date=str(last["date"]),
                    close=float(last["close"]),
                    change=change,
                    change_pct=None if change is None else change / prev_close * 100,
                    volume=float(last["volume"]),
                    spark=[float(x) for x in df["close"].tail(SPARK_POINTS)],
                )
            )
        return out

    def get_prices(self, ticker: str, price_range: PriceRange = PriceRange.M6) -> PriceSeries:
        df = self._repo.prices(ticker)
        if df.empty:
            raise NotFoundError(f"Không có dữ liệu cho {ticker.upper()}")

        # Tính MA trên toàn bộ lịch sử rồi mới cắt, để MA hợp lệ ngay từ đầu khoảng chọn
        df = df.copy()
        df["ma20"] = sma(df["close"], 20)
        df["ma50"] = sma(df["close"], 50)
        days = price_range.days
        if days is not None:
            cutoff = (pd.to_datetime(df["date"].iloc[-1]) - pd.Timedelta(days=days)).strftime(
                "%Y-%m-%d"
            )
            df = df[df["date"] >= cutoff]

        candles = [
            Candle(
                date=str(r.date),
                open=float(r.open),
                high=float(r.high),
                low=float(r.low),
                close=float(r.close),
                volume=float(r.volume),
                ma20=_num(r.ma20),
                ma50=_num(r.ma50),
            )
            for r in df.itertuples(index=False)
        ]
        return PriceSeries(
            ticker=ticker.upper(),
            source=self._repo.source(ticker),
            range=price_range,
            candles=candles,
        )
