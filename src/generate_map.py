import folium
import webbrowser

from folium.plugins import Search

from dataHandler import readExcelData, getCoordinates, getBounds, getPointDescription

filepath = 'dane_gmina_fredropol.xlsx'
readExcelData(filepath)

coordinates_list = getCoordinates()

map_fedropol = folium.Map(location=coordinates_list[0], zoom_start=12)
map_fedropol.fit_bounds(getBounds(coordinates_list))
markers = folium.FeatureGroup(name='Markers').add_to(map_fedropol)
for i, coord in enumerate(coordinates_list):
    color = None
    icon = None
    popup_text = getPointDescription(['identyfikator PRNG', 'nazwa główna', 'rodzaj obiektu' ], i)
    if 'las' in popup_text:
        color = 'green'
        icon = 'tree'

    elif 'potok' in popup_text:
        color = 'blue'
        icon = 'water'

    elif 'góra' in popup_text or 'skała' in popup_text or 'masyw' in popup_text:
        color = 'gray'
        icon = 'mountain'

    elif 'pole' in popup_text or 'dolina'  in popup_text or 'jar' in popup_text:
        color = 'orange'
        icon = 'seedling'

    elif 'kopiec' in popup_text:
        color = 'red'
        icon = 'landmark'

    elif 'łąki' in popup_text:
        color = 'darkgreen'
        icon = 'leaf'

    elif 'przełęcz' in popup_text:
        color = 'purple'
        icon = 'exchange-alt'

    elif 'region naturalny' in popup_text:
        color = 'darkpurple'
        icon = 'global'

    elif 'uroczysko-dawna miejscowość' in popup_text:
        color = 'beige'
        icon = 'home'

    marker = folium.Marker(
        coord,
        name=popup_text,
        popup=popup_text,
        icon=folium.Icon(color=color, icon=icon, prefix='fa')
    ).add_to(markers)


    folium.Circle(
        location=coord,
        radius=100,  # Promień w metrach
        color=color,
        fill=True,
        fill_color=color
    ).add_to(map_fedropol)

# Dodaj funkcjonalność wyszukiwania
search = Search(
    layer=markers,
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
