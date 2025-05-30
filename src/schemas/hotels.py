from pydantic import BaseModel
from pydantic import Field


class CreateOrUpdateHotelSchema(BaseModel):
    title: str
    location: str


class PartialUpdateHotelSchema(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
