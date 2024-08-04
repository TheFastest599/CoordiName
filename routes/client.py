from fastapi import HTTPException
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import jwt
import os
from models.clientData import ClientData, latLongDecimalContainer, latLongDMSContainer, ClientDataToken, ClientDataGetCoordiName, ClientDataGetLatLong
from core.coordianme_converter import coordinates_decimal_to_dms, dms_to_coordiname, coordiname_to_coordinate, coordinates_dms_to_decimal
from timezonefinder import TimezoneFinder


load_dotenv()
clientRouter = APIRouter()

timezoneObj = TimezoneFinder()


# route for handling client request
@clientRouter.post("/client_data")
async def get_client_data(data: ClientData):
    res = {}
    try:
        if data.getCoordiName:
            # Validate input data
            if "lat" not in data.latLong or "lon" not in data.latLong:
                raise ValueError("Latitude and longitude are required")
            if not (-90 <= data.latLong["lat"] <= 90) or not (-180 <= data.latLong["lon"] <= 180):
                raise ValueError(
                    f"Invalid latitude or longitude values: {data.latLong}")
            lat_dms, lon_dms = coordinates_decimal_to_dms(
                data.latLong["lat"], data.latLong["lon"])
            temp = dms_to_coordiname(lat_dms, lon_dms)
            res["coordiName"] = temp["Word"]
            if data.timezone:
                timezone = timezoneObj.timezone_at(
                    lng=data.latLong["lon"], lat=data.latLong["lat"])
                if timezone is None:
                    raise ValueError("Invalid coordinates for timezone lookup")
                res["timezone"] = timezone

        if data.getLatLong:
            if not data.coordiName:
                raise ValueError("CoordiName is required")
            temp = coordiname_to_coordinate(data.coordiName)
            if temp is None or "decimal" not in temp:
                raise ValueError("Invalid coordiName")
            res["latLong"] = temp
            if data.timezone:
                timezone = timezoneObj.timezone_at(
                    lng=res["latLong"]["decimal"]["longitude"], lat=res["latLong"]["decimal"]["lattitude"])
                if timezone is None:
                    raise ValueError("Invalid coordinates for timezone lookup")
                res["timezone"] = timezone
    except ValueError as e:
        # Handle specific errors, e.g., missing data or invalid conversions
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")

    return res


# route for handling client/getcoordiname request
@clientRouter.post("/client_data/getcoordiname")
async def get_coordiname(data: ClientDataGetCoordiName):
    res = {}
    try:
        # Validate input data
        if "lat" not in data.latLong or "lon" not in data.latLong:
            raise ValueError("Latitude and longitude are required")
        if not (-90 <= data.latLong["lat"] <= 90) or not (-180 <= data.latLong["lon"] <= 180):
            raise ValueError(
                f"Invalid latitude or longitude values: {data.latLong}")
        lat_dms, lon_dms = coordinates_decimal_to_dms(
            data.latLong["lat"], data.latLong["lon"])
        temp = dms_to_coordiname(lat_dms, lon_dms)
        res["coordiName"] = temp["Word"]
        if data.timezone:
            timezone = timezoneObj.timezone_at(
                lng=data.latLong["lon"], lat=data.latLong["lat"])
            if timezone is None:
                raise ValueError("Invalid coordinates for timezone lookup")
            res["timezone"] = timezone

    except ValueError as e:
        # Handle specific errors, e.g., missing data or invalid conversions
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")

    return res

# route for handling client/getlatlong request


@clientRouter.post("/client_data/getlatlong")
async def get_latlong(data: ClientDataGetLatLong):
    res = {}
    try:
        if not data.coordiName:
            raise ValueError("CoordiName is required")
        temp = coordiname_to_coordinate(data.coordiName)
        if temp is None or "decimal" not in temp:
            raise ValueError("Invalid coordiName")
        res["latLong"] = temp
        if data.timezone:
            timezone = timezoneObj.timezone_at(
                lng=res["latLong"]["decimal"]["longitude"], lat=res["latLong"]["decimal"]["lattitude"])
            if timezone is None:
                raise ValueError("Invalid coordinates for timezone lookup")
            res["timezone"] = timezone
    except ValueError as e:
        # Handle specific errors, e.g., missing data or invalid conversions
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")

    return res


# Secured route for handling client request
@clientRouter.post("/client_data_secured")
async def get_client_data_secured(data: ClientDataToken):
    try:
        # Decode the token
        data = jwt.decode(data.token, os.getenv(
            "JWT_SECRET"), algorithms=["HS256"])  # Decode the token
        data = ClientData(**data)
        res = {}
        if data.getCoordiName:
            lat_dms, lon_dms = coordinates_decimal_to_dms(
                data.latLong["lat"], data.latLong["lon"])
            temp = dms_to_coordiname(lat_dms, lon_dms)
            res["coordiName"] = temp["Word"]
        if data.getLatLong:
            temp = coordiname_to_coordinate(data.coordiName)
            res["latLong"] = temp
        return res
    except jwt.ExpiredSignatureError:
        # Handle expired token
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        # Handle invalid token
        raise HTTPException(status_code=401, detail="Invalid token")


@clientRouter.post("/client_data/latLong_decimal_to_dms")
async def decimal_to_dms(data: latLongDecimalContainer):
    lat, lon = coordinates_decimal_to_dms(data.lat, data.lon)
    return {lat, lon}


@clientRouter.post("/client_data/latLong_dms_to_decimal")
async def dms_to_decimal(data: latLongDMSContainer):
    lat, lon = coordinates_dms_to_decimal(data.lat, data.lon)
    return {lat, lon}
