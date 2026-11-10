import pytest

from stockwatch.core.errors import NotFoundError
from stockwatch.domain.models import PriceRange
from stockwatch.providers.demo import DemoProvider
from stockwatch.repositories.memory import MemoryPriceRepository
from stockwatch.services.market import MarketService


@pytest.fixture()
def service(sql_repo, make_prices):
    sql_repo.upsert(make_prices("VCB", 120), "demo")
    sql_repo.upsert(make_prices("FPT", 5, start_close=50), "demo")
    return MarketService(sql_repo)


def test_health(service):
    h = service.health()
    assert (h.status, h.tickers, h.sources) == ("ok", 2, ["demo"])


def test_list_tickers_summary(service):
    data = {t.ticker: t for t in service.list_tickers()}
    fpt = data["FPT"]
    assert fpt.close == 54 and fpt.change == 1
    assert fpt.change_pct == pytest.approx(1 / 53 * 100)
    assert len(fpt.spark) == 5


def test_range_cuts_history_but_ma_valid_from_start(service):
    candles = service.get_prices("vcb", PriceRange.M1).candles
    assert 15 <= len(candles) <= 25
    assert candles[0].ma20 is not None and candles[0].ma50 is not None


def test_all_range_has_none_ma_until_enough_data(service):
    candles = service.get_prices("VCB", PriceRange.ALL).candles
    assert len(candles) == 120
    assert candles[0].ma20 is None and candles[19].ma20 is not None
    assert candles[48].ma50 is None and candles[49].ma50 is not None


def test_unknown_ticker(service):
    with pytest.raises(NotFoundError):
        service.get_prices("XXX")


def test_memory_repository_serves_provider_data_without_database():
    repo = MemoryPriceRepository(DemoProvider(), ["VCB", "FPT"], "2024-01-01")
    svc = MarketService(repo)
    assert svc.health().sources == ["demo"]
    assert {t.ticker for t in svc.list_tickers()} == {"FPT", "VCB"}
    assert repo.prices("NOPE").empty
