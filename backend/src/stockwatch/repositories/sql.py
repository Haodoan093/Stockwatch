"""Repository SQLAlchemy: chạy trên SQLite (dev/test) và PostgreSQL (Docker, Supabase, RDS).

Chọn DB bằng DATABASE_URL, ví dụ:
    sqlite:///data/stock.db
    postgresql://stockwatch:stockwatch@localhost:5432/stockwatch
Ghi dữ liệu là upsert nên chạy lại không bị trùng.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pandas as pd
from sqlalchemy import (
    Column,
    Date,
    Engine,
    Float,
    MetaData,
    String,
    Table,
    create_engine,
    func,
    select,
)
from sqlalchemy.pool import StaticPool

from stockwatch.domain.models import BAR_COLUMNS

VALUE_COLUMNS = ("open", "high", "low", "close", "volume")

metadata = MetaData()
prices_table = Table(
    "prices",
    metadata,
    Column("ticker", String(16), primary_key=True),
    Column("date", Date, primary_key=True),
    Column("open", Float, nullable=False),
    Column("high", Float, nullable=False),
    Column("low", Float, nullable=False),
    Column("close", Float, nullable=False),
    Column("volume", Float, nullable=False),
    # Nguồn dữ liệu ("vnstock", "demo"...) để giao diện luôn nói rõ dữ liệu là thật hay demo
    Column("source", String(16), nullable=False, server_default="unknown"),
)


def normalize_url(url: str) -> str:
    """Nhà cung cấp (Supabase...) hay đưa 'postgresql://'; SQLAlchemy cần chỉ rõ driver psycopg 3."""
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix) :]
    return url


def make_engine(url: str) -> Engine:
    """Tạo engine và đảm bảo bảng tồn tại (idempotent). Sau này thay bằng migration (Alembic)."""
    url = normalize_url(url)
    kwargs: dict = {}
    if url.startswith("sqlite"):
        if ":memory:" in url or url == "sqlite://":
            kwargs = {"connect_args": {"check_same_thread": False}, "poolclass": StaticPool}
        else:
            path = url.removeprefix("sqlite:///")
            if path:
                Path(path).parent.mkdir(parents=True, exist_ok=True)
    else:
        kwargs = {"pool_pre_ping": True}
    engine = create_engine(url, **kwargs)
    metadata.create_all(engine)
    return engine


def _insert(engine: Engine):
    name = engine.dialect.name
    if name == "postgresql":
        from sqlalchemy.dialects.postgresql import insert
    elif name == "sqlite":
        from sqlalchemy.dialects.sqlite import insert
    else:
        raise NotImplementedError(f"Chưa hỗ trợ upsert cho {name}")
    return insert


class SqlPriceRepository:
    """Triển khai cả PriceRepository (đọc) và PriceSink (ghi)."""

    def __init__(self, engine: Engine):
        self._engine = engine

    # --- đọc (PriceRepository) ---
    def tickers(self) -> list[str]:
        stmt = select(prices_table.c.ticker).distinct().order_by("ticker")
        with self._engine.connect() as conn:
            return [r[0] for r in conn.execute(stmt)]

    def prices(self, ticker: str) -> pd.DataFrame:
        stmt = (
            select(prices_table.c.date, *[prices_table.c[c] for c in VALUE_COLUMNS])
            .where(prices_table.c.ticker == ticker.upper())
            .order_by(prices_table.c.date)
        )
        with self._engine.connect() as conn:
            rows = conn.execute(stmt).all()
        df = pd.DataFrame(rows, columns=BAR_COLUMNS)
        df["date"] = df["date"].map(lambda d: d.isoformat())
        return df

    def source(self, ticker: str) -> str:
        stmt = select(func.max(prices_table.c.source)).where(
            prices_table.c.ticker == ticker.upper()
        )
        with self._engine.connect() as conn:
            return conn.execute(stmt).scalar() or "unknown"

    # --- ghi (PriceSink) ---
    def last_date(self, ticker: str) -> str | None:
        stmt = select(func.max(prices_table.c.date)).where(
            prices_table.c.ticker == ticker.upper()
        )
        with self._engine.connect() as conn:
            value = conn.execute(stmt).scalar()
        return value.isoformat() if value else None

    def upsert(self, df: pd.DataFrame, source: str) -> int:
        if df.empty:
            return 0
        rows = [
            {
                "ticker": r.ticker,
                "date": dt.date.fromisoformat(r.date),
                "source": source,
                **{c: float(getattr(r, c)) for c in VALUE_COLUMNS},
            }
            for r in df.itertuples(index=False)
        ]
        stmt = _insert(self._engine)(prices_table)
        stmt = stmt.on_conflict_do_update(
            index_elements=["ticker", "date"],
            set_={c: stmt.excluded[c] for c in (*VALUE_COLUMNS, "source")},
        )
        with self._engine.begin() as conn:
            conn.execute(stmt, rows)
        return len(rows)
