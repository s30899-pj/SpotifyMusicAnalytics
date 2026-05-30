from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import streamlit as st

from spotify_analytics.facade import SpotifyAnalyticsFacade
from spotify_analytics.visualizer import SpotifyVisualizer


DATA_PATH = Path("data/spotify_songs.csv")


def configure_page() -> None:
    st.set_page_config(
        page_title="Spotify Music Analytics",
        page_icon="🎧",
        layout="wide",
    )


@st.cache_data(show_spinner=False)
def load_data(path: str):
    facade = SpotifyAnalyticsFacade(Path(path))
    return facade.load_dataset()


def build_sidebar(data):
    st.sidebar.header("Filtry danych")

    genres = sorted(data["playlist_genre"].dropna().unique())
    selected_genres = st.sidebar.multiselect(
        "Gatunki",
        genres,
        default=genres,
    )

    subgenres = sorted(
        data.loc[data["playlist_genre"].isin(selected_genres), "playlist_subgenre"]
        .dropna()
        .unique()
    )
    selected_subgenres = st.sidebar.multiselect(
        "Podgatunki",
        subgenres,
        default=subgenres,
    )

    min_year = int(data["release_year"].min())
    max_year = int(data["release_year"].max())
    year_range = st.sidebar.slider(
        "Zakres lat wydania",
        min_year,
        max_year,
        (min_year, max_year),
    )

    popularity_range = st.sidebar.slider(
        "Zakres popularności",
        0,
        100,
        (0, 100),
    )

    top_n = st.sidebar.slider("Liczba wyników w rankingach", 5, 30, 10)

    return {
        "genres": selected_genres,
        "subgenres": selected_subgenres,
        "year_range": year_range,
        "popularity_range": popularity_range,
        "top_n": top_n,
    }


def show_metrics(data, analyzer) -> None:
    summary = analyzer.summary(data)
    cols = st.columns(4)
    cols[0].metric("Utwory", f"{summary['tracks']:,}")
    cols[1].metric("Artyści", f"{summary['artists']:,}")
    cols[2].metric("Gatunki", f"{summary['genres']:,}")
    cols[3].metric("Śr. popularność", f"{summary['average_popularity']:.1f}")


def main() -> None:
    configure_page()
    st.title("Spotify Music Analytics")
    st.caption(
        "Interaktywna analiza popularności, gatunków i cech audio utworów Spotify."
    )

    facade = SpotifyAnalyticsFacade(DATA_PATH)
    visualizer = SpotifyVisualizer()

    try:
        data = load_data(str(DATA_PATH))
    except Exception as error:
        st.error(f"Nie udało się wczytać danych: {error}")
        st.stop()

    filters = build_sidebar(data)
    analyzer = facade.analyzer
    insights = facade.insights
    filtered_data = analyzer.filter_tracks(
        data,
        genres=filters["genres"],
        subgenres=filters["subgenres"],
        year_range=filters["year_range"],
        popularity_range=filters["popularity_range"],
    )

    if filtered_data.empty:
        st.warning("Brak danych dla wybranych filtrów. Zmień ustawienia w panelu bocznym.")
        st.stop()

    show_metrics(filtered_data, analyzer)

    tabs = st.tabs(
        [
            "Eksploracja",
            "Popularność",
            "Gatunki",
            "Korelacje",
            "Nastrój",
            "Wnioski",
        ]
    )

    with tabs[0]:
        st.subheader("Podgląd danych")
        st.dataframe(
            filtered_data[
                [
                    "track_name",
                    "track_artist",
                    "track_popularity",
                    "playlist_genre",
                    "playlist_subgenre",
                    "release_year",
                    "duration_min",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Typy danych i braki")
        left, right = st.columns(2)
        with left:
            st.dataframe(analyzer.column_overview(filtered_data), use_container_width=True)
        with right:
            st.dataframe(analyzer.missing_values(filtered_data), use_container_width=True)

    with tabs[1]:
        st.subheader("Najpopularniejsze utwory")
        top_tracks = analyzer.top_tracks(filtered_data, filters["top_n"])
        st.dataframe(top_tracks, use_container_width=True, hide_index=True)

        st.pyplot(visualizer.popularity_distribution(filtered_data))
        st.info(insights.popularity_insight(filtered_data))

    with tabs[2]:
        st.subheader("Porównanie gatunków")
        genre_ranking = facade.run_strategy("genre_popularity", filtered_data)
        st.dataframe(genre_ranking, use_container_width=True, hide_index=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.pyplot(visualizer.genre_popularity_bar(genre_ranking))
        with col_b:
            st.pyplot(visualizer.genre_popularity_box(filtered_data))

        st.info(insights.genre_insight(genre_ranking))

    with tabs[3]:
        st.subheader("Korelacje cech audio")
        correlation = facade.run_strategy("correlation", filtered_data)
        st.dataframe(correlation, use_container_width=True)
        st.pyplot(visualizer.correlation_heatmap(correlation))
        st.info(insights.correlation_insight(correlation))

    with tabs[4]:
        st.subheader("Analiza nastroju: energia i pozytywność")
        st.pyplot(visualizer.mood_scatter(filtered_data))

        mood_summary = facade.run_strategy("mood", filtered_data)
        st.dataframe(mood_summary, use_container_width=True, hide_index=True)
        st.info(insights.mood_insight(mood_summary))

    with tabs[5]:
        st.subheader("Najważniejsze wnioski z aktualnie wybranych danych")
        for item in insights.all_insights(filtered_data, analyzer):
            st.write(f"- {item}")


if __name__ == "__main__":
    main()
