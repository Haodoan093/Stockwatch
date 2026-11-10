"""Đọc danh sách mã theo dõi từ file TOML."""

from __future__ import annotations

import tomllib
from pathlib import Path

DEFAULT_START = "2023-01-01"


def load_watchlist(path: Path) -> tuple[list[str], str]:
    """Trả về (danh sách mã viết hoa, ngày bắt đầu YYYY-MM-DD)."""
    with path.open("rb") as f:
        cfg = tomllib.load(f)
    return [t.upper() for t in cfg["tickers"]], cfg.get("start_date", DEFAULT_START)
