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


# Example usage:
lattitude = 90  # Example lattitude string
direction = "N"
normalized_lattitude = lattitude_to_0_to_180(lattitude, direction)
print(f"Original lattitude: {str(lattitude) + direction}")
print(f"Converted lattitude: {normalized_lattitude}°")
