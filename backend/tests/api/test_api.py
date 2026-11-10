import pytest
from fastapi.testclient import TestClient

from stockwatch.api.app import create_app
from stockwatch.core.settings import Settings
from stockwatch.services.market import MarketService


@pytest.fixture()
def client(sql_repo, make_prices):
    sql_repo.upsert(make_prices("VCB", 120), "demo")
    sql_repo.upsert(make_prices("FPT", 5, start_close=50), "demo")
    return TestClient(create_app(service=MarketService(sql_repo), settings=Settings()))


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "tickers": 2, "sources": ["demo"]}


def test_tickers_contract(client):
    rows = {t["ticker"]: t for t in client.get("/api/tickers").json()}
    assert set(rows) == {"FPT", "VCB"}
    assert set(rows["FPT"]) == {
        "ticker", "source", "date", "close", "change", "change_pct", "volume", "spark"
    }
    assert rows["FPT"]["source"] == "demo"


def test_prices_contract(client):
    body = client.get("/api/prices/vcb?range=1M").json()
    assert body["ticker"] == "VCB" and body["range"] == "1M" and body["source"] == "demo"
    candle = body["candles"][0]
    assert set(candle) == {"date", "open", "high", "low", "close", "volume", "ma20", "ma50"}
    assert candle["ma20"] is not None


def test_prices_all_has_null_ma_at_start(client):
    candles = client.get("/api/prices/VCB?range=ALL").json()["candles"]
    assert candles[0]["ma20"] is None


def test_default_range_is_6m(client):
    assert client.get("/api/prices/VCB").json()["range"] == "6M"


def test_unknown_ticker_404(client):
    r = client.get("/api/prices/XXX")
    assert r.status_code == 404 and "XXX" in r.json()["detail"]


def test_bad_range_422(client):
    assert client.get("/api/prices/VCB?range=5Y").status_code == 422


def test_app_builds_from_settings_with_demo_memory(tmp_path):
    wl = tmp_path / "w.toml"
    wl.write_text('tickers = ["VCB"]\nstart_date = "2024-01-01"\n', encoding="utf-8")
    c = TestClient(create_app(settings=Settings(watchlist_path=wl)))
    assert c.get("/api/health").json()["sources"] == ["demo"]
    assert len(c.get("/api/prices/VCB?range=3M").json()["candles"]) > 30
