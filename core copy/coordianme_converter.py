# Welcome to CoordiName
import json

with open('core\CoordiName_database.json', 'r') as file:
    data = json.load(file)


# DMS to decimal conversion functions
def dms_to_decimal(degrees: int, minutes: int, seconds: float, direction: str) -> float:
    """
    Converts coordinates from degrees, minutes, and seconds (DMS) format to decimal degrees format.

    This function takes the degrees, minutes, and seconds of a geographic coordinate, along with a direction indicator ('N', 'S', 'E', 'W'), and converts it to a decimal degree format. Directions 'S' and 'W' result in negative decimal degrees.

    Parameters:
    degrees (int): The degree component of the coordinate.
    minutes (int): The minutes component of the coordinate.
    seconds (float): The seconds component of the coordinate.
    direction (str): A single character string indicating the direction ('N', 'S', 'E', 'W') of the coordinate.

    Returns:
    float: The coordinate in decimal degrees format.

    Example:
    >>> dms_to_decimal(34, 12, 18, 'N')
    34.205
    >>> dms_to_decimal(118, 22, 30, 'W')
    -118.375
    """
    decimal_degree = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal_degree *= -1
    return decimal_degree


def coordinates_dms_to_decimal(lat: list, lon: list) -> tuple:
    """
    Converts latitude and longitude coordinates from degrees, minutes, and seconds (DMS) format to decimal format.

    Parameters:
    lat (list): A list containing the latitude in DMS format. The list should contain four elements: degrees (int), minutes (int), seconds (float), and direction (str, 'N' or 'S').
    lon (list): A list containing the longitude in DMS format. The list should contain four elements: degrees (int), minutes (int), seconds (float), and direction (str, 'E' or 'W').

    Returns:
    tuple: A tuple containing two elements, the latitude and longitude in decimal format.

    Example:
    >>> coordinates_dms_to_decimal([34, 12, 18, 'N'], [118, 22, 30, 'W'])
    (34.205, -118.375)
    """
    latitude = dms_to_decimal(lat[0], lat[1], lat[2], lat[3])
    longitude = dms_to_decimal(lon[0], lon[1], lon[2], lon[3])
    return latitude, longitude

# -----------------------------------------------------------------


# Decimal to DMS conversion functions

def decimal_to_dms(decimal_degree: float, is_latitude: bool = True) -> tuple:
    """
    Converts a decimal degree value to degrees, minutes, and seconds (DMS) format, along with the appropriate cardinal direction (N, S, E, W).

    Parameters:
    decimal_degree (float): The decimal degree value to be converted. Positive values indicate north or east, depending on whether it represents latitude or longitude, respectively. Negative values indicate south or west.
    is_latitude (bool, optional): A flag indicating whether the decimal degree value represents latitude (True) or longitude (False). Defaults to True.

    Returns:
    tuple: A tuple containing the degrees (int), minutes (int), seconds (float), and direction (str) in DMS format. The direction is 'N' or 'S' for latitudes and 'E' or 'W' for longitudes.

    Example:
    >>> decimal_to_dms(34.205, True)
    (34, 12, 18.0, 'N')
    >>> decimal_to_dms(-118.375, False)
    (118, 22, 30.0, 'W')
    """
    is_positive = decimal_degree >= 0
    decimal_degree = abs(decimal_degree)
    degrees = int(decimal_degree)
    minutes = int((decimal_degree - degrees) * 60)
    seconds = (decimal_degree - degrees - minutes / 60) * 3600
    if is_latitude:
        direction = 'N' if is_positive else 'S'
    else:
        direction = 'E' if is_positive else 'W'
    return degrees, minutes, seconds, direction


def coordinates_decimal_to_dms(lat: float, lon: float) -> tuple:
    """
    Converts latitude and longitude coordinates from decimal format to degrees, minutes, and seconds (DMS) format.

    Parameters:
    lat (float): The latitude in decimal format. Positive values indicate the northern hemisphere, and negative values indicate the southern hemisphere.
    lon (float): The longitude in decimal format. Positive values indicate the eastern hemisphere, and negative values indicate the western hemisphere.

    Returns:
    tuple: A tuple containing two elements. Each element is a tuple representing the latitude and longitude in DMS format, respectively. Each DMS format is represented as a tuple containing degrees (int), minutes (int), seconds (float), and direction (str, 'N' or 'S' for latitude and 'E' or 'W' for longitude).

    Example:
    >>> coordinates_decimal_to_dms(34.205, -118.375)
    ((34, 12, 18, 'N'), (118, 22, 30, 'W'))
    """
    lat_dms = decimal_to_dms(lat, is_latitude=True)
    lon_dms = decimal_to_dms(lon, is_latitude=False)
    return lat_dms, lon_dms

# -----------------------------------------------------------------

# Coordinate to CoordiName functions ------------------------------


def lattitude_to_0_to_180(lattitude: int, direction: str = None) -> int:
    """
    Converts a latitude value to a normalized value within the range [0, 180] based on its direction.
    If the direction is South, the latitude is converted to a range of 90 to 0.
    If the direction is North, the latitude is converted to a range of 90 to 180.
    If the direction is not provided, it is determined based on the sign of the latitude:
    negative latitudes are considered South (and the latitude is made positive), while positive latitudes are considered North.

    Parameters:
    lattitude (int): The latitude value to be converted. This should be a numerical value representing the latitude.
    direction (str, optional): The direction of the latitude. Expected values are 'N' for North or 'S' for South. If not provided, the direction is inferred from the sign of the latitude value, with negative being South and positive being North.

    Returns:
    int: The converted latitude value based on the direction, normalized to be within the range [0, 180].
    """
    if direction is None:
        if lattitude < 0:
            direction = "S"
            lattitude *= -1
        else:
            direction = "N"
    if direction == "S":
        degrees = 90 - lattitude
    else:
        degrees = lattitude + 90
    return degrees


def longitude_to_0_to_360(longitude: int, direction: str = None) -> int:
    """
    Converts a longitude value to a normalized value within the range [0, 360] based on its direction.
    If the direction is West, the longitude is converted to a range of 180 to 0.
    If the direction is East, the longitude is converted to a range of 180 to 360.
    If the direction is not provided, it is determined based on the sign of the longitude:
    negative longitudes are considered West (and the longitude is made positive), while positive longitudes are considered East.

    Parameters:
    longitude (int): The longitude value to be converted. This should be a numerical value representing the longitude.
    direction (str, optional): The direction of the longitude. Expected values are 'E' for East or 'W' for West. If not provided, the direction is inferred from the sign of the longitude value, with negative being West and positive being East.

    Returns:
    int: The converted longitude value based on the direction, normalized to be within the range [0, 360].
    """
    if direction == None:
        if longitude < 0:
            direction = "W"
            longitude *= -1
        else:
            direction = "E"
    if direction == "W":
        degrees = 180 - longitude
    else:
        degrees = longitude + 180

    return degrees % 360


def normalize_minutes_and_seconds(minutes: int, seconds: int) -> int:
    """
    Normalize minutes and seconds to be within the range [0, 3600]
    Parameters:
    minutes (int): The minutes value to be converted. 
    seconds (int): The seconds value to be converted. 

    Returns:
    int: The converted minutes and seconds value based on the range.
    """
    return (minutes * 60 + seconds) % 3600


def dms_to_coordiname(lat_data: list, lon_data: list) -> dict:
    """
    Converts latitude and longitude data from degrees, minutes, and seconds (DMS) format to a dictionary containing corresponding words for degrees and minutes/seconds, both separately and combined into a single string, with a precision of 30m^2.

    Parameters:
    lat_data (list): A list containing the latitude data in the order of degrees, minutes, seconds, and direction ('N' or 'S'). Example: [34, 12, 18, 'N']
    lon_data (list): A list containing the longitude data in the order of degrees, minutes, seconds, and direction ('E' or 'W'). Example: [118, 22, 30, 'W']

    Returns:
    dict: A dictionary with keys 'Latitude', 'Longitude', 'Together', and 'Word'. 'Latitude' and 'Longitude' are dictionaries themselves containing 'degree_word' and 'minute_second_word'. 'Together' is a list of the combined words, and 'Word' is a string concatenation of all the words separated by dashes.

    Example return value:
    >>> dms_to_coordiname([34, 12, 18, 'N'], [118, 22, 30, 'W'])
    {
        "Latitude": {
            "degree_word": "someWordForLatitudeDegree",
            "minute_second_word": "someWordForLatitudeMinuteSecond"
        },
        "Longitude": {
            "degree_word": "someWordForLongitudeDegree",
            "minute_second_word": "someWordForLongitudeMinuteSecond"
        },
        "Together": ["someWordForLatitudeDegree", "someWordForLatitudeMinuteSecond", "someWordForLongitudeDegree", "someWordForLongitudeMinuteSecond"],
        "Word": "someWordForLatitudeDegree-someWordForLatitudeMinuteSecond-someWordForLongitudeDegree-someWordForLongitudeMinuteSecond"
    }
    """
    [lat_degrees, lat_minutes, lat_seconds, lat_direction] = lat_data
    [lon_degrees, lon_minutes, lon_seconds, lon_direction] = lon_data
    lat_degrees_index = lattitude_to_0_to_180(lat_degrees, lat_direction)
    lon_degrees_index = longitude_to_0_to_360(lon_degrees, lon_direction)

    lat_min_sec_index = normalize_minutes_and_seconds(
        lat_minutes, int(round(lat_seconds)))
    lon_min_sec_index = normalize_minutes_and_seconds(
        lon_minutes, int(round(lon_seconds)))
    arr = [data["words_180"][lat_degrees_index], data["words_3600"][lat_min_sec_index],
           data["words_360"][lon_degrees_index], data["words_3600"][lon_min_sec_index]]
    res = {
        "Lattitude": {
            "degree_word": arr[0],
            "minute_second_word": arr[1]
        },
        "Longitude": {
            "degree_word": arr[2],
            "minute_second_word": arr[3]
        },
        "Word_list": arr,
        "Word": f"{arr[0]}-{arr[1]}-{arr[2]}-{arr[3]}"
    }

    return res

# -------------------------------------------------------------------------

# CoordiName to Coordinate functions---------------------------------------


def _0_to_180_to_lattitude(degrees: int) -> tuple:
    """
    Converts a latitude value from a normalized 0 to 180 degrees scale back to the traditional latitude format with direction.

    This function is designed to reverse a latitude normalization process where latitudes in the southern hemisphere are represented as values from 0 to 90, and latitudes in the northern hemisphere are represented as values from 90 to 180. The function returns the traditional latitude value along with its corresponding cardinal direction ('N' for north, 'S' for south).

    Parameters:
    degrees (int): The latitude value in the 0 to 180 degrees scale to be converted back to traditional format.

    Returns:
    tuple: A tuple containing the latitude value in traditional format (int) and its cardinal direction ('N' or 'S').

    Example:
    >>> _0_to_180_to_lattitude(45)
    (45, 'S')
    >>> _0_to_180_to_lattitude(135)
    (45, 'N')
    """
    if degrees <= 90:
        return 90 - degrees, "S"
    else:
        return degrees - 90, "N"


def _0_to_360_longitude(degrees: int) -> tuple:
    """
    Converts a longitude value from a normalized 0 to 360 degrees scale back to the traditional longitude format with direction.

    This function is designed to reverse a longitude normalization process where longitudes in the western hemisphere are represented as values from 0 to 180, and longitudes in the eastern hemisphere are represented as values from 180 to 360. The function returns the traditional longitude value along with its corresponding cardinal direction ('E' for east, 'W' for west).

    Parameters:
    degrees (int): The longitude value in the 0 to 360 degrees scale to be converted back to traditional format.

    Returns:
    tuple: A tuple containing the longitude value in traditional format (int) and its cardinal direction ('E' or 'W').

    Example:
    >>> _0_to_360_longitude(45)
    (135, 'W')
    >>> _0_to_360_longitude(225)
    (45, 'E')
    """
    if degrees <= 180:
        return 180 - degrees, "W"
    else:
        return degrees - 180, "E"


def index_to_minutes_seconds(index: int) -> tuple:
    """
    Converts an index value to minutes and seconds.

    Parameters:
    index (int): The index value to be converted.

    Returns:
    tuple: A tuple containing the minutes (int) and seconds (int) derived from the index.
    """
    return index//60, index % 60


def coordiname_to_coordinate(word: str) -> dict:
    """
    Converts a 'coordiname' (a word representation of coordinates) into both DMS (Degrees, Minutes, Seconds) and decimal formats.

    The function splits the input word into parts representing latitude and longitude in a custom encoding, converts these parts into numeric values using predefined dictionaries, and then formats these values into human-readable DMS and decimal coordinate formats.

    Parameters:
    word (str): The 'coordiname' string to be converted, formatted as 'lat-degrees-lat-minutes-sec-lon-degrees-lon-minutes-sec'.

    Returns:
    dict: A dictionary containing the coordinates in both DMS and decimal formats, including individual components and formatted strings.

    Example:
    >>> coordiname_to_coordinate("melon-communicate-macchiato-registration")
    {
        "DMS": {
            "lat_list": [26, 10, 41, 'N'],
            "lon_list": [10, 41, 0, 'E'],
            "lattitude": "26°10'41\"N",
            "longitude": "10°41'0\"E",
            "DMS_string": "26°10'41\"N 10°41'0\"E"
        },
        "decimal": {
            "lattitude": 26.178056,
            "longitude": 10.683333,
            "decimal_string": "26.178056 10.683333"
        }
    }
    """
    words = word.split('-')
    lat_degrees_index = data["dict_words_to_number_180"][words[0]]
    lat_min_sec_index = data["dict_words_to_number_3600"][words[1]]
    lon_degrees_index = data["dict_words_to_number_360"][words[2]]
    lon_min_sec_index = data["dict_words_to_number_3600"][words[3]]
    lat_degree, lat_direction = _0_to_180_to_lattitude(lat_degrees_index)
    lon_degree, lon_direction = _0_to_360_longitude(lon_degrees_index)
    lat_min, lat_sec = index_to_minutes_seconds(lat_min_sec_index)
    lon_min, lon_sec = index_to_minutes_seconds(lon_min_sec_index)

    lattitude, longitude = coordinates_dms_to_decimal([lat_degree, lat_min, lat_sec, lat_direction], [
        lon_degree, lon_min, lon_sec, lon_direction])
    res = {
        "DMS": {
            "lat_list": [lat_degree, lat_min, lat_sec, lat_direction],
            "lon_list": [lon_degree, lon_min, lon_sec, lon_direction],
            "lattitude": f"{lat_degree}°{lat_min}'{lat_sec}\"{lat_direction}",
            "longitude": f" {lon_degree}°{lon_min}'{lon_sec}\"{lon_direction}",
            "DMS_string": f" {lat_degree}°{lat_min}'{lat_sec}\"{lat_direction} {lon_degree}°{lon_min}'{lon_sec}\"{lon_direction}"
        },
        "decimal": {
            "lattitude": lattitude,
            "longitude": longitude,
            "decimal_string": f" {lattitude} {longitude}"
        }
    }

    return res

# -------------------------------------------------------------------------


if __name__ == "__main__":

    # Coordinate to CoordiName-----------------------------------------------------------------
    # Example usage 1 (with decimal coordinates)
    latitude = 26.177979069330007
    longitude = 91.76085595487656

    lat_dms, lon_dms = coordinates_decimal_to_dms(latitude, longitude)

    print("Example usage of dms_to_coordiname 1",
          "inputs - ", latitude, longitude)
    print(dms_to_coordiname(lat_dms, lon_dms))

    # Example usage 2 (with DMS coordinates)

    lat_degree = 26
    lat_min = 10
    lat_sec = 41
    lat_direction = "N"

    lat_dms = [lat_degree, lat_min, lat_sec, lat_direction]

    lon_degree = 91
    lon_min = 45
    lon_sec = 39
    lon_direction = "E"

    lon_dms = [lon_degree, lon_min, lon_sec, lon_direction]

    print("Example usage of dms_to_coordiname 2", "inputs ", lat_dms, lon_dms)
    print(dms_to_coordiname(lat_dms, lon_dms))

    # DMS to CoordiName done !!!-------------------------------------------------

    # CoordiName to Coordinate----------------------------------------------------

    # Example usage 1

    word = 'melon-communicate-macchiato-registration'

    print("Example usage of coordiname_to_coordinate 1", "input", word)
    print(coordiname_to_coordinate(word))
