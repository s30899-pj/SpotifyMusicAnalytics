from abc import ABC, abstractmethod

import pandas as pd


class AnalysisStrategy(ABC):
    """Interfejs strategii pozwalający dodawać nowe analizy bez zmiany warstwy interfejsu."""

    @abstractmethod
    def run(self, data: pd.DataFrame, analyzer):
        raise NotImplementedError


class GenrePopularityStrategy(AnalysisStrategy):
    """Strategia rankingu gatunków według popularności i cech audio."""

    def run(self, data: pd.DataFrame, analyzer) -> pd.DataFrame:
        return analyzer.genre_popularity(data)


class CorrelationStrategy(AnalysisStrategy):
    """Strategia liczenia korelacji między cechami audio a popularnością."""

    def run(self, data: pd.DataFrame, analyzer) -> pd.DataFrame:
        return analyzer.audio_feature_correlations(data)


class MoodStrategy(AnalysisStrategy):
    """Strategia grupowania utworów według nastroju (energia i pozytywność)."""

    def run(self, data: pd.DataFrame, analyzer) -> pd.DataFrame:
        return analyzer.mood_summary(data)


class TrendStrategy(AnalysisStrategy):
    """Strategia analizy zmian popularności i cech audio w czasie (po roku wydania)."""

    def run(self, data: pd.DataFrame, analyzer) -> pd.DataFrame:
        return analyzer.popularity_trend(data)
