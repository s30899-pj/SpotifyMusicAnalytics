import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class SpotifyVisualizer:
    """Creates Matplotlib and Seaborn charts for Streamlit."""

    def __init__(self) -> None:
        sns.set_theme(style="whitegrid", palette="Set2")

    def popularity_distribution(self, data: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(9, 4.8))
        sns.histplot(data=data, x="track_popularity", bins=20, kde=True, ax=ax)
        ax.set_title("Rozkład popularności utworów")
        ax.set_xlabel("Popularność")
        ax.set_ylabel("Liczba utworów")
        fig.tight_layout()
        return fig

    def genre_popularity_bar(self, genre_ranking: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(8, 4.8))
        top = genre_ranking.head(10)
        sns.barplot(
            data=top,
            x="average_popularity",
            y="playlist_genre",
            ax=ax,
        )
        ax.set_title("Średnia popularność według gatunku")
        ax.set_xlabel("Średnia popularność")
        ax.set_ylabel("Gatunek")
        fig.tight_layout()
        return fig

    def genre_popularity_box(self, data: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(8, 4.8))
        sns.boxplot(
            data=data,
            x="track_popularity",
            y="playlist_genre",
            ax=ax,
        )
        ax.set_title("Rozkład popularności w gatunkach")
        ax.set_xlabel("Popularność")
        ax.set_ylabel("Gatunek")
        fig.tight_layout()
        return fig

    def correlation_heatmap(self, correlation: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(9, 6.5))
        sns.heatmap(
            correlation,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            linewidths=0.5,
            ax=ax,
        )
        ax.set_title("Korelacje cech audio")
        fig.tight_layout()
        return fig

    def mood_scatter(self, data: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(9, 5.5))
        sns.scatterplot(
            data=data,
            x="valence",
            y="energy",
            hue="playlist_genre",
            size="track_popularity",
            sizes=(30, 180),
            alpha=0.7,
            ax=ax,
        )
        ax.axhline(0.6, color="gray", linestyle="--", linewidth=1)
        ax.axvline(0.5, color="gray", linestyle="--", linewidth=1)
        ax.set_title("Nastrój utworów: energia vs pozytywność")
        ax.set_xlabel("Valence - pozytywność nastroju")
        ax.set_ylabel("Energy - energia")
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        return fig
