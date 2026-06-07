from pathlib import Path
import base64
import sys


ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pandas as pd
import streamlit as st

from spotify_analytics.facade import SpotifyAnalyticsFacade
from spotify_analytics.visualizer import SpotifyVisualizer


DATA_PATH = ROOT_DIR / "data" / "spotify_songs.csv"
ASSETS_DIR = ROOT_DIR / "assets"


def configure_page() -> None:
    st.set_page_config(
        page_title="Spotify Music Analytics",
        page_icon="🎧",
        layout="wide",
    )


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container { padding-top: 2.2rem; padding-bottom: 3rem; }
        .sma-hero {
            display: flex; align-items: center; gap: 1.4rem;
            padding: 1.5rem 1.8rem; border-radius: 1.1rem;
            background: radial-gradient(120% 140% at 0% 0%, #1DB95433 0%, #181818 55%, #101010 100%);
            border: 1px solid #2A2A2A; margin-bottom: 1.4rem;
        }
        .sma-hero img { width: 74px; height: 74px; }
        .sma-title { font-size: 2.3rem; font-weight: 800; line-height: 1.05; margin: 0; }
        .sma-title .accent {
            background: linear-gradient(90deg, #1ED760, #1AA64C);
            -webkit-background-clip: text; background-clip: text; color: transparent;
        }
        .sma-tag { color: #B3B3B3; font-size: 0.98rem; margin-top: 0.35rem; }
        .sma-eq { display: inline-flex; align-items: flex-end; gap: 4px; height: 46px; margin-left: auto; }
        .sma-eq span {
            width: 6px; border-radius: 3px; transform-origin: bottom;
            background: linear-gradient(#1ED760, #1AA64C); animation: sma-bounce 1.1s infinite ease-in-out;
        }
        .sma-eq span:nth-child(1){ height: 60%; animation-delay: 0s; }
        .sma-eq span:nth-child(2){ height: 100%; animation-delay: .18s; }
        .sma-eq span:nth-child(3){ height: 45%; animation-delay: .36s; }
        .sma-eq span:nth-child(4){ height: 80%; animation-delay: .12s; }
        .sma-eq span:nth-child(5){ height: 55%; animation-delay: .30s; }
        @keyframes sma-bounce { 0%,100%{ transform: scaleY(.35);} 50%{ transform: scaleY(1);} }
        .sma-insight {
            border-left: 4px solid #1DB954; background: #1DB9541A;
            padding: 0.8rem 1rem; border-radius: 0.6rem; color: #E8E8E8; margin: 0.4rem 0;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem; border-bottom: 1px solid #2A2A2A; padding-bottom: 0.2rem;
        }
        .stTabs [data-baseweb="tab"] {
            height: 44px; padding: 0 1.05rem; border-radius: 0.7rem;
            display: flex; align-items: center; justify-content: center;
        }
        .stTabs [data-baseweb="tab"] p { font-weight: 600; font-size: 0.95rem; }
        .stTabs [data-baseweb="tab"]:hover { background: #1A1A1A; }
        .stTabs [aria-selected="true"] { background: #1DB9541F; color: #1DB954; }
        .stTabs [data-baseweb="tab-highlight"] { background: #1DB954; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def logo_data_uri() -> str:
    svg = (ASSETS_DIR / "logo.svg").read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(svg).decode("ascii")


def render_header() -> None:
    st.markdown(
        f"""
        <div class="sma-hero">
            <img src="{logo_data_uri()}" alt="logo" />
            <div>
                <p class="sma-title">Spotify <span class="accent">Music Analytics</span></p>
                <div class="sma-tag">
                    Interaktywna eksploracja popularności, gatunków, trendów i nastroju utworów Spotify.
                </div>
            </div>
            <div class="sma-eq"><span></span><span></span><span></span><span></span><span></span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight(text: str) -> None:
    st.markdown(f'<div class="sma-insight">💡 {text}</div>', unsafe_allow_html=True)


@st.cache_data(show_spinner="Wczytywanie i czyszczenie danych...")
def load_data(path: str) -> pd.DataFrame:
    facade = SpotifyAnalyticsFacade(Path(path))
    return facade.load_dataset()


def build_sidebar(data: pd.DataFrame) -> dict:
    st.sidebar.header(":material/tune: Filtry danych")

    genres = sorted(data["playlist_genre"].dropna().unique())
    selected_genres = st.sidebar.pills(
        "Gatunki",
        genres,
        selection_mode="multi",
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

    popularity_range = st.sidebar.slider("Zakres popularności", 0, 100, (0, 100))
    top_n = st.sidebar.slider("Liczba wyników w rankingach", 5, 30, 10)

    st.sidebar.caption(
        "Sterowanie klawiaturą: Tab przełącza pola, strzałki regulują suwaki, "
        "Enter zatwierdza wybór."
    )

    return {
        "genres": selected_genres,
        "subgenres": selected_subgenres,
        "year_range": year_range,
        "popularity_range": popularity_range,
        "top_n": top_n,
    }


def show_metrics(filtered: pd.DataFrame, full: pd.DataFrame, analyzer) -> None:
    summary = analyzer.summary(filtered)
    share = len(filtered) / len(full) if len(full) else 0
    popularity_delta = summary["average_popularity"] - float(full["track_popularity"].mean())

    cols = st.columns(4)
    cols[0].metric(
        "Utwory",
        f"{summary['tracks']:,}".replace(",", " "),
        delta=f"{share:.0%} zbioru",
        delta_color="off",
    )
    cols[1].metric("Artyści", f"{summary['artists']:,}".replace(",", " "))
    cols[2].metric("Gatunki", f"{summary['genres']:,}")
    cols[3].metric(
        "Śr. popularność",
        f"{summary['average_popularity']:.1f}",
        delta=round(popularity_delta, 1),
        help="Różnica średniej popularności względem całego zbioru danych.",
    )


def main() -> None:
    configure_page()
    inject_styles()
    render_header()

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

    show_metrics(filtered_data, data, analyzer)

    tabs = st.tabs(
        [
            ":material/search: Eksploracja",
            ":material/local_fire_department: Popularność",
            ":material/category: Gatunki",
            ":material/show_chart: Trendy",
            ":material/grid_on: Korelacje",
            ":material/mood: Nastrój",
            ":material/lightbulb: Wnioski",
        ]
    )

    with tabs[0]:
        st.subheader("Podgląd danych")
        with st.container(border=True):
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
                width="stretch",
                hide_index=True,
            )
            st.download_button(
                "Pobierz przefiltrowane dane (CSV)",
                filtered_data.to_csv(index=False).encode("utf-8"),
                file_name="spotify_filtered.csv",
                mime="text/csv",
                icon=":material/download:",
            )

        left, right = st.columns(2)
        with left:
            st.subheader("Typy danych i braki")
            with st.container(border=True):
                st.dataframe(analyzer.column_overview(filtered_data), width="stretch")
                st.dataframe(analyzer.missing_values(filtered_data), width="stretch")
        with right:
            st.subheader("Kodowanie gatunków")
            with st.container(border=True):
                st.caption("Konwersja danych kategorycznych na numeryczne (kody gatunków).")
                codes = pd.Categorical(filtered_data["playlist_genre"]).codes
                mapping = (
                    filtered_data.assign(genre_code=codes)[["playlist_genre", "genre_code"]]
                    .drop_duplicates()
                    .sort_values("genre_code")
                    .reset_index(drop=True)
                )
                st.dataframe(mapping, width="stretch", hide_index=True)

    with tabs[1]:
        st.subheader("Najpopularniejsze utwory")
        with st.container(border=True):
            top_tracks = analyzer.top_tracks(filtered_data, filters["top_n"])
            st.dataframe(top_tracks, width="stretch", hide_index=True)
        with st.container(border=True):
            st.pyplot(visualizer.popularity_distribution(filtered_data))
        insight(insights.popularity_insight(filtered_data))

    with tabs[2]:
        st.subheader("Porównanie gatunków")
        genre_ranking = facade.run_strategy("genre_popularity", filtered_data)
        with st.container(border=True):
            st.dataframe(genre_ranking, width="stretch", hide_index=True)

        col_a, col_b = st.columns(2)
        with col_a:
            with st.container(border=True):
                st.pyplot(visualizer.genre_popularity_bar(genre_ranking))
        with col_b:
            with st.container(border=True):
                st.pyplot(visualizer.genre_popularity_box(filtered_data))

        insight(insights.genre_insight(genre_ranking))

    with tabs[3]:
        st.subheader("Trendy w czasie")
        trend = facade.run_strategy("trend", filtered_data)
        with st.container(border=True):
            st.pyplot(visualizer.popularity_trend_line(trend))
        with st.container(border=True):
            st.dataframe(trend, width="stretch", hide_index=True)
        insight(insights.trend_insight(trend))

    with tabs[4]:
        st.subheader("Korelacje cech audio")
        correlation = facade.run_strategy("correlation", filtered_data)
        with st.container(border=True):
            st.pyplot(visualizer.correlation_heatmap(correlation))
        with st.container(border=True):
            st.dataframe(correlation, width="stretch")
        insight(insights.correlation_insight(correlation))

    with tabs[5]:
        st.subheader("Analiza nastroju: energia i pozytywność")
        with st.container(border=True):
            st.pyplot(visualizer.mood_scatter(filtered_data))

        mood_summary = facade.run_strategy("mood", filtered_data)
        with st.container(border=True):
            st.dataframe(mood_summary, width="stretch", hide_index=True)
        insight(insights.mood_insight(mood_summary))

    with tabs[6]:
        st.subheader("Najważniejsze wnioski z wybranych danych")
        for item in insights.all_insights(filtered_data, analyzer):
            insight(item)


if __name__ == "__main__":
    main()
