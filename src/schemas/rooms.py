from decimal import Decimal
from typing import Annotated

from annotated_types import Ge
from annotated_types import MaxLen
from annotated_types import MinLen
from pydantic import BaseModel
from pydantic import ConfigDict


class RoomCreateRequestSchema(BaseModel):
    title: Annotated[
        str,
        MaxLen(100),
    ]
    description: Annotated[
        str | None,
        MinLen(10),
    ]
    price: Annotated[
        Decimal,
        Ge(0),
    ]
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
    ]
    description: Annotated[
        str | None,
        MinLen(10),
    ]
    price: Annotated[
        Decimal | None,
        Ge(0),
    ]
    quantity: Annotated[
        int | None,
        Ge(0),
    ]
