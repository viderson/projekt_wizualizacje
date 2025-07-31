import re
import pandas as pd
from datetime import datetime


def readExcelData(filepath):
    """
    Read data from an Excel (.xlsx) file and store it in a global variable.

    :param filepath: Path to the .xlsx file
    :return: DataFrame containing the Excel data, or None if an error occurs
    """
    global data
    try:
        data = pd.read_excel(filepath)
        return data
    except Exception as e:
        print(f"Exception while reading the Excel file: {e}")
        return None


def getColumns(column_names):
    """
    Return selected columns from the global DataFrame.

    :param column_names: List of column names to retrieve
    :return: DataFrame containing only the specified columns, or None if an error occurs
    """
    try:
        return data[column_names]
    except Exception as e:
        print(f"Exception while retrieving columns from DataFrame: {e}")
        return None


def calculateCoordinates(raw_match):
    """
    Convert a match object representing degrees, minutes, and seconds into a decimal degree value.

    :param raw_match: Regex match object with groups for degrees, minutes, and seconds
    :return: Decimal degree value, or None if an error occurs
    """
    try:
        degrees = int(raw_match.group(1))
        minutes = int(raw_match.group(2))
        seconds = int(raw_match.group(3))
        return degrees + (minutes / 60.0) + (seconds / 3600.0)
    except Exception as e:
        print(f"Error while calculating coordinates: {e}")
        return None


def getCoordinates():
    """
    Extract geographic coordinates from the loaded data.

    :return: List of [latitude, longitude] pairs, or an empty list if an error occurs
    """
    coordinates_list = []
    try:
        coords_col = getColumns(['współrzędne geograficzne'])
        if coords_col is None:
            raise ValueError("Column 'współrzędne geograficzne' not found.")

        for entry in coords_col['współrzędne geograficzne']:
            parts = entry.split(" ")
            pattern = r"(\d+)°(\d+)'(\d+)\""
            match_lat = re.search(pattern, parts[0])  # latitude part
            match_lon = re.search(pattern, parts[1])  # longitude part

            if not match_lat or not match_lon:
                raise ValueError(f"Invalid coordinate format: {entry}")

            lat = calculateCoordinates(match_lat)
            lon = calculateCoordinates(match_lon)
            if lat is None or lon is None:
                raise ValueError(f"Coordinate conversion failed for: {entry}")

            coordinates_list.append([lat, lon])
    except Exception as e:
        print(f"Error while getting coordinates: {e}")
        return []
    return coordinates_list


def getBounds(coordinates_list):
    """
    Calculate bounding box for a list of coordinates, useful for setting map zoom.

    :param coordinates_list: List of [latitude, longitude] pairs
    :return: [(min_lat, min_lon), (max_lat, max_lon)], or None if error
    """
    if not coordinates_list:
        print("Empty coordinates list.")
        return None
    try:
        lats = [c[0] for c in coordinates_list]
        lons = [c[1] for c in coordinates_list]
        return [(min(lats), min(lons)), (max(lats), max(lons))]
    except Exception as e:
        print(f"Error while calculating bounds: {e}")
        return None


def formatPopup(row):
    """
    Build HTML content for a map popup from a row of data.

    :param row: Series or dict containing data for a single point
    :return: HTML string for popup, or empty string if error
    """
    try:
        html = f"""
        <div style=\"font-family: Arial, sans-serif; padding: 10px;\">
            <h4 style=\"margin-bottom: 8px;\">{row['nazwa główna']}</h4>
            <p><b>Object Type:</b> {row['rodzaj obiektu']}</p>
            <p><b>Document Date:</b> {row['data dokumentu źródłowego']}</p>
        </div>
        """
        return html
    except Exception as e:
        print(f"Error while formatting popup: {e}")
        return ''


def getPointDescription(selected_columns, index):
    """
    Retrieve a subset of data to describe a point for popup content.

    :param selected_columns: List of column names to include
    :param index: Row index in the DataFrame
    :return: DataFrame slice or None if error
    """
    try:
        subset = getColumns(selected_columns)
        return subset.iloc[[index]].fillna('no data')
    except Exception as e:
        print(f"Error while getting point description: {e}")
        return None


def getTimeStamps(i):
    """
    Retrieve timestamp from the 'ważna od' column for a given row index.

    :param i: Row index in the DataFrame
    :return: ISO-formatted timestamp string, or None if error
    """
    try:
        if 'ważna od' not in data.columns:
            raise KeyError("'ważna od' column is missing.")
        data['ważna od'] = pd.to_datetime(data['ważna od'])
        return data.loc[i, 'ważna od'].isoformat()
    except Exception as e:
        print(f"Error while getting timestamps: {e}")
        return None
