import pandas as pd
import pytest

from spotify_analytics.data_loader import DataLoadingError, SpotifyDataLoader


def test_loader_raises_error_when_required_column_is_missing(tmp_path):
    path = tmp_path / "broken.csv"
    pd.DataFrame({"track_name": ["Song"]}).to_csv(path, index=False)

    loader = SpotifyDataLoader(path)

    with pytest.raises(DataLoadingError):
        loader.load()
