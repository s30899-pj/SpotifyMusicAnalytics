import pandas as pd
import pytest


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "track_name": ["A", "B", "C"],
            "track_artist": ["X", "Y", "X"],
            "track_popularity": [90, 40, 70],
            "playlist_genre": ["pop", "rock", "pop"],
            "playlist_subgenre": ["dance pop", "alt rock", "dance pop"],
            "release_year": [2020, 2019, 2021],
            "danceability": [0.8, 0.4, 0.7],
            "energy": [0.9, 0.6, 0.7],
            "valence": [0.7, 0.3, 0.8],
            "tempo": [120, 100, 130],
            "loudness": [-4, -8, -5],
            "acousticness": [0.1, 0.3, 0.2],
            "instrumentalness": [0.0, 0.1, 0.0],
            "speechiness": [0.05, 0.04, 0.03],
        }
    )
