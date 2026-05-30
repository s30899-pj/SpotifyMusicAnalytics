from typing import Optional

import numpy as np
import pandas as pd

from spotify_analytics.config import AUDIO_FEATURES


class SpotifyAnalyzer:
    """Contains pure analytical operations used by the Streamlit interface."""

    def summary(self, data: pd.DataFrame) -> dict[str, float]:
        return {
            "tracks": int(len(data)),
            "artists": int(data["track_artist"].nunique()),
            "genres": int(data["playlist_genre"].nunique()),
            "average_popularity": float(data["track_popularity"].mean()),
        }

    def column_overview(self, data: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "column": data.columns,
                "type": [str(dtype) for dtype in data.dtypes],
            }
        )

    def missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        missing = data.isna().sum().sort_values(ascending=False)
        return missing.reset_index().rename(columns={"index": "column", 0: "missing"})

    def filter_tracks(
        self,
        data: pd.DataFrame,
        genres: Optional[list[str]] = None,
        subgenres: Optional[list[str]] = None,
        year_range: Optional[tuple[int, int]] = None,
        popularity_range: Optional[tuple[int, int]] = None,
    ) -> pd.DataFrame:
        filtered = data.copy()

        if genres:
            filtered = filtered[filtered["playlist_genre"].isin(genres)]
        if subgenres:
            filtered = filtered[filtered["playlist_subgenre"].isin(subgenres)]
        if year_range:
            filtered = filtered[
                filtered["release_year"].between(year_range[0], year_range[1])
            ]
        if popularity_range:
            filtered = filtered[
                filtered["track_popularity"].between(
                    popularity_range[0],
                    popularity_range[1],
                )
            ]

        return filtered.reset_index(drop=True)

    def top_tracks(self, data: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
        columns = [
            "track_name",
            "track_artist",
            "track_popularity",
            "playlist_genre",
            "release_year",
        ]
        return (
            data.sort_values("track_popularity", ascending=False)
            .loc[:, columns]
            .head(limit)
            .reset_index(drop=True)
        )

    def genre_popularity(self, data: pd.DataFrame) -> pd.DataFrame:
        return (
            data.groupby("playlist_genre", as_index=False)
            .agg(
                average_popularity=("track_popularity", "mean"),
                median_popularity=("track_popularity", "median"),
                track_count=("track_name", "count"),
                average_energy=("energy", "mean"),
                average_danceability=("danceability", "mean"),
            )
            .sort_values("average_popularity", ascending=False)
            .reset_index(drop=True)
        )

    def audio_feature_correlations(self, data: pd.DataFrame) -> pd.DataFrame:
        columns = ["track_popularity", *AUDIO_FEATURES]
        return data[columns].corr(numeric_only=True).round(3)

    def mood_summary(self, data: pd.DataFrame) -> pd.DataFrame:
        labelled = data.copy()
        conditions = [
            (labelled["energy"] >= 0.6) & (labelled["valence"] >= 0.5),
            (labelled["energy"] >= 0.6) & (labelled["valence"] < 0.5),
            (labelled["energy"] < 0.6) & (labelled["valence"] >= 0.5),
        ]
        choices = [
            "energetyczne i pozytywne",
            "energetyczne i mroczniejsze",
            "spokojne i pozytywne",
        ]
        labelled["mood_group"] = np.select(
            conditions,
            choices,
            default="spokojne i mroczniejsze",
        )
        return (
            labelled.groupby("mood_group", as_index=False)
            .agg(
                track_count=("track_name", "count"),
                average_popularity=("track_popularity", "mean"),
                average_energy=("energy", "mean"),
                average_valence=("valence", "mean"),
            )
            .sort_values("track_count", ascending=False)
            .reset_index(drop=True)
        )
