
from geopy.geocoders import Nominatim
import time

start = time.time()

# Creating a geocoder object
geolocator = Nominatim(user_agent="my_app")

# Geocoding an address
location = geolocator.geocode("Guwahati Assam")
location1 = geolocator.geocode(
    "1600 Pennsylvania Ave NW, Washington, DC 20500")
location2 = geolocator.geocode(
    "1600 Pennsylvania Ave NW, Washington, DC 20500")
location3 = geolocator.geocode(
    "1600 Pennsylvania Ave NW, Washington, DC 20500")
if location is not None:
    print(location.latitude, location.longitude)
    print(location1.latitude, location1.longitude)
    print(location2.latitude, location2.longitude)
    print(location3.latitude, location3.longitude)
else:
    print("Address not found")

# Reverse geocoding coordinates
address = geolocator.reverse("38.8976633, -77.0365739")
address1 = geolocator.reverse("38.8976633, -77.0365739")
address2 = geolocator.reverse("38.8976633, -77.0365739")
address3 = geolocator.reverse("38.8976633, -77.0365739")
if address is not None:
    print(address.address)
    print(address1.address)
    print(address2.address)
    print(address3.address)
else:
    print("Coordinates not found")


end = time.time()

print("Time taken - ", end - start)
