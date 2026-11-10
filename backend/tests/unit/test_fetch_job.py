import pandas as pd

from stockwatch.cli import run_fetch
from stockwatch.domain.ports import PriceProvider
from stockwatch.providers.normalize import normalize_prices


class FakeProvider(PriceProvider):
    name = "fake"

    def __init__(self, fail_for=()):
        self.fail_for = set(fail_for)
        self.calls = []

    def fetch_daily(self, ticker, start, end=None):
        self.calls.append((ticker, start))
        if ticker in self.fail_for:
            raise RuntimeError("boom")
        raw = pd.DataFrame(
            {
                "time": ["2024-01-02", "2024-01-03"],
                "open": [10, 11],
                "high": [11, 12],
                "low": [9, 10],
                "close": [10.5, 11.5],
                "volume": [100, 200],
            }
        )
        return normalize_prices(raw, ticker)


def test_rerun_does_not_duplicate(sql_repo):
    run_fetch(FakeProvider(), ["VCB"], "2024-01-01", sql_repo)
    run_fetch(FakeProvider(), ["VCB"], "2024-01-01", sql_repo)
    assert len(sql_repo.prices("VCB")) == 2
    assert sql_repo.source("VCB") == "fake"


def test_second_run_only_requests_new_range(sql_repo):
    run_fetch(FakeProvider(), ["VCB"], "2024-01-01", sql_repo)
    p = FakeProvider()
    run_fetch(p, ["VCB"], "2024-01-01", sql_repo)
    assert p.calls == [("VCB", "2024-01-03")]


def test_one_failing_ticker_does_not_stop_job(sql_repo):
    res = run_fetch(FakeProvider(fail_for=["FPT"]), ["FPT", "VCB"], "2024-01-01", sql_repo)
    assert res == {"FPT": -1, "VCB": 2}
    assert len(sql_repo.prices("VCB")) == 2
