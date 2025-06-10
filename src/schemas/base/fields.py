from decimal import Decimal
from typing import Annotated

from annotated_types import Ge
from annotated_types import Le

from src.config import settings


PositiveDecimal = Annotated[
    Decimal,
    Ge(0),
    Le(settings.models.MAX_DECIMAL_VALUE),
]
PositiveInteger = Annotated[
    int,
    Ge(0),
]
IntegerId = Annotated[
    int,
    Ge(1),
]
