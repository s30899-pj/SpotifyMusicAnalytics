from pathlib import Path

import pandas as pd

from spotify_analytics.analyzer import SpotifyAnalyzer
from spotify_analytics.cleaner import SpotifyDataCleaner
from spotify_analytics.data_loader import SpotifyDataLoader
from spotify_analytics.insights import InsightGenerator
from spotify_analytics.strategies import (
    CorrelationStrategy,
    GenrePopularityStrategy,
    MoodStrategy,
)


class SpotifyAnalyticsFacade:
    """Facade joining loading, cleaning, analysis and insight generation."""

    def __init__(self, data_path: Path):
        self.loader = SpotifyDataLoader(data_path)
        self.cleaner = SpotifyDataCleaner()
        self.analyzer = SpotifyAnalyzer()
        self.insights = InsightGenerator()
        self.strategies = {
            "genre_popularity": GenrePopularityStrategy(),
            "correlation": CorrelationStrategy(),
            "mood": MoodStrategy(),
        }

    def load_dataset(self) -> pd.DataFrame:
        raw_data = self.loader.load()
        return self.cleaner.clean(raw_data)

    def run_strategy(self, name: str, data: pd.DataFrame):
        if name not in self.strategies:
            raise ValueError(f"Nieznana strategia analizy: {name}")
        return self.strategies[name].run(data, self.analyzer)
