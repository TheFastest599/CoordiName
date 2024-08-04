from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter
from dotenv import load_dotenv
import os


load_dotenv()


class SingletonGeolocator:
    _instance = None

    @classmethod
    async def get_instance(cls):
        print("Getting instance")
        if cls._instance is None:
            cls._instance = Nominatim(user_agent=os.getenv(
                "OSM_USER_AGENT"), adapter_factory=AioHTTPAdapter, timeout=10)
        return cls._instance


async def get_geocode_async(address):
    geolocator = await SingletonGeolocator.get_instance()
    # Now you can use geolocator to perform geolocation requests
    location = await geolocator.geocode(address)
    return location


async def get_reverse_geocode_async(lattitude, longitude):
    geolocator = await SingletonGeolocator.get_instance()
    # Now you can use geolocator to perform reverse geolocation requests
    location = await geolocator.reverse(f"{lattitude}, {longitude}")
    return location
