import folium
import webbrowser

from folium.plugins import Search, TimestampedGeoJson

from dataHandler import readExcelData, getCoordinates, getBounds, getPointDescription

filepath = 'dane_gmina_fredropol.xlsx'
readExcelData(filepath)
coordinates_list = getCoordinates()

map_fedropol = folium.Map(location=coordinates_list[0], zoom_start=12)
map_fedropol.fit_bounds(getBounds(coordinates_list))

features = []
for i, coord in enumerate(coordinates_list):
    popup_text = getPointDescription(['identyfikator PRNG', 'nazwa główna', 'rodzaj obiektu'], i)
    color = None
    icon = None

    if 'las' in popup_text:
        color = 'green'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%230c6f08&icon=tree&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"

    elif 'potok' in popup_text:
        color = 'blue'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%230ee5e9&icon=water&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"

    elif 'góra' in popup_text or 'skała' in popup_text or 'masyw' in popup_text:
        color = 'gray'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%2361696a&icon=mountain&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"

    elif 'kopiec' in popup_text:
        color = 'red'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%238cb57f&icon=terrain&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"

    elif 'pole' in popup_text or 'dolina' in popup_text or 'jar' in popup_text or 'pola' in popup_text:
        color = 'orange'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%239be351&icon=seedling&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"

    elif 'łąki' in popup_text:
        color = 'darkgreen'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%23d3f035&icon=grass&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"

    elif 'przełęcz' in popup_text:
        color = 'purple'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%23b935f0&icon=route&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"

    elif 'region naturalny' in popup_text:
        color = 'darkpurple'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%23fdfdfd&icon=cruelty_free&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"

    elif 'uroczysko-dawna miejscowość' in popup_text:
        color = 'beige'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%238f3d3d&icon=home&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"

    # Create GeoJSON feature
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coord[::-1]
        },
        "properties": {
            "name" : popup_text,
            "popup": popup_text,
            "markerColor" : color,
            "icon": "marker",
            "iconstyle": {
                "iconUrl": f'{icon}',
                 "iconSize": [31, 46],

            },
        }
    }
    features.append(feature)

gjson = folium.GeoJson(
    {
        "type": "FeatureCollection",
        "features": features
    },
    popup= folium.GeoJsonPopup(fields=['name'], labels=False),
    name="geojson",
    show=False
).add_to(map_fedropol)
folium.LayerControl().add_to(map_fedropol)
# Add a search box to the map
search = Search(
    layer=gjson,
    geom_type='Point',
    placeholder='Search for a location',
    collapsed=False,
    search_label='name',
).add_to(map_fedropol)


# Add a timestamped geojson layer for the timeline
folium.plugins.TimestampedGeoJson(
    {"type": "FeatureCollection", "features": features},
    period="P1M",
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options="YYYY/MM/DD",
    time_slider_drag_update=True,
    duration="P2M",
).add_to(map_fedropol)


map_fedropol.save("fedropol_map.html")
webbrowser.open("fedropol_map.html")

print("Mapa została zapisana jako fedropol_map.html i otwarta w przeglądarce")