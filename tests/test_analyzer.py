import pandas as pd

from spotify_analytics.analyzer import SpotifyAnalyzer


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


def test_filter_tracks_by_genre_and_year_range():
    analyzer = SpotifyAnalyzer()

    result = analyzer.filter_tracks(
        sample_data(),
        genres=["pop"],
        year_range=(2020, 2021),
    )

    assert len(result) == 2
    assert set(result["playlist_genre"]) == {"pop"}


def test_top_tracks_are_sorted_by_popularity_descending():
    analyzer = SpotifyAnalyzer()

    result = analyzer.top_tracks(sample_data(), limit=2)

    assert result["track_popularity"].tolist() == [90, 70]


def test_genre_popularity_groups_rows():
    analyzer = SpotifyAnalyzer()

    result = analyzer.genre_popularity(sample_data())

    pop_row = result[result["playlist_genre"] == "pop"].iloc[0]
    assert pop_row["track_count"] == 2
    assert pop_row["average_popularity"] == 80
