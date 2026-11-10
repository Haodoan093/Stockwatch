"""Nơi lắp ghép phụ thuộc (composition root): chọn triển khai cụ thể theo Settings."""

from __future__ import annotations

from stockwatch.core.settings import Settings
from stockwatch.core.watchlist import load_watchlist
from stockwatch.domain.ports import PriceRepository
from stockwatch.providers.factory import build_provider
from stockwatch.repositories.memory import MemoryPriceRepository
from stockwatch.repositories.sql import SqlPriceRepository, make_engine
from stockwatch.services.market import MarketService


def build_repository(settings: Settings) -> PriceRepository:
    if settings.repository == "db":
        return SqlPriceRepository(make_engine(settings.database_url))
    tickers, start = load_watchlist(settings.watchlist_path)
    return MemoryPriceRepository(build_provider(settings.provider), tickers, start)


def build_market_service(settings: Settings) -> MarketService:
    return MarketService(build_repository(settings))
