from pydantic import BaseModel, Field


class getCoordiName(BaseModel):
    latLong: list[list[float]] = Field(
        default=None, example=[[26.1779, 91.7608], [28.6139, 77.2090]])
    timezone: bool = Field(default=False, example=True)
    reverse_geocode: bool = Field(default=False, example=True)


class getLatLong(BaseModel):
    coordiName: list[str] = Field(default=None, example=[
                                  "melon-communicate-macchiato-registration", "mint-negative-latte-convenience"])
    timezone: bool = Field(default=False, example=True)
    reverse_geocode: bool = Field(default=False, example=True)


class geoCode(BaseModel):
    address: list[str] = Field(default=None, example=[
        "Islumpur, Gandhi Basti, Guwahati, Kamrup Metropolitan, Assam, 781015, India",
        "Vijay Chowk, Raisina Hill, Chanakya Puri Tehsil, New Delhi, Delhi, India"
    ])
    coordiName: bool = Field(default=False, example=True)
    timezone: bool = Field(default=False, example=True)
