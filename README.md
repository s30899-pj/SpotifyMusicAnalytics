# Spotify Music Analytics

Interaktywna aplikacja Streamlit do analizy danych o utworach Spotify. Projekt
powstaje jako zadanie zaliczeniowe z analizy danych z wykorzystaniem bibliotek
Pandas, NumPy, Matplotlib i Seaborn.

## Cel analizy

Projekt odpowiada na pytanie:

> Jak cechy audio utworów, takie jak taneczność, energia, tempo, głośność i
> pozytywność nastroju, wiążą się z popularnością oraz gatunkiem muzycznym?

Aplikacja pozwala filtrować dane, sortować rankingi, porównywać gatunki,
oglądać korelacje oraz generować krótkie wnioski z aktualnie wybranych danych.

## Dane

Docelowe źródło danych:
https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs

W repozytorium znajduje się pełny plik `data/spotify_songs.csv`, dzięki czemu
projekt uruchamia się autonomicznie. Plik zawiera 32 833 rekordy i pochodzi z
publicznego zbioru Spotify Songs udostępnianego również w repozytorium
TidyTuesday:
https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv

## Uruchomienie

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Testy

```bash
pytest
```

## Struktura programu

- `app.py` - interfejs Streamlit.
- `SpotifyDataLoader` - wczytuje CSV i sprawdza wymagane kolumny.
- `SpotifyDataCleaner` - czyści dane, konwertuje typy, tworzy `release_year`
  i `duration_min`.
- `SpotifyAnalyzer` - wykonuje filtrowanie, sortowanie, grupowanie, rankingi
  i korelacje. W analizie nastroju wykorzystuje NumPy do wektorowej klasyfikacji
  utworów na podstawie energii i pozytywności.
- `SpotifyVisualizer` - tworzy wykresy Matplotlib/Seaborn.
- `InsightGenerator` - generuje tekstowe wnioski z wyników.
- `SpotifyAnalyticsFacade` - upraszcza komunikację między interfejsem i logiką.

## Wzorce projektowe

Projekt wykorzystuje wzorzec **Facade**. Klasa `SpotifyAnalyticsFacade` ukrywa
szczegóły wczytywania, czyszczenia i analizy danych, dzięki czemu `app.py`
pozostaje czytelny.

W module `strategies.py` zastosowano wzorzec **Strategy**. Różne analizy mogą
być rozwijane jako osobne strategie bez przebudowy głównej logiki aplikacji.

## Uzasadnienie metod i wykresów

- Histogram popularności pokazuje rozkład zmiennej liczbowej `track_popularity`.
- Wykres słupkowy średniej popularności porównuje kategorie, czyli gatunki.
- Boxplot popularności według gatunku pokazuje medianę, rozrzut i wartości
  odstające, więc jest lepszy niż sama średnia.
- Heatmapa korelacji jest dopasowana do wielu zmiennych numerycznych i pozwala
  szybko ocenić siłę związków między cechami audio.
- Wykres punktowy `energy` vs `valence` pokazuje charakter utworów: spokojny,
  energetyczny, pozytywny lub mroczniejszy.

## Obsługa błędów

Program obsługuje m.in. brak pliku CSV, pusty plik, błędny format CSV, brak
wymaganych kolumn i brak danych po zastosowaniu filtrów. Zamiast przerywać
działanie, aplikacja pokazuje użytkownikowi czytelny komunikat.
