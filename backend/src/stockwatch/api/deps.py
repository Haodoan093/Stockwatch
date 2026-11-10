from __future__ import annotations

from fastapi import Request

from stockwatch.services.market import MarketService


def get_market_service(request: Request) -> MarketService:
    return request.app.state.market_service  # type: ignore[no-any-return]
