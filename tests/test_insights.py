from spotify_analytics.analyzer import SpotifyAnalyzer
from spotify_analytics.insights import InsightGenerator
from tests.test_analyzer import sample_data


def test_insight_generator_returns_textual_conclusions():
    analyzer = SpotifyAnalyzer()
    generator = InsightGenerator()

    result = generator.all_insights(sample_data(), analyzer)

    assert len(result) == 4
    assert all(isinstance(item, str) and item for item in result)
