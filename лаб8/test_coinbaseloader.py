import pytest
import pandas as pd
from dataloader.coinbaseloader import CoinbaseLoader, Granularity

@pytest.fixture
def loader():
    return CoinbaseLoader()

def test_get_pairs(loader):
    pairs = loader.get_pairs()
    assert isinstance(pairs, pd.DataFrame), "get_pairs повинен повертати DataFrame"
    assert not pairs.empty, "DataFrame не повинен бути порожнім"

@pytest.mark.parametrize("pair", ["BTC-USDT", "ETH-USDT"])
def test_get_stats(loader, pair):
    stats = loader.get_stats(pair)
    assert isinstance(stats, pd.DataFrame), "get_stats повинен повертати DataFrame"
    assert not stats.empty, "DataFrame не повинен бути порожнім"

@pytest.mark.parametrize("pair, begin, end, granularity", [("BTC-USDT", "2023-01-01", "2023-06-30", Granularity.ONE_DAY)])
def test_get_historical_data(loader, pair, begin, end, granularity):
    data = loader.get_historical_data(pair, begin, end, granularity)
    assert isinstance(data, pd.DataFrame), "get_historical_data повинен повертати DataFrame"
    assert not data.empty, "DataFrame не повинен бути порожнім"
