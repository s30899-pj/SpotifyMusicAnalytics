from abc import ABC, abstractmethod

import pandas as pd


class AnalysisStrategy(ABC):
    """Strategy interface for adding new analyses without changing the UI layer."""

    @abstractmethod
    def run(self, data: pd.DataFrame, analyzer):
        raise NotImplementedError


class GenrePopularityStrategy(AnalysisStrategy):
    def run(self, data: pd.DataFrame, analyzer) -> pd.DataFrame:
        return analyzer.genre_popularity(data)


class CorrelationStrategy(AnalysisStrategy):
    def run(self, data: pd.DataFrame, analyzer) -> pd.DataFrame:
        return analyzer.audio_feature_correlations(data)


class MoodStrategy(AnalysisStrategy):
    def run(self, data: pd.DataFrame, analyzer) -> pd.DataFrame:
        return analyzer.mood_summary(data)
