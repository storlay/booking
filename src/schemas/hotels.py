from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel

from src.schemas.base import IntegerId


class HotelCreateOrUpdateSchema(BaseModel):
    title: Annotated[
        str,
        MaxLen(100),
    ]
    location: Annotated[
        str,
        MaxLen(1000),
    ]


class HotelSchema(HotelCreateOrUpdateSchema):
    id: IntegerId


class PartialUpdateHotelSchema(BaseModel):
    title: Annotated[
        str | None,
        MaxLen(100),
    ] = None
    location: Annotated[
        str | None,
        MaxLen(1000),
    ] = None


class HotelsQueryParamsSchema(PartialUpdateHotelSchema):
    title: Annotated[
        str | None,
        MaxLen(100),
    ] = None
    location: Annotated[
        str | None,
        MaxLen(1000),
    ] = None


class HotelIdSchema(BaseModel):
    hotel_id: IntegerId
