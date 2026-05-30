import pandas as pd

from spotify_analytics.cleaner import SpotifyDataCleaner


def test_cleaner_creates_release_year_and_duration_min():
    raw = pd.DataFrame(
        {
            "track_name": ["Song"],
            "track_artist": ["Artist"],
            "track_popularity": ["80"],
            "track_album_release_date": ["2020-05-01"],
            "playlist_genre": ["pop"],
            "playlist_subgenre": ["dance pop"],
            "danceability": ["0.7"],
            "energy": ["0.8"],
            "valence": ["0.6"],
            "tempo": ["120"],
            "loudness": ["-5"],
            "acousticness": ["0.1"],
            "instrumentalness": ["0.0"],
            "speechiness": ["0.05"],
            "duration_ms": ["180000"],
        }
    )

    cleaned = SpotifyDataCleaner().clean(raw)

    assert cleaned.loc[0, "release_year"] == 2020
    assert cleaned.loc[0, "duration_min"] == 3
    assert cleaned.loc[0, "track_popularity"] == 80
