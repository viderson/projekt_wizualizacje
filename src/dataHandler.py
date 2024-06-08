import re
import pandas as pd

def readExcelData(filepath):
    '''
    Czytanie danych zawartych w formacie .xlsx i przypisanie ich do zmiennej globalnej
    :param filepath - ścieżka do pliku xlsx:
    :return:
    '''
    global data
    try:
        data = pd.read_excel(filepath)
        return data
    except Exception as e:
        print(f'Exception while reading form file {e}')
        return None

def getColumns(columnsName):
    '''
    Zwraca wybrane kolumny z DataFrame
    Przykład getColumns(['identyfikator PRNG', 'nazwa główna']
    :param columnsName - nazwy wybranych kolumn:
    :return :
    '''
    try:
        data_filtered = data[columnsName]
        return data_filtered
    except Exception as e:
        print(f'Exception while getting columns from DataFrame {e}')
        return None

def calculateCoordinates(rawCoordinates):
    '''
    Funkcja przeliczająca koordynaty w formie stopnie, minuty, sekundy
    na wartość liczbową
    :param rawCoordinates:
    :return:
    '''
    degrees = int(rawCoordinates.group(1))
    minutes = int(rawCoordinates.group(2))
    seconds = int(rawCoordinates.group(3))
    return degrees + (minutes / 60.0) + (seconds / 3600.0)

def getCoordinates():
    '''
    Pobiera współrzędne geograficzne z pliku
    Zwraca listę zawierającą jako element [longitude, latitude]
    :return:
    '''
    coordinates_list = []
    for row in getColumns('współrzędne geograficzne'):
        data_coordinates = row.split(" ")
        pattern = r'(\d+)°(\d+)\'(\d+)"'
        match0 = re.search(pattern, data_coordinates[0])
        match1 = re.search(pattern, data_coordinates[1])
        latitude = calculateCoordinates(match0)
        longitude = calculateCoordinates(match1)
        coordinates_list.append([latitude, longitude])
    return coordinates_list
def getBounds(coordinates_list):
    '''
    Oblicza wymiary współrzędnych potrzebne w celu ustalenia zooma początkowego
    mieszczącego wszystkie punkty na mapie
    użycie: map.fit_bounds(dataHandler.getBounds(coordinates_list))
    :param coordinates_list - lista w której [latitude, longitude] jest elementem:
    :return [(min_lat, min_lon), (max_lat, max_lon)]:
    '''
    min_latitude = coordinates_list[0][0]
    max_latitude = coordinates_list[0][0]
    min_longitude = coordinates_list[0][1]
    max_longitude = coordinates_list[0][1]
    for coord in coordinates_list:
        if coord[1] > max_longitude:
            max_longitude = coord[1]
        elif coord[1] < min_longitude:
            min_longitude = coord[1]
        if coord[0] > max_latitude:
            max_latitude = coord[0]
        elif coord[0] < min_latitude:
            min_latitude = coord[0]
    return [(min_latitude, min_longitude), (max_latitude, max_longitude)]

def getPointDescription(selectedColumns, index):
    '''
    Tworzy popup dla danego punktu
    Przykład użycia: folium.features.Circle(coord, radius=40, color='red', fill=True, popup=f"{dataHandler.getPointDescription(['nazwa główna', 'rodzaj obiektu'], i)}", fill_color='pink', fill_opacity=0.4).add_to(m)
    :param selectedColumns:
    :param index:
    :return:
    '''
    row = getColumns(selectedColumns).head(index).tail(1)
    return row.to_string(header=False, index=False)
