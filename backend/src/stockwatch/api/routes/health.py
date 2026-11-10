from __future__ import annotations

from fastapi import APIRouter, Depends

from stockwatch.api.deps import get_market_service
from stockwatch.api.schemas import HealthOut
from stockwatch.services.market import MarketService

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthOut)
def health(service: MarketService = Depends(get_market_service)) -> HealthOut:
    return HealthOut.model_validate(service.health())
