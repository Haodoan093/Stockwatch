import pandas as pd
import pytest

from stockwatch.domain.models import PRICE_COLUMNS
from stockwatch.providers.normalize import normalize_prices


def raw_frame():
    return pd.DataFrame(
        {
            "time": ["2024-01-03", "2024-01-02", "2024-01-02", "2024-01-04", "2024-01-05"],
            "open": [10, 9, 9.5, 11, -1],
            "high": [11, 10, 10.5, 12, 5],
            "low": [9, 8, 9, 10, 1],
            "close": [10.5, 9.5, 10, None, 3],
            "volume": [1000, 500, 600, 700, 800],
        }
    )


def test_columns_and_order():
    df = normalize_prices(raw_frame(), "vcb")
    assert list(df.columns) == PRICE_COLUMNS
    assert (df["ticker"] == "VCB").all()


def test_drops_bad_rows_and_duplicates():
    df = normalize_prices(raw_frame(), "VCB")
    # dòng close=None và dòng giá âm bị loại; ngày trùng giữ bản cuối
    assert list(df["date"]) == ["2024-01-02", "2024-01-03"]
    assert df.loc[df["date"] == "2024-01-02", "close"].iloc[0] == 10


def test_empty():
    df = normalize_prices(pd.DataFrame(), "VCB")
    assert df.empty and list(df.columns) == PRICE_COLUMNS


def test_missing_columns():
    with pytest.raises(ValueError):
        normalize_prices(pd.DataFrame({"time": ["2024-01-01"], "close": [1]}), "VCB")
