from stockwatch.providers.demo import MAX_DAILY_MOVE, DemoProvider


def test_deterministic_and_labeled():
    p = DemoProvider()
    assert p.name == "demo"
    a = p.fetch_daily("VCB", "2024-01-01", "2024-06-30")
    b = p.fetch_daily("VCB", "2024-01-01", "2024-06-30")
    assert a.equals(b)
    assert not a.equals(p.fetch_daily("FPT", "2024-01-01", "2024-06-30"))


def test_ohlc_consistent_and_within_limits():
    df = DemoProvider().fetch_daily("HPG", "2023-01-01", "2024-12-31")
    assert len(df) > 400
    assert (df["high"] >= df[["open", "close"]].max(axis=1)).all()
    assert (df["low"] <= df[["open", "close"]].min(axis=1)).all()
    assert (df["volume"] > 0).all()
    moves = df["close"].pct_change().dropna().abs()
    assert moves.max() <= MAX_DAILY_MOVE + 1e-3


def test_subrange_matches_full_history():
    p = DemoProvider()
    full = p.fetch_daily("FPT", "2023-01-01", "2024-06-30").set_index("date")
    part = p.fetch_daily("FPT", "2024-03-01", "2024-06-30").set_index("date")
    assert full.loc[part.index, "close"].equals(part["close"])
