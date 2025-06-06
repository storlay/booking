from decimal import Decimal
from typing import Annotated

from annotated_types import Ge
from annotated_types import Le
from pydantic import BaseModel

from src.config.config import settings


class BaseSuccessResponseSchema(BaseModel):
    status: str = "ok"


class BaseHTTPExceptionSchema(BaseModel):
    detail: str


PositiveDecimal = Annotated[
    Decimal,
    Ge(0),
    Le(settings.models.MAX_DECIMAL_VALUE),
]
