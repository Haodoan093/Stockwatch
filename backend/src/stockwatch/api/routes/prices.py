from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from stockwatch.api.deps import get_market_service
from stockwatch.api.schemas import PricesOut
from stockwatch.domain.models import PriceRange
from stockwatch.services.market import MarketService

router = APIRouter(tags=["market"])


@router.get("/prices/{ticker}", response_model=PricesOut)
def get_prices(
    ticker: str,
    range: PriceRange = Query(PriceRange.M6, description="Khoảng thời gian"),
    service: MarketService = Depends(get_market_service),
) -> PricesOut:
    return PricesOut.model_validate(service.get_prices(ticker, range))
