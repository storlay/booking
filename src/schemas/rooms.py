from datetime import date
from typing import Annotated

from annotated_types import Ge
from annotated_types import MaxLen
from annotated_types import MinLen
from pydantic import BaseModel
from pydantic import ConfigDict

from src.schemas.base import PositiveDecimal


class RoomCreateRequestSchema(BaseModel):
    title: Annotated[
        str,
        MaxLen(100),
    ]
    description: Annotated[
        str | None,
        MinLen(10),
    ]
    price: PositiveDecimal
    quantity: Annotated[
        int,
        Ge(0),
    ]


class RoomCreateSchema(RoomCreateRequestSchema):
    hotel_id: int


class RoomSchema(RoomCreateSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


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
    quantity: Annotated[
        int | None,
        Ge(0),
    ] = None


class RoomsQueryParamsSchema(BaseModel):
    hotel_id: Annotated[
        int,
        Ge(1),
    ]
    date_from: date
    date_to: date
