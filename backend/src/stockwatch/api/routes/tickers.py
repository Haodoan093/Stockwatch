from __future__ import annotations

from fastapi import APIRouter, Depends

from stockwatch.api.deps import get_market_service
from stockwatch.api.schemas import TickerOut
from stockwatch.services.market import MarketService

router = APIRouter(tags=["market"])


@router.get("/tickers", response_model=list[TickerOut])
def list_tickers(service: MarketService = Depends(get_market_service)) -> list[TickerOut]:
    return [TickerOut.model_validate(t) for t in service.list_tickers()]
