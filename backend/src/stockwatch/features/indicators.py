"""Chỉ báo kỹ thuật cơ bản tính từ giá đóng cửa."""

from __future__ import annotations

import pandas as pd


def sma(close: pd.Series, window: int) -> pd.Series:
    """Trung bình động đơn giản; NaN cho các điểm chưa đủ dữ liệu."""
    return close.rolling(window=window, min_periods=window).mean()
