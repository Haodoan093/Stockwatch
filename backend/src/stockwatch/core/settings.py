"""Cấu hình ứng dụng, đọc từ biến môi trường (xem ../.env.example ở thư mục gốc)."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

PROVIDERS = ("demo", "vnstock")
REPOSITORIES = ("memory", "db")


@dataclass(frozen=True)
class Settings:
    provider: str = "demo"
    repository: str = "memory"
    database_url: str = "sqlite:///data/stock.db"
    watchlist_path: Path = Path("config/watchlist.toml")
    cors_origins: tuple[str, ...] = ("http://localhost:5173", "http://127.0.0.1:5173")

    def __post_init__(self) -> None:
        if self.provider not in PROVIDERS:
            raise ValueError(f"STOCKWATCH_PROVIDER phải thuộc {PROVIDERS}, nhận {self.provider!r}")
        if self.repository not in REPOSITORIES:
            raise ValueError(
                f"STOCKWATCH_REPOSITORY phải thuộc {REPOSITORIES}, nhận {self.repository!r}"
            )

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Settings:
        env = os.environ if env is None else env
        default = cls()
        origins = env.get("STOCKWATCH_CORS_ORIGINS")
        return cls(
            provider=env.get("STOCKWATCH_PROVIDER", default.provider),
            repository=env.get("STOCKWATCH_REPOSITORY", default.repository),
            database_url=env.get("DATABASE_URL", default.database_url),
            watchlist_path=Path(env.get("STOCKWATCH_WATCHLIST", str(default.watchlist_path))),
            cors_origins=(
                tuple(o.strip() for o in origins.split(",") if o.strip())
                if origins
                else default.cors_origins
            ),
        )
