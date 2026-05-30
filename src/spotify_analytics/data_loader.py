from pathlib import Path

import pandas as pd

from spotify_analytics.config import REQUIRED_COLUMNS


class DataLoadingError(Exception):
    """Raised when the dataset cannot be loaded correctly."""


class SpotifyDataLoader:
    """Loads the Spotify CSV dataset and validates its required schema."""

    def __init__(self, path: Path):
        self.path = Path(path)

    def load(self) -> pd.DataFrame:
        if not self.path.exists():
            raise DataLoadingError(f"Nie znaleziono pliku danych: {self.path}")

        try:
            data = pd.read_csv(self.path)
        except pd.errors.EmptyDataError as error:
            raise DataLoadingError("Plik CSV jest pusty.") from error
        except pd.errors.ParserError as error:
            raise DataLoadingError("Plik CSV ma niepoprawny format.") from error
        except OSError as error:
            raise DataLoadingError(f"Nie można odczytać pliku: {error}") from error

        self._validate_columns(data)
        return data

    def _validate_columns(self, data: pd.DataFrame) -> None:
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in data]
        if missing_columns:
            missing = ", ".join(missing_columns)
            raise DataLoadingError(f"Brakuje wymaganych kolumn: {missing}")
