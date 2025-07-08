
# 🗺️ Visualization Project: Municipality of Fredropol

This project enables interactive data visualization for the municipality of **Fredropol**, combining tabular data (from Excel) with geospatial map generation.

---

## 🚀 Features

- Parses data from an Excel file (`dane_gmina_fredropol.xlsx`)
- Generates interactive HTML maps
- Supports both Windows and macOS (via `.bat` and `.sh` launcher scripts)
- Lightweight server with a basic `index.html` template
- Can be easily extended for other municipalities or datasets

---

## 🗂️ Project Structure

```
projekt_wizualizacje/
├── build_win32.bat            # Windows launcher script
├── build_macos.sh             # macOS launcher script
├── README.md                  # This file
├── .gitignore
└── src/
    ├── main.py                # Main application logic
    ├── dataHandler.py         # Excel data parser
    ├── generate_map.py        # Map generation module
    ├── dane_gmina_fredropol.xlsx  # Input data file
    ├── requirements.txt       # Python dependencies
    ├── app_windows.c          # Windows-specific C module (optional)
    ├── app_macos.c            # macOS-specific C module (optional)
    └── templates/
        └── index.html         # HTML template for map display
```

---

## ✅ Requirements

- Python 3.8+
- Required packages: `pandas`, `folium`, `openpyxl`, `flask`

Install them using:

```bash
pip install -r src/requirements.txt
```

---

## ▶️ How to Run

From inside the `src/` directory:

```bash
python main.py
```

Then open your browser at `http://127.0.0.1:5000/` to view the map.

---

## 🌍 Usage Example

The program loads structured data from an Excel spreadsheet and overlays it on an interactive map viewable in your browser. You can extend it with new layers, filters, or export options (e.g., PDF, GeoJSON).

---

## 🛠️ Authors

Developed as part of a university course or a geospatial data processing project.

---


---

## 🧾 Customizing Pop-up Content on the Map

To change the information displayed when clicking on locations in the generated map, follow these steps:

### 1. Modify `dataHandler.py`:

- Open the file `src/dataHandler.py`.
- Go to line **114**.
- Add the following line below:

```python
'<p><b>Displayed_Label:</b> {row['column_name']}</p>'
```

- Replace `Displayed_Label` with the label you want to show in the popup.
- Replace `column_name` with the actual column name from the `.xlsx` file.

---

### 2. Modify `generate_map.py`:

- Open the file `src/generate_map.py`.
- Go to lines **35 and 36**.
- Inside the square brackets, add your column name:

```python
# Example:
popup_text = formatPopup(getPointDescription(['identyfikator PRNG', 'nazwa główna', 'rodzaj obiektu', 'column_name'], i).sum())
name = getPointDescription(['identyfikator PRNG', 'nazwa główna', 'rodzaj obiektu', 'column_name'], i).to_string(header=False, index=False)
```

- Ensure that `column_name` exactly matches the column header in your `.xlsx` spreadsheet.

---

### 3. Regenerate the Map:

After making these edits, re-run the application to regenerate the map and see your updated pop-up content reflected in the browser.

