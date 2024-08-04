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


# Example usage:
longitude = 180  # Example longitude string
direction = "E"  # Example direction string
normalized_longitude = longitude_to_0_to_360(longitude, direction)
print(f"Original Longitude: {str(longitude) + direction}")
print(f"Converted Longitude: {normalized_longitude}°")
