"""Provider dữ liệu DEMO: chuỗi giá ngẫu nhiên có seed theo mã, KHÔNG phải dữ liệu thị trường thật.

Dùng để phát triển giao diện/pipeline khi chưa có nguồn thật. Dữ liệu được gắn source="demo"
và giao diện hiển thị nhãn "Dữ liệu demo".
"""

from __future__ import annotations

import zlib

import numpy as np
import pandas as pd

from stockwatch.domain.ports import PriceProvider
from stockwatch.providers.normalize import normalize_prices

# Biên độ dao động ngày của sàn HOSE là ±7%; giữ trong ±6.9% cho giống thực tế
MAX_DAILY_MOVE = 0.069


class DemoProvider(PriceProvider):
    name = "demo"

    def fetch_daily(self, ticker: str, start: str, end: str | None = None) -> pd.DataFrame:
        end = end or pd.Timestamp.today().strftime("%Y-%m-%d")
        dates = pd.bdate_range(start, end)
        if len(dates) == 0:
            return normalize_prices(pd.DataFrame(), ticker)

        # Seed theo mã (không theo ngày bắt đầu) để lấy lại một đoạn cho kết quả nhất quán
        seed = zlib.crc32(ticker.upper().encode())
        rng = np.random.default_rng(seed)
        base = 15 + (seed % 9000) / 100  # giá khởi điểm 15–105 (nghìn đồng)
        full = pd.bdate_range("2015-01-01", end)
        returns = np.clip(rng.normal(0.0001, 0.016, len(full)), -MAX_DAILY_MOVE, MAX_DAILY_MOVE)
        closes = base * np.exp(np.cumsum(returns))
        spread = np.abs(rng.normal(0, 0.008, len(full)))
        gaps = rng.normal(0, 0.006, len(full))
        volume = rng.lognormal(mean=13.5, sigma=0.5, size=len(full))

        df = pd.DataFrame({"time": full, "close": closes, "spread": spread, "gap": gaps})
        df["open"] = df["close"].shift(1).fillna(df["close"]) * (1 + df["gap"])
        df["high"] = df[["open", "close"]].max(axis=1) * (1 + df["spread"])
        df["low"] = df[["open", "close"]].min(axis=1) * (1 - df["spread"])
        df["volume"] = volume.round()
        df = df[df["time"].isin(dates)]
        for col in ("open", "high", "low", "close"):
            df[col] = df[col].round(2)
        return normalize_prices(df[["time", "open", "high", "low", "close", "volume"]], ticker)
