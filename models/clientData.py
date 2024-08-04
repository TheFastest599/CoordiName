from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ClientData(BaseModel):
    latLong: Optional[Dict[str, Optional[float]]] = Field(
        default=None, example={"lat": 26.177979069330007, "lon": 91.76085595487656},  description="Latitude and Longitude")
    coordiName: str = Field(
        default=None, example='melon-communicate-macchiato-registration', description="Name of the coordinates")
    getCoordiName: bool = False
    getLatLong: bool = False
    timezone: bool = False


class ClientDataGetCoordiName(BaseModel):
    latLong: Optional[Dict[str, Optional[float]]] = Field(
        default=None, example={"lat": 26.177979069330007, "lon": 91.76085595487656},  description="Latitude and Longitude")
    timezone: bool = False


class ClientDataGetLatLong(BaseModel):
    coordiName: str = Field(
        default=None, example='melon-communicate-macchiato-registration', description="Name of the coordinates")
    timezone: bool = False


class ClientDataToken(BaseModel):
    token: str


class latLongDecimalContainer(BaseModel):
    lat: float = Field(default=None, example=34.205,
                       description=" Give decimal lattitude in example format")
    lon: float = Field(default=None, example=-118.375,
                       description=" Give decimal longitude in example format")


class latLongDMSContainer(BaseModel):
    lat: list[Any] = Field(default=None, example=[
                           34, 12, 18, 'N'], description="Give dms lattitude in example format")
    lon: list[Any] = Field(default=None, example=[
                           118, 22, 30, 'W'], description="Give dms longitude in example format")
