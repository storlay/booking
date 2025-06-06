from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel
from pydantic import ConfigDict


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
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class PartialUpdateHotelSchema(BaseModel):
    title: Annotated[
        str | None,
        MaxLen(100),
    ]
    location: Annotated[
        str | None,
        MaxLen(1000),
    ]
