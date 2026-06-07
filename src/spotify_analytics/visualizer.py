import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

SPOTIFY_GREEN = "#1DB954"
PANEL_COLOR = "#181818"
GENRE_PALETTE = ["#1DB954", "#2FD4FF", "#C77DFF", "#FFB347", "#FF5D8F", "#4ADE80"]


class SpotifyVisualizer:
    """Tworzy wykresy Matplotlib i Seaborn w ciemnym motywie Spotify dla Streamlit."""

    def __init__(self) -> None:
        sns.set_theme(style="darkgrid")
        plt.rcParams.update(
            {
                "figure.facecolor": PANEL_COLOR,
                "axes.facecolor": PANEL_COLOR,
                "savefig.facecolor": PANEL_COLOR,
                "axes.edgecolor": "#333333",
                "axes.labelcolor": "#D0D0D0",
                "axes.titlecolor": "#FFFFFF",
                "axes.titleweight": "bold",
                "text.color": "#D0D0D0",
                "xtick.color": "#A0A0A0",
                "ytick.color": "#A0A0A0",
                "grid.color": "#2A2A2A",
                "legend.facecolor": PANEL_COLOR,
                "legend.edgecolor": "#333333",
            }
        )

    def popularity_distribution(self, data: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(9, 4.8))
        sns.histplot(
            data=data,
            x="track_popularity",
            bins=20,
            kde=True,
            color=SPOTIFY_GREEN,
            edgecolor=PANEL_COLOR,
            ax=ax,
        )
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
            hue="playlist_genre",
            palette=GENRE_PALETTE,
            legend=False,
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
            hue="playlist_genre",
            palette=GENRE_PALETTE,
            legend=False,
            ax=ax,
        )
        ax.set_title("Rozkład popularności w gatunkach")
        ax.set_xlabel("Popularność")
        ax.set_ylabel("Gatunek")
        fig.tight_layout()
        return fig

    def correlation_heatmap(self, correlation: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(9, 6.5))
        cmap = sns.diverging_palette(15, 145, s=75, l=50, as_cmap=True)
        sns.heatmap(
            correlation,
            annot=True,
            fmt=".2f",
            cmap=cmap,
            center=0,
            linewidths=0.5,
            linecolor=PANEL_COLOR,
            annot_kws={"color": "#0A0A0A"},
            cbar_kws={"shrink": 0.8},
            ax=ax,
        )
        ax.set_title("Korelacje cech audio")
        fig.tight_layout()
        return fig

    def popularity_trend_line(self, trend: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(9, 4.8))
        sns.lineplot(
            data=trend,
            x="release_year",
            y="average_popularity",
            color=SPOTIFY_GREEN,
            marker="o",
            linewidth=2.2,
            ax=ax,
        )
        ax.fill_between(
            trend["release_year"],
            trend["average_popularity"],
            color=SPOTIFY_GREEN,
            alpha=0.12,
        )
        ax.set_title("Średnia popularność utworów według roku wydania")
        ax.set_xlabel("Rok wydania")
        ax.set_ylabel("Średnia popularność")
        fig.tight_layout()
        return fig

    def mood_scatter(self, data: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(9, 5.5))
        sns.scatterplot(
            data=data,
            x="valence",
            y="energy",
            hue="playlist_genre",
            palette=GENRE_PALETTE,
            size="track_popularity",
            sizes=(30, 180),
            alpha=0.7,
            edgecolor="none",
            ax=ax,
        )
        ax.axhline(0.6, color="#666666", linestyle="--", linewidth=1)
        ax.axvline(0.5, color="#666666", linestyle="--", linewidth=1)
        ax.set_title("Nastrój utworów: energia vs pozytywność")
        ax.set_xlabel("Valence - pozytywność nastroju")
        ax.set_ylabel("Energy - energia")
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        return fig
