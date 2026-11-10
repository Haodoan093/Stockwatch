"""Chuẩn hóa dữ liệu giá thô từ bất kỳ nguồn nào về định dạng chuẩn của hệ thống."""

from __future__ import annotations

import pandas as pd

from stockwatch.domain.models import PRICE_COLUMNS


def normalize_prices(raw: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Chuẩn hóa tên cột, kiểu dữ liệu; bỏ dòng hỏng và ngày trùng; thêm cột ticker."""
    if raw is None or raw.empty:
        return pd.DataFrame(columns=PRICE_COLUMNS)

    df = raw.rename(columns=lambda c: str(c).strip().lower()).copy()
    if "time" in df.columns and "date" not in df.columns:
        df = df.rename(columns={"time": "date"})

    missing = {"date", "open", "high", "low", "close", "volume"} - set(df.columns)
    if missing:
        raise ValueError(f"Dữ liệu thiếu cột: {sorted(missing)}")

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    for col in ("open", "high", "low", "close", "volume"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["date", "open", "high", "low", "close"])
    # Giá <= 0 là dữ liệu hỏng
    df = df[(df[["open", "high", "low", "close"]] > 0).all(axis=1)]
    df["volume"] = df["volume"].fillna(0)
    df["ticker"] = ticker.upper()
    df = df.drop_duplicates(subset=["ticker", "date"], keep="last").sort_values("date")
    return df[PRICE_COLUMNS].reset_index(drop=True)
