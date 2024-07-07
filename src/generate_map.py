import sys
import folium
import webbrowser
import pandas as pd
from folium.plugins import Search, TimestampedGeoJson, FeatureGroupSubGroup

from dataHandler import readExcelData, getCoordinates, getBounds, getPointDescription, getTimeStamps, formatPopup

filepath = sys.argv[1]
data = readExcelData(filepath)
coordinates_list = getCoordinates()

map_fedropol = folium.Map(location=coordinates_list[0], zoom_start=12)
map_fedropol.fit_bounds(getBounds(coordinates_list))

main_group = folium.FeatureGroup(name='All Locations', show=False).add_to(map_fedropol)

groups = {
    'forest': folium.plugins.FeatureGroupSubGroup(main_group, 'las', show=True).add_to(map_fedropol),
    'stream': folium.plugins.FeatureGroupSubGroup(main_group, 'potok', show=True).add_to(map_fedropol),
    'mountain': folium.plugins.FeatureGroupSubGroup(main_group, 'góra', show=True).add_to(map_fedropol),
    'mound': folium.plugins.FeatureGroupSubGroup(main_group, 'kopiec', show=True).add_to(map_fedropol),
    'field': folium.plugins.FeatureGroupSubGroup(main_group, 'pole', show=True).add_to(map_fedropol),
    'meadow': folium.plugins.FeatureGroupSubGroup(main_group, 'łąki', show=True).add_to(map_fedropol),
    'pass': folium.plugins.FeatureGroupSubGroup(main_group, 'przełęcz', show=True).add_to(map_fedropol),
    'natural_region': folium.plugins.FeatureGroupSubGroup(main_group, 'region naturalny', show=True).add_to(map_fedropol),
    'historical_settlement': folium.plugins.FeatureGroupSubGroup(main_group, 'uroczysko-dawna miejscowość', show=True).add_to(map_fedropol),
}

default_icon = "https://api.geoapify.com/v1/icon/?type=material&color=%230c6f08&icon=help&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"

features = []
for i, coord in enumerate(coordinates_list):
    popup_text = formatPopup(getPointDescription(['identyfikator PRNG', 'nazwa główna', 'rodzaj obiektu'], i).sum())
    name = getPointDescription(['identyfikator PRNG', 'nazwa główna', 'rodzaj obiektu'], i).to_string(header=False, index=False)
    color = None
    icon = default_icon
    group = main_group

    if 'las' in popup_text:
        color = 'green'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%230c6f08&icon=tree&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"
        group = groups['forest']
    elif 'potok' in popup_text:
        color = 'blue'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%230ee5e9&icon=water&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"
        group = groups['stream']
    elif 'góra' in popup_text or 'skała' in popup_text or 'masyw' in popup_text:
        color = 'gray'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%2361696a&icon=mountain&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"
        group = groups['mountain']
    elif 'kopiec' in popup_text:
        color = 'red'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%238cb57f&icon=terrain&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"
        group = groups['mound']
    elif 'pole' in popup_text or 'dolina' in popup_text or 'jar' in popup_text or 'pola' in popup_text:
        color = 'orange'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%239be351&icon=seedling&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"
        group = groups['field']
    elif 'łąki' in popup_text:
        color = 'darkgreen'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%23d3f035&icon=grass&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"
        group = groups['meadow']
    elif 'przełęcz' in popup_text:
        color = 'purple'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%23b935f0&icon=route&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"
        group = groups['pass']
    elif 'region naturalny' in popup_text:
        color = 'darkpurple'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%23fdfdfd&icon=cruelty_free&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"
        group = groups['natural_region']
    elif 'uroczysko-dawna miejscowość' in popup_text:
        color = 'beige'
        icon = "https://api.geoapify.com/v1/icon/?type=material&color=%238f3d3d&icon=home&iconType=awesome&iconSize=large&scaleFactor=2&apiKey=769fdc58c4cc45b3a87a679303341049"
        group = groups['historical_settlement']

    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coord[::-1]
        },
        "properties": {
            "time": getTimeStamps(i),
            "name": name,
            "popup": popup_text,
            "markerColor": color,
            "icon": "marker",
            "iconstyle": {
                "iconUrl": f'{icon}',
                "iconSize": [31, 46],
            },
        }
    }
    features.append(feature)

    
    html_popup = folium.Html(popup_text, script=True)
    popup = folium.Popup(html_popup, max_width=300)

    
    folium.Marker(
        location=coord,
        popup=popup,
        icon=folium.CustomIcon(icon, icon_size=(31, 46))
    ).add_to(group)


feature_collection = {
    'type': 'FeatureCollection',
    'features': features
}


gjson = folium.GeoJson(
    feature_collection,
    marker=folium.Circle(radius=0, fill_color="orange", fill_opacity=0.0, color="black", weight=0),
    popup=folium.GeoJsonPopup(fields=['name'], labels=False),
    name="geojson",
).add_to(map_fedropol)

search = Search(
    layer=gjson,
    geom_type='Point',
    placeholder='Search for a location',
    collapsed=False,
    search_label='name',
    search_zoom=18,
    show=False
).add_to(map_fedropol)



TimestampedGeoJson(
    feature_collection,
    period='P3M',
    add_last_point=True,
    auto_play=True,
    loop=False
).add_to(map_fedropol)


folium.LayerControl(collapsed=True).add_to(map_fedropol)

map_fedropol.save("fedropol_map.html")
webbrowser.open("fedropol_map.html")
