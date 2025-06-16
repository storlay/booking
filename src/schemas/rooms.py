from datetime import date
from typing import Annotated

from annotated_types import MaxLen
from annotated_types import MinLen
from pydantic import BaseModel

from src.schemas.base import IntegerId
from src.schemas.base import PositiveDecimal
from src.schemas.base import PositiveInteger
from src.schemas.facilities import FacilitySchema


class RoomCreateRequestSchema(BaseModel):
    title: Annotated[
        str,
        MaxLen(100),
    ]
    price: PositiveDecimal
    quantity: PositiveInteger
    facilities_ids: list[IntegerId] | None = None
    description: Annotated[
        str | None,
        MinLen(10),
    ] = None


class RoomCreateSchema(BaseModel):
    hotel_id: IntegerId
    title: Annotated[
        str,
        MaxLen(100),
    ]
    price: PositiveDecimal
    quantity: PositiveInteger
    description: Annotated[
        str | None,
        MinLen(10),
    ]


class RoomSchema(RoomCreateSchema):
    id: IntegerId


class RoomWithRelsSchema(RoomSchema):
    facilities: list[FacilitySchema | None]


class RoomUpdateSchema(RoomCreateRequestSchema):
    pass


class RoomPartiallyUpdateSchema(BaseModel):
    title: Annotated[
        str | None,
        MaxLen(100),
    ] = None
    description: Annotated[
        str | None,
        MinLen(10),
    ] = None
    price: PositiveDecimal = None
    quantity: PositiveInteger | None = None
    facilities_ids: list[IntegerId] = None


class RoomsQueryParamsSchema(BaseModel):
    hotel_id: IntegerId
    date_from: date
    date_to: date
