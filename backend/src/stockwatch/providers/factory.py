from __future__ import annotations

from stockwatch.domain.ports import PriceProvider
from stockwatch.providers.demo import DemoProvider
from stockwatch.providers.vnstock import VnstockProvider


def build_provider(name: str) -> PriceProvider:
    """Tạo provider theo tên (demo | vnstock). Thêm nguồn mới: đăng ký tại đây."""
    if name == "demo":
        return DemoProvider()
    if name == "vnstock":
        return VnstockProvider()
    raise ValueError(f"Provider không hợp lệ: {name!r}")
