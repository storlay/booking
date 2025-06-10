from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel
from pydantic import ConfigDict

from src.schemas.base import IntegerId


class FacilityCreateSchema(BaseModel):
    title: Annotated[
        str,
        MaxLen(100),
    ]


class FacilitySchema(FacilityCreateSchema):
    id: IntegerId

    model_config = ConfigDict(
        from_attributes=True,
    )
