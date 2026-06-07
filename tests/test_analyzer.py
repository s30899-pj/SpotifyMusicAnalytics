from spotify_analytics.analyzer import SpotifyAnalyzer


def test_filter_tracks_by_genre_and_year_range(sample_data):
    analyzer = SpotifyAnalyzer()

    result = analyzer.filter_tracks(
        sample_data,
        genres=["pop"],
        year_range=(2020, 2021),
    )

    assert len(result) == 2
    assert set(result["playlist_genre"]) == {"pop"}


def test_top_tracks_are_sorted_by_popularity_descending(sample_data):
    analyzer = SpotifyAnalyzer()

    result = analyzer.top_tracks(sample_data, limit=2)

    assert result["track_popularity"].tolist() == [90, 70]


def test_genre_popularity_groups_rows(sample_data):
    analyzer = SpotifyAnalyzer()

    result = analyzer.genre_popularity(sample_data)

    pop_row = result[result["playlist_genre"] == "pop"].iloc[0]
    assert pop_row["track_count"] == 2
    assert pop_row["average_popularity"] == 80


def test_popularity_trend_is_sorted_by_year_and_aggregates(sample_data):
    analyzer = SpotifyAnalyzer()

    result = analyzer.popularity_trend(sample_data)

    assert result["release_year"].tolist() == [2019, 2020, 2021]
    row_2020 = result[result["release_year"] == 2020].iloc[0]
    assert row_2020["track_count"] == 1
    assert row_2020["average_popularity"] == 90


def test_mood_summary_labels_energetic_positive_group(sample_data):
    analyzer = SpotifyAnalyzer()

    result = analyzer.mood_summary(sample_data)

    assert "energetyczne i pozytywne" in result["mood_group"].tolist()
    assert result["track_count"].sum() == 3
