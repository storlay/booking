from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel
from pydantic import ConfigDict


class FacilityCreateSchema(BaseModel):
    title: Annotated[
        str,
        MaxLen(100),
    ]


class FacilitySchema(FacilityCreateSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
