from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel

from src.schemas.base import IntegerId


class FacilityCreateSchema(BaseModel):
    title: Annotated[
        str,
        MaxLen(100),
    ]


class FacilitySchema(FacilityCreateSchema):
    id: IntegerId


class RoomFacilityAddSchema(BaseModel):
    room_id: IntegerId
    facility_id: IntegerId


class RoomFacilitySchema(RoomFacilityAddSchema):
    id: IntegerId
