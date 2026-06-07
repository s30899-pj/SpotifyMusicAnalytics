import pandas as pd
import pytest

from spotify_analytics.facade import SpotifyAnalyticsFacade


def make_facade():
    return SpotifyAnalyticsFacade("data/spotify_songs.csv")


def test_run_strategy_dispatches_to_registered_strategy(sample_data):
    facade = make_facade()

    result = facade.run_strategy("genre_popularity", sample_data)

    assert isinstance(result, pd.DataFrame)
    assert "average_popularity" in result.columns


def test_run_strategy_rejects_unknown_name(sample_data):
    facade = make_facade()

    with pytest.raises(ValueError):
        facade.run_strategy("nieistniejaca", sample_data)


def test_all_strategies_return_dataframes(sample_data):
    facade = make_facade()
    data = sample_data

    for name in facade.strategies:
        assert isinstance(facade.run_strategy(name, data), pd.DataFrame)
