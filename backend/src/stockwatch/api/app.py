"""Khởi tạo ứng dụng FastAPI.

Chạy: uvicorn stockwatch.api.app:app_factory --factory --reload
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from stockwatch.api.errors import register_error_handlers
from stockwatch.api.routes import health, prices, tickers
from stockwatch.bootstrap import build_market_service
from stockwatch.core.settings import Settings
from stockwatch.services.market import MarketService


def create_app(service: MarketService | None = None, settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    app = FastAPI(title="stockwatch API", version="0.1.0")
    app.state.market_service = service or build_market_service(settings)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    register_error_handlers(app)
    for module in (health, tickers, prices):
        app.include_router(module.router, prefix="/api")
    return app


def app_factory() -> FastAPI:
    return create_app()
