def decimal_to_dms(decimal_degree, is_latitude=True):
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


def convert_coordinates(lat, lon):
    lat_dms = decimal_to_dms(lat, is_latitude=True)
    lon_dms = decimal_to_dms(lon, is_latitude=False)
    return lat_dms, lon_dms


# Example usage
latitude = 26.177979069330007
longitude = 91.76085595487656

lat_dms, lon_dms = convert_coordinates(latitude, longitude)

print(f"Latitude: {lat_dms[0]}°{lat_dms[1]}'{lat_dms[2]:.0f}\"{lat_dms[3]}")
print(f"Longitude: {lon_dms[0]}°{lon_dms[1]}'{lon_dms[2]:.0f}\"{lon_dms[3]}")
