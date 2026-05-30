import pandas as pd


class InsightGenerator:
    """Builds short textual conclusions from computed analytical results."""

    def popularity_insight(self, data: pd.DataFrame) -> str:
        average = data["track_popularity"].mean()
        median = data["track_popularity"].median()
        if average > median:
            return (
                "Średnia popularność jest wyższa od mediany, co sugeruje obecność "
                "grupy bardzo popularnych utworów podbijających wynik."
            )
        return (
            "Mediana popularności jest zbliżona do średniej lub od niej wyższa, "
            "więc rozkład popularności jest w wybranych danych bardziej wyrównany."
        )

    def genre_insight(self, genre_ranking: pd.DataFrame) -> str:
        if genre_ranking.empty:
            return "Brak danych gatunkowych dla wybranych filtrów."

        top = genre_ranking.iloc[0]
        return (
            f"Najwyższą średnią popularność ma gatunek {top['playlist_genre']} "
            f"ze średnim wynikiem {top['average_popularity']:.1f}."
        )

    def correlation_insight(self, correlation: pd.DataFrame) -> str:
        if "track_popularity" not in correlation:
            return "Nie można obliczyć korelacji z popularnością."

        popularity_correlation = (
            correlation["track_popularity"]
            .drop(labels=["track_popularity"], errors="ignore")
            .dropna()
        )
        if popularity_correlation.empty:
            return "Za mało danych, aby wskazać korelacje z popularnością."

        strongest = popularity_correlation.abs().idxmax()
        value = popularity_correlation[strongest]
        strength = "słaba"
        if abs(value) >= 0.5:
            strength = "umiarkowana lub silna"
        elif abs(value) >= 0.3:
            strength = "umiarkowana"

        direction = "dodatnia" if value > 0 else "ujemna"
        return (
            f"Największy związek z popularnością ma cecha {strongest}. "
            f"Korelacja jest {direction} i {strength} ({value:.2f})."
        )

    def mood_insight(self, mood_summary: pd.DataFrame) -> str:
        if mood_summary.empty:
            return "Brak danych do analizy nastroju."

        most_common = mood_summary.iloc[0]
        return (
            f"Najliczniejsza grupa nastroju to: {most_common['mood_group']}. "
            f"Obejmuje {int(most_common['track_count'])} utworów."
        )

    def all_insights(self, data: pd.DataFrame, analyzer) -> list[str]:
        genre_ranking = analyzer.genre_popularity(data)
        correlation = analyzer.audio_feature_correlations(data)
        mood_summary = analyzer.mood_summary(data)

        return [
            self.popularity_insight(data),
            self.genre_insight(genre_ranking),
            self.correlation_insight(correlation),
            self.mood_insight(mood_summary),
        ]
