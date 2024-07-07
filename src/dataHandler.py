import re
import pandas as pd
from datetime import datetime

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


def formatPopup(row):
    popup_text = f"""
            <div style="font-family: Arial, sans-serif; padding: 10px;">
                <h4 style="margin-bottom: 8px;">{row['nazwa główna']}</h4>
                <p><b>Typ obiektu:</b> {row['rodzaj obiektu']}</p>
                <p><b>Identyfikator:</b> {row['identyfikator PRNG']}</p>
            </div>
        """
    return popup_text
def getPointDescription(selectedColumns, index):
    '''
    Tworzy popup dla danego punktu
    :param selectedColumns: lista nazw wybranych kolumn
    :param index: indeks punktu
    :return: tekst popupu
    '''
    row = getColumns(selectedColumns).iloc[[index]]
    return row


def getTimeStamps(i):
    """
    Funkcja wczytuje znaczniki czasowe z pliku Excel.

    :param filepath: Ścieżka do pliku Excel.
    :param time_column: Nazwa kolumny zawierającej znaczniki czasowe.
    :return: Lista znaczników czasowych.
    """
    data['ważna od'] = data['ważna od'].apply(pd.to_datetime)
    return data.loc[i]['ważna od'].isoformat()
