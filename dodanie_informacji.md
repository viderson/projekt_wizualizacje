### Edycja Informacji Wyświetlanych w Popupach w Twojej Aplikacji

Aby zmienić informacje wyświetlane po kliknięciu w lokalizacje na mapie, wykonaj poniższe kroki:

1. **Modyfikacja pliku `dataHandler.py`:**
   - Otwórz plik `dataHandler.py`.
   - Przejdź do linii 114.
   - Dodaj następującą linię kodu:
    ```python
     '<p><b>Wyświetlana_nazwa:</b> {row['nazwa_kolumny']}</p>'
    ```
     - Zamień `Wyświetlana_nazwa` na nazwę informacji, którą chcesz wyświetlić.
     - Zamień `nazwa_kolumny` na nazwę kolumny z pliku `.xlsx`, z której ta informacja ma być pobrana.

2. **Modyfikacja pliku `generate_map.py`:**
   - Otwórz plik `generate_map.py`.
   - Przejdź do linii 35 i 36.
   - Wewnątrz nawiasów `[]` dodaj `, 'nazwa_kolumny'`:
     ```python
     #Przykład:
     popup_text = formatPopup(getPointDescription(['identyfikator PRNG', 'nazwa główna', 'rodzaj obiektu', 'nazwa_kolumny'], i).sum())
     name = getPointDescription(['identyfikator PRNG', 'nazwa główna', 'rodzaj obiektu', 'nazwa_kolumny'], i).to_string(header=False, index=False)
     ```
   - Upewnij się, że `nazwa_kolumny` jest zgodna z nazwą kolumny z pliku `.xlsx`.

3. **Generowanie mapy:**
   - Po wprowadzeniu powyższych zmian, ponownie wygeneruj mapę w swojej aplikacji, aby zmiany zostały zastosowane.
