from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from models.apiModel import getCoordiName, getLatLong, geoCode
from config.database import collection_user, collection_apiKey
from config.middleware import get_api_key
from core.coordianme_converter import coordinates_decimal_to_dms, dms_to_coordiname, coordiname_to_coordinate
from models.geoLocator import get_geocode_async, get_reverse_geocode_async
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from timezonefinder import TimezoneFinder
from dotenv import load_dotenv


apiRouter = APIRouter()

load_dotenv()


# Load the data from the JSON file
_data_cache = None


timezoneObj = TimezoneFinder()

# Load the data from the JSON file


def get_data():
    global _data_cache
    print("CoordiName config loaded")
    # Check if data has already been loaded
    if _data_cache is None:
        # If not, load the data and cache it
        with open('core/Coordiname_config.json', 'r') as file:
            _data_cache = json.load(file)
    # Return the cached data
    return _data_cache


configData = get_data()


# Handle Api request Count
async def handle_api_request_count(apiKeyDetails, apiCallCount=1):
    if apiKeyDetails["usageToday"] < configData["tier"][str(apiKeyDetails["tier"])]["reqPerDay"]:
        await collection_apiKey.update_one({"key": apiKeyDetails["key"]}, {
            "$inc": {"usageToday": apiCallCount, "usageTotal": apiCallCount}})
    else:
        raise HTTPException(
            status_code=403, detail="Daily Request limit exceeded")


# Api Route to handle "/api/getcoordiname"


@apiRouter.post("/api/getcoordiname")
async def getCoordiname(data: getCoordiName, apiKeyDetails=Depends(get_api_key)):
    """
    Processes a list of latitude and longitude pairs to return various geographical information.

    For each pair of coordinates, this endpoint returns the decimal format, a generated 'coordiName',
    and optionally timezone and reverse geocode information if requested. It validates the coordinates,
    handles API request counts, and manages errors appropriately.

    Normal - API request count is 1 . Can get max 20 CoordiName and timezone per request. (api request count is 1)
    reverse_geocode : true - API request count is 1 + (1 * no of entries per request (max 5)) . Can get max 5 CoordiName, timezone and reverse_geocode per request. (api request count is max  6)

    Args:
        data (getCoordiName): A Pydantic model that includes the latitude and longitude pairs,
                              and flags for reverse geocode and timezone information.
        apiKeyDetails (Depends): Dependency that extracts and validates the API key from the request.

    Returns:
        list: A list of dictionaries, each containing the processed information for a pair of coordinates.

    Raises:
        HTTPException: For invalid input data or any unexpected error during processing.
    """
    try:
        if not data.latLong:
            raise ValueError("Latitude and Longitude data is required.")
        responsePerReq = configData["apiReqBucket"]
        apiCallCount = 1
        if data.reverse_geocode:
            responsePerReq = configData["apiReqBucketAdvanced"]
        res = []
        for i in data.latLong[:responsePerReq]:
            if not (-90 <= i[0] <= 90) or not (-180 <= i[1] <= 180):
                raise ValueError(f"Invalid latitude or longitude values: {i}")
            res.append({})
            res[-1]["latLong"] = {"decimal": {"lattitude": i[0],
                                              "longitude": i[1]}}
            lat_dms, lon_dms = coordinates_decimal_to_dms(
                i[0], i[1])
            temp = dms_to_coordiname(lat_dms, lon_dms)
            res[-1]["coordiName"] = temp["Word"]

            if data.timezone:
                try:
                    res[-1]["timezone"] = timezoneObj.timezone_at(
                        lng=i[1], lat=i[0])
                except Exception as e:
                    res[-1]["timezone_error"] = str(e)

            if data.reverse_geocode:
                try:
                    apiCallCount += 1
                    location = await get_reverse_geocode_async(i[0], i[1])
                    if location is not None:
                        res[-1]["reverse_geocode"] = location.address
                    else:
                        res[-1]["reverse_geocode"] = "Coordinates not found"
                except Exception as e:
                    res[-1]["reverse_geocode_error"] = str(e)

        await handle_api_request_count(apiKeyDetails, apiCallCount)
        return res
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=e.detail if hasattr(e, 'detail') else "An unexpected error occurred.")
    # Your endpoint logic here


# Api Route to handle "/api/getLatLong"

@apiRouter.post("/api/getLatLong")
async def getLatlong(data: getLatLong, apiKeyDetails=Depends(get_api_key)):
    """
    Converts 'coordiName' to latitude and longitude, and optionally provides timezone and reverse geocode information.

    This endpoint processes a list of 'coordiName' values, converting each to its corresponding latitude and longitude
    in decimal format. It also handles optional requests for timezone and reverse geocode information for each coordinate pair.
    The function manages API request counts and ensures that the number of processed items does not exceed the configured limits.

    Normal - API request count is 1 . Can get max 20 lattitude and longitude and timezone per request. (api request count is 1)
    reverse_geocode : true - API request count is 1 + (1 * no of entries per request (max 5)) . Can get max 5 lattitude and longitude, timezone and reverse_geocode per request. (api request count is max  6)

    Args:
        data (getLatLong): A Pydantic model that includes the 'coordiName' values and flags for requesting additional information.
        apiKeyDetails (Depends): Dependency that extracts and validates the API key from the request.

    Returns:
        list: A list of dictionaries, each containing the latitude and longitude, and optionally timezone and reverse geocode information.

    Raises:
        HTTPException: For missing 'coordiName' data, invalid 'coordiName' values, or any unexpected error during processing.
    """
    try:
        if not data.coordiName:
            raise ValueError("Coordinate name data is required.")
        responsePerReq = configData["apiReqBucket"]
        apiCallCount = 1
        if data.reverse_geocode:
            responsePerReq = configData["apiReqBucketAdvanced"]
        res = []
        for i in data.coordiName[: responsePerReq]:
            res.append({})
            res[-1]["coordiName"] = i
            temp = coordiname_to_coordinate(i)
            if temp is None:
                raise ValueError(f"Invalid coordiName: {i}")
            res[-1]["latLong"] = temp
            longitude = res[-1]["latLong"]["decimal"]["longitude"]
            lattitude = res[-1]["latLong"]["decimal"]["lattitude"]
            if data.timezone:
                res[-1]["timezone"] = timezoneObj.timezone_at(
                    lng=longitude, lat=lattitude)
            if data.reverse_geocode:
                apiCallCount += 1
                location = await get_reverse_geocode_async(lattitude, longitude)
                if location is not None:
                    res[-1]["reverse_geocode"] = location.address
                else:
                    res[-1]["reverse_geocode"] = "Coordinates not found"
        await handle_api_request_count(apiKeyDetails, apiCallCount)
        return res
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=e.detail if hasattr(e, 'detail') else "An unexpected error occurred.")


# Api Route to handle "/api/geocode"
@apiRouter.post("/api/geocode")
async def geocode(data: geoCode, apiKeyDetails=Depends(get_api_key)):
    try:
        if not data.address:
            raise ValueError("Address data is required.")
        apiCallCount = 1
        responsePerReq = configData["apiReqBucketAdvanced"]
        res = []
        for i in data.address[:responsePerReq]:
            res.append({})
            apiCallCount += 1
            location = await get_geocode_async(i)
            if location is None:
                raise ValueError(
                    f"Latitude and longitude not found for address: {i}")
            dmsLatLong = coordinates_decimal_to_dms(
                location.latitude, location.longitude)
            temp = {"decimal": {"lattitude": location.latitude, "longitude": location.longitude}, "dms": {
                "lattitude": dmsLatLong[0], "longitude": dmsLatLong[1]}}
            res[-1]["latLong"] = temp
            if data.coordiName:
                res[-1]["coordiName"] = dms_to_coordiname(
                    dmsLatLong[0], dmsLatLong[1])["Word"]
            if data.timezone:
                res[-1]["timezone"] = timezoneObj.timezone_at(
                    lng=location.longitude, lat=location.latitude)
        await handle_api_request_count(apiKeyDetails, apiCallCount)
        return res
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=e.detail if hasattr(e, 'detail') else "An unexpected error occurred.")


# Reset usage today
async def reset_usage_today():
    await collection_apiKey.update_many({}, {"$set": {"usageToday": 0}})
    print("Usage today reset")


sheduler = AsyncIOScheduler()
sheduler.add_job(reset_usage_today, CronTrigger(
    hour=0, minute=0, second=0, timezone="UTC"))
