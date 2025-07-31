# 🗺️ Visualization Project: Municipality of Fredropol

This project enables interactive data visualization for the municipality of **Fredropol**, combining tabular data (from Excel) with geospatial map generation.

---

## 🚀 Features

* Parses data from an Excel file (`dane_gmina_fredropol.xlsx`).
* Generates interactive HTML maps with markers and pop-ups.
* Lightweight Flask server for file upload and map display.
* Easy to extend: add custom data layers, filters, and export formats.

---

## 🗂️ Project Structure

```
projekt_wizualizacje/
├── build_win32.bat            # Windows launcher script (optional)
├── build_macos.sh             # macOS launcher script (optional)
├── README.md                  # This documentation
├── .gitignore                 # Git ignore rules
└── src/
    ├── main.py                # Flask application entry point
    ├── dataHandler.py         # Excel data parser and HTML formatter
    ├── generate_map.py        # Map generation module using Folium
    ├── dane_gmina_fredropol.xlsx  # Sample input data file
    ├── requirements.txt       # Python dependencies
    ├── templates/
    │   └── index.html         # Basic upload form template
    └── venv/                  # Virtual environment (not in Git)
```

---

## ✅ Requirements

* **Python** 3.8+
* Python packages:

  * `pandas`
  * `numpy`
  * `flask`
  * `folium`
  * `openpyxl`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

1. **Clone the repository**

   ```bash
   git clone https://github.com/viderson/projekt_wizualizacje.git
   ```
2. **Navigate to the source folder**

   ```bash
   cd projekt_wizualizacje/src
   ```
3. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
5. **Start the Flask server**

   ```bash
   python main.py
   ```

   You should see:

   ```text
   * Running on http://127.0.0.1:5000/
   ```
6. **Open in browser**
   Go to `http://127.0.0.1:5000`, upload your Excel file, and click **Load** to generate the map.

---

## 🌍 Usage Example

After starting the app, upload any properly structured Excel file and interactively explore the generated map. You can pan, zoom, and click markers to view pop-ups. To extend:

* Add layers directly in `generate_map.py`.
* Customize pop-up HTML in `dataHandler.py`.
* Export maps to PDF or GeoJSON by adding export logic.

---

## 🛠️ Authors

Maintained by **viderson** [GitHub](https://github.com/viderson).

---

## 🧾 Customizing Pop-up Content

1. **Edit `src/dataHandler.py`**

   * Locate the HTML-building logic (e.g., `formatPopup`).
   * Append new fields:

     ```python
     html_elements.append(f"<p><strong>MyLabel:</strong> {row['my_column']}</p>")
     ```
   * Ensure `'my_column'` matches the Excel header exactly.

2. **Edit `src/generate_map.py`**

   * In the marker loop, include your new column:

     ```python
     popup_html = formatPopup(getPointDescription(
         ['identyfikator PRNG', 'nazwa główna', 'rodzaj obiektu', 'my_column'], i
     ))
     ```

3. **Restart the app**

   ```bash
   python main.py
   ```

   Upload again to see updated pop-ups.
