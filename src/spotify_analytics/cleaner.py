import pandas as pd

from spotify_analytics.config import AUDIO_FEATURES, REQUIRED_COLUMNS


class SpotifyDataCleaner:
    """Prepares raw Spotify data for analysis."""

    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        cleaned = data.copy()
        cleaned = cleaned[REQUIRED_COLUMNS].drop_duplicates()

        numeric_columns = ["track_popularity", "duration_ms", *AUDIO_FEATURES]
        for column in numeric_columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

        cleaned["track_album_release_date"] = pd.to_datetime(
            cleaned["track_album_release_date"],
            errors="coerce",
            format="mixed",
        )
        cleaned["release_year"] = cleaned["track_album_release_date"].dt.year
        cleaned["duration_min"] = cleaned["duration_ms"] / 60000

        text_columns = [
            "track_name",
            "track_artist",
            "playlist_genre",
            "playlist_subgenre",
        ]
        for column in text_columns:
            cleaned[column] = cleaned[column].fillna("unknown").astype(str).str.strip()

        cleaned = cleaned.dropna(
            subset=[
                "track_popularity",
                "release_year",
                "duration_min",
                *AUDIO_FEATURES,
            ]
        )
        cleaned["release_year"] = cleaned["release_year"].astype(int)

        return cleaned.reset_index(drop=True)
