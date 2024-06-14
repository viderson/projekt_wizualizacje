import folium
import webbrowser
from data_handler import readExcelData, getCoordinates, getBounds, getPointDescription

filepath = 'path'
readExcelData(filepath)

coordinates_list = getCoordinates()

map_fedropol = folium.Map(location=coordinates_list[0], zoom_start=12)
map_fedropol.fit_bounds(getBounds(coordinates_list))


for i, coord in enumerate(coordinates_list):
    popup_text = getPointDescription(['identyfikator PRNG', 'nazwa główna', 'rodzaj obiektu' ], i)

    if 'las' in popup_text:
        folium.Marker(
        coord,
        popup=popup_text,
        icon=folium.Icon(color='green', icon='tree', prefix='fa')
    ).add_to(map_fedropol)
        
    elif 'potok' in popup_text:
        folium.Marker(
        coord,
        popup=popup_text,
        icon=folium.Icon(color='blue', icon='water', prefix='fa')
    ).add_to(map_fedropol)
    
    elif 'góra' in popup_text or 'skała' in popup_text or 'masyw' in popup_text:
        folium.Marker(
        coord,
        popup=popup_text,
        icon=folium.Icon(color='gray', icon='mountain', prefix='fa')
    ).add_to(map_fedropol)
        
    elif 'pole' in popup_text or 'dolina'  in popup_text or 'jar' in popup_text:
        folium.Marker(
        coord,
        popup=popup_text,
        icon=folium.Icon(color='orange', icon='seedling', prefix='fa')
    ).add_to(map_fedropol)
        
    elif 'pole' in popup_text:
        folium.Marker(
        coord,
        popup=popup_text,
        icon=folium.Icon(color='orange', icon='seedling', prefix='fa')
    ).add_to(map_fedropol)
    
    elif 'kopiec' in popup_text:
        folium.Marker(
        coord,
        popup=popup_text,
        icon=folium.Icon(color='red', icon='landmark', prefix='fa')
    ).add_to(map_fedropol)
        
    elif 'łąki' in popup_text:
        folium.Marker(
        coord,
        popup=popup_text,
        icon=folium.Icon(color='darkgreen', icon='leaf', prefix='fa')
    ).add_to(map_fedropol)
        
    elif 'przełęcz' in popup_text:
        folium.Marker(
        coord,
        popup=popup_text,
        icon=folium.Icon(color='purple', icon='exchange-alt', prefix='fa')
    ).add_to(map_fedropol)
        
    elif 'region naturalny' in popup_text:
        folium.Marker(
        coord,
        popup=popup_text,
        icon=folium.Icon(color='darkpurple', icon='globe', prefix='fa')
    ).add_to(map_fedropol)
        
    elif 'uroczysko-dawna miejscowość' in popup_text:
        folium.Marker(
        coord,
        popup=popup_text,
        icon=folium.Icon(color='beige', icon='home', prefix='fa')
    ).add_to(map_fedropol)    

map_fedropol.save("fedropol_map.html")

webbrowser.open("fedropol_map.html")

print("Mapa została zapisana jako fedropol_map.html i otwarta w przeglądarce")
