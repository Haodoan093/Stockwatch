import pytest

from stockwatch.core.retry import retry


def test_succeeds_after_failures():
    calls = {"n": 0}
    delays = []

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("429")
        return "ok"

    assert retry(flaky, attempts=4, base_delay=1, sleep=delays.append) == "ok"
    assert delays == [1, 2]


def test_gives_up():
    def always_fail():
        raise RuntimeError("down")

    with pytest.raises(RuntimeError):
        retry(always_fail, attempts=2, base_delay=0, sleep=lambda _: None)
