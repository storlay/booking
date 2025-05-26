from pydantic import BaseModel
from pydantic import Field


class CreateHotelSchema(BaseModel):
    title: str
    name: str


class PartialUpdateHotelSchema(BaseModel):
    title: str | None = Field(None)
    name: str | None = Field(None)
