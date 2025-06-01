from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class CreateOrUpdateHotelSchema(BaseModel):
    title: str
    location: str


class HotelSchema(CreateOrUpdateHotelSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class PartialUpdateHotelSchema(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
