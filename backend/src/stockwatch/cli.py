"""CLI: python -m stockwatch.cli fetch [--provider demo|vnstock] [--tickers VCB,FPT]

Lấy giá và LƯU VÀO DATABASE (chưa dùng ở giai đoạn này; API mặc định đọc từ bộ nhớ).
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

from stockwatch.core.settings import Settings
from stockwatch.core.watchlist import DEFAULT_START, load_watchlist
from stockwatch.domain.ports import PriceProvider, PriceSink
from stockwatch.providers.factory import build_provider
from stockwatch.repositories.sql import SqlPriceRepository, make_engine

log = logging.getLogger("stockwatch")


def run_fetch(
    provider: PriceProvider, tickers: list[str], start: str, sink: PriceSink
) -> dict[str, int]:
    """Lấy giá cho từng mã (chỉ phần mới), ghi vào sink. Lỗi một mã không dừng cả job."""
    results: dict[str, int] = {}
    for ticker in tickers:
        since = sink.last_date(ticker)
        # lấy lại từ ngày cuối để cập nhật nến chưa chốt; upsert nên không bị trùng
        begin = since if since and since > start else start
        try:
            df = provider.fetch_daily(ticker, begin)
            results[ticker] = sink.upsert(df, provider.name)
            log.info("%s: %d dòng (từ %s)", ticker, results[ticker], begin)
        except Exception:
            log.exception("%s: lỗi khi lấy dữ liệu", ticker)
            results[ticker] = -1
    return results


def main(argv: list[str] | None = None) -> int:
    settings = Settings.from_env()
    parser = argparse.ArgumentParser(prog="stockwatch")
    sub = parser.add_subparsers(dest="command", required=True)
    f = sub.add_parser("fetch", help="Lấy giá ngày và lưu vào DB")
    f.add_argument("--provider", choices=["vnstock", "demo"], default="vnstock")
    f.add_argument("--tickers", help="Danh sách mã, cách nhau bằng dấu phẩy")
    f.add_argument("--start", help="Ngày bắt đầu YYYY-MM-DD")
    f.add_argument("--config", type=Path, default=settings.watchlist_path)
    f.add_argument("--database-url", default=settings.database_url)
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    tickers, start = load_watchlist(args.config) if args.config.exists() else ([], DEFAULT_START)
    if args.tickers:
        tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    start = args.start or start
    if not tickers:
        parser.error("Không có mã nào: truyền --tickers hoặc tạo config/watchlist.toml")
    pd.Timestamp(start)  # kiểm tra định dạng ngày sớm

    sink = SqlPriceRepository(make_engine(args.database_url))
    results = run_fetch(build_provider(args.provider), tickers, start, sink)
    failed = [t for t, n in results.items() if n < 0]
    print(f"Xong: {len(results) - len(failed)}/{len(results)} mã thành công")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
