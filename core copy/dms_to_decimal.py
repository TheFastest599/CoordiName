def dms_to_decimal(degrees, minutes, seconds, direction):
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


# Example usage
# Latitude: 26°10'40.72"N
lat_degrees = 26
lat_minutes = 10
lat_seconds = 41
lat_direction = 'N'

# Longitude: 91°45'39.08"E
lon_degrees = 91
lon_minutes = 45
lon_seconds = 39
lon_direction = 'E'

lattitude, longitude = coordinates_dms_to_decimal(
    [lat_degrees, lat_minutes, lat_seconds, lat_direction], [lon_degrees, lon_minutes, lon_seconds, lon_direction])

print(f"Latitude: {lattitude}")
print(f"Longitude: {longitude}")
