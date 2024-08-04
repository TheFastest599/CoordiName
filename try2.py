from timezonefinder import TimezoneFinder


# object creation
obj = TimezoneFinder()


# pass the longitude and latitude
# in timezone_at and
# it return time zone
latitude = 26.1779
longitude = 91.7608
result = obj.timezone_at(lng=longitude, lat=latitude)
print(result)
