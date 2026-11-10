from pathlib import Path

import pytest

from stockwatch.core.settings import Settings


def test_defaults():
    s = Settings.from_env({})
    assert s.provider == "demo" and s.repository == "memory"
    assert "http://localhost:5173" in s.cors_origins


def test_from_env():
    s = Settings.from_env(
        {
            "STOCKWATCH_PROVIDER": "vnstock",
            "STOCKWATCH_REPOSITORY": "db",
            "DATABASE_URL": "postgresql://u:p@h/d",
            "STOCKWATCH_WATCHLIST": "x/w.toml",
            "STOCKWATCH_CORS_ORIGINS": "http://a.com, http://b.com",
        }
    )
    assert (s.provider, s.repository) == ("vnstock", "db")
    assert s.database_url == "postgresql://u:p@h/d"
    assert s.watchlist_path == Path("x/w.toml")
    assert s.cors_origins == ("http://a.com", "http://b.com")


@pytest.mark.parametrize(
    "env",
    [{"STOCKWATCH_PROVIDER": "nope"}, {"STOCKWATCH_REPOSITORY": "nope"}],
)
def test_invalid_values_rejected(env):
    with pytest.raises(ValueError):
        Settings.from_env(env)
