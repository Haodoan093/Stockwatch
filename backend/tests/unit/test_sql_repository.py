from stockwatch.repositories.sql import SqlPriceRepository, make_engine, normalize_url


def test_upsert_is_idempotent(sql_repo, make_prices):
    df = make_prices("VCB", 10)
    assert sql_repo.upsert(df, "demo") == 10
    assert sql_repo.upsert(df, "demo") == 10
    assert len(sql_repo.prices("VCB")) == 10
    assert sql_repo.last_date("VCB") == df["date"].iloc[-1]


def test_upsert_updates_existing_row(make_prices):
    repo = SqlPriceRepository(make_engine("sqlite:///:memory:"))
    df = make_prices("VCB", 1)
    repo.upsert(df, "demo")
    df["close"] = 1.8
    df["high"] = 2.0
    repo.upsert(df, "vnstock")
    loaded = repo.prices("VCB")
    assert len(loaded) == 1 and loaded["close"].iloc[0] == 1.8
    assert repo.source("VCB") == "vnstock"


def test_reads(sql_repo, make_prices):
    sql_repo.upsert(make_prices("VCB", 3), "demo")
    sql_repo.upsert(make_prices("FPT", 2), "demo")
    assert sql_repo.tickers() == ["FPT", "VCB"]
    assert sql_repo.last_date("XXX") is None
    assert sql_repo.prices("XXX").empty
    assert sql_repo.source("XXX") == "unknown"
    assert list(sql_repo.prices("VCB").columns) == [
        "date", "open", "high", "low", "close", "volume"
    ]


def test_normalize_url_for_postgres():
    assert normalize_url("postgres://u:p@h:5432/d") == "postgresql+psycopg://u:p@h:5432/d"
    assert normalize_url("postgresql://u:p@h/d") == "postgresql+psycopg://u:p@h/d"
    assert normalize_url("sqlite:///x.db") == "sqlite:///x.db"
