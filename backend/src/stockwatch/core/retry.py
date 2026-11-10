"""Thử lại với backoff lũy thừa cho các lệnh gọi mạng tới nguồn bên thứ ba."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import TypeVar

log = logging.getLogger(__name__)

T = TypeVar("T")


def retry(
    fn: Callable[[], T],
    attempts: int = 4,
    base_delay: float = 2.0,
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Gọi fn, thử lại khi lỗi (rate limit, mạng...) với độ trễ base_delay * 2**lần_thử."""
    for i in range(attempts):
        try:
            return fn()
        except Exception as exc:
            if i == attempts - 1:
                raise
            delay = base_delay * (2**i)
            log.warning("Lỗi %s, thử lại sau %.1fs (lần %d/%d)", exc, delay, i + 1, attempts)
            sleep(delay)
    raise RuntimeError("unreachable")
