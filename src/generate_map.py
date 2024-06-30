import folium
import webbrowser

from folium.plugins import Search

from dataHandler import readExcelData, getCoordinates, getBounds, getPointDescription

filepath = 'dane_gmina_fredropol.xlsx'
readExcelData(filepath)
coordinates_list = getCoordinates()

map_fedropol = folium.Map(location=coordinates_list[0], zoom_start=12)
map_fedropol.fit_bounds(getBounds(coordinates_list))

features = []
for i, coord in enumerate(coordinates_list):
    popup_text = getPointDescription(['identyfikator PRNG', 'nazwa główna', 'rodzaj obiektu'], i)

    # Create GeoJSON feature
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coord[::-1]
        },
        "properties": {
            "name" : popup_text,
        }
    }
    features.append(feature)

# Create a GeoJSON Feature Collection
feature_collection = {
    "type": "FeatureCollection",
    "features": features,
}

gjson = folium.GeoJson(feature_collection).add_to(map_fedropol) # Stwórz GeoJson
folium.features.GeoJsonPopup(fields=["name"], labels=False).add_to(gjson) # Dodaj popupy

# Dodaj funkcjonalność wyszukiwania
search = Search(
    layer=gjson,
    geom_type='Point',
    placeholder="Wyszukaj...",
    collapsed=False,
    search_label='name',
    position="topleft",
    tooltip="Click to search"
).add_to(map_fedropol)

map_fedropol.save("fedropol_map.html")
webbrowser.open("fedropol_map.html")

print("Mapa została zapisana jako fedropol_map.html i otwarta w przeglądarce")