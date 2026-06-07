# 🎧 Spotify Music Analytics

Interaktywna aplikacja do analizy danych o utworach Spotify. Projekt
powstał wykorzystaniem bibliotek
**Pandas, NumPy, Matplotlib i Seaborn**.


## Cel analizy

Projekt odpowiada na pytanie:

> Jak cechy audio utworów (taneczność, energia, tempo, głośność, pozytywność) wiążą
> się z popularnością, gatunkiem muzycznym oraz jak popularność zmienia się w czasie?

Aplikacja pozwala filtrować dane, sortować rankingi, porównywać gatunki, oglądać
korelacje, śledzić trendy w czasie, analizować nastrój utworów oraz generować
krótkie, automatyczne wnioski z aktualnie wybranych danych.

## Dane

Docelowe źródło danych:
https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs

W repozytorium znajduje się pełny plik `data/spotify_songs.csv` (32 833 rekordy),
dzięki czemu projekt uruchamia się **autonomicznie**, bez pobierania czegokolwiek.

## Uruchomienie

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Testy

```bash
pytest
```

## Sterowanie klawiaturą

Wszystkie elementy interfejsu są dostępne z klawiatury (wymaganie A6): `Tab`
przełącza pola, strzałki regulują suwaki i przełączają zakładki, `Enter`/`Spacja`
zatwierdzają wybór, a pola wielokrotnego wyboru obsługują wpisywanie i strzałki.

## Struktura programu i relacje klas

Logika jest oddzielona od interfejsu. Warstwa danych i analizy mieszka w pakiecie
`src/spotify_analytics`, a `app.py` jest tylko cienkim interfejsem Streamlit.

- `app.py` — interfejs Streamlit (układ, filtry, wykresy, motyw, logo).
- `assets/logo.svg` — autorskie logo z wkomponowaną ikoną Spotify.
- `.streamlit/config.toml` — ciemny motyw w barwach Spotify.
- `SpotifyDataLoader` — wczytuje CSV i waliduje wymagane kolumny.
- `SpotifyDataCleaner` — czyści dane, konwertuje typy, tworzy `release_year`
  i `duration_min`.
- `SpotifyAnalyzer` — filtrowanie, sortowanie, grupowanie, rankingi, korelacje,
  trend w czasie oraz klasyfikacja nastroju (wektorowo, z użyciem NumPy).
- `SpotifyVisualizer` — wykresy Matplotlib/Seaborn w ciemnym motywie.
- `InsightGenerator` — generuje tekstowe wnioski z wyników.
- `AnalysisStrategy` + strategie konkretne — wymienne algorytmy analizy.
- `SpotifyAnalyticsFacade` — spina wszystkie komponenty i udostępnia je interfejsowi.

Relacje: `SpotifyAnalyticsFacade` **komponuje** (kompozycja) loader, cleaner,
analyzer, insights oraz słownik strategii. Strategie **dziedziczą** po wspólnej
klasie abstrakcyjnej `AnalysisStrategy` i **polimorficznie** udostępniają metodę
`run(...)`. Interfejs (`app.py`) nie zna szczegółów analiz — rozmawia wyłącznie
z fasadą i analizatorem.

## Zastosowane paradygmaty programowania

Z wykładu wykorzystano paradygmaty, które realnie poprawiają strukturę projektu:

- **Obiektowy** — każdy etap przetwarzania to osobna klasa o jednej
  odpowiedzialności (loader, cleaner, analyzer, visualizer, insights, fasada).
- **Abstrakcja i dziedziczenie** — `AnalysisStrategy` to klasa abstrakcyjna
  (`abc.ABC` z `@abstractmethod`), po której dziedziczą konkretne strategie.
- **Polimorfizm** — fasada wywołuje `strategy.run(...)` jednakowo dla każdej
  strategii, niezależnie od jej rodzaju.
- **Enkapsulacja** — szczegóły wczytywania, czyszczenia i liczenia są ukryte
  w klasach; interfejs korzysta tylko z ich publicznych metod.
- **Kompozycja** — fasada składa się z gotowych obiektów współpracowników,
  zamiast po nich dziedziczyć.
- **Funkcyjny i deklaratywny** — analizy opisują *co* policzyć, a nie *jak*:
  wektorowe operacje Pandas/NumPy (`groupby`, `agg`, `corr`, `np.select`) oraz
  listy składane przy budowaniu wniosków.

## Zastosowane wzorce projektowe

- **Facade (strukturalny)** — `SpotifyAnalyticsFacade` ukrywa złożoność wczytywania,
  czyszczenia i analizy danych za prostym interfejsem (`load_dataset`, `run_strategy`),
  dzięki czemu `app.py` pozostaje czytelny.
- **Strategy (behawioralny)** — w `strategies.py` każda analiza (gatunki, korelacje,
  nastrój, trend) jest osobną, wymienną strategią. Nową analizę dodaje się przez
  utworzenie kolejnej klasy i zarejestrowanie jej w fasadzie — bez zmian w interfejsie.

## Uzasadnienie metod i wykresów (dopasowanie do typu danych)

- **Histogram** popularności pokazuje rozkład jednej zmiennej liczbowej
  (`track_popularity`) — idealny do oceny skośności i typowych wartości.
- **Wykres słupkowy** średniej popularności porównuje wartość liczbową między
  kategoriami (gatunkami) — naturalny wybór dla zmiennej kategorycznej.
- **Boxplot** popularności według gatunku pokazuje medianę, rozrzut i wartości
  odstające, więc niesie więcej informacji niż sama średnia.
- **Wykres liniowy** trendu jest dopasowany do danych uporządkowanych w czasie
  (rok wydania) i czytelnie pokazuje kierunek zmian popularności.
- **Heatmapa korelacji** jest dopasowana do wielu zmiennych numerycznych naraz
  i pozwala szybko ocenić siłę i znak związków między cechami audio.
- **Wykres punktowy** `energy` vs `valence` pokazuje charakter utworów (spokojny,
  energetyczny, pozytywny, mroczniejszy), a wielkość punktu koduje popularność.

Wnioski liczbowe (np. „która cecha najsilniej koreluje z popularnością") są
wyznaczane na danych, więc pozostają sensowne dla dowolnego wyboru filtrów.

## Obsługa błędów (nieprzerwana egzekucja)

Program obsługuje m.in. brak pliku CSV, pusty plik, błędny format CSV, brak
wymaganych kolumn oraz brak danych po zastosowaniu filtrów. Zamiast przerywać
działanie wyjątkiem, aplikacja pokazuje użytkownikowi czytelny komunikat
(`st.error` / `st.warning`) i zatrzymuje się bezpiecznie.
