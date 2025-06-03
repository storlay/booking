from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

from src.config.config import settings


class PaginationParams(BaseModel):
    page: Annotated[
        int,
        Query(
            1,
            ge=1,
        ),
    ]
    per_page: Annotated[
        int,
        Query(
            3,
            ge=1,
            le=settings.pagination.MAX_ENTITIES_PER_PAGE,
        ),
    ]
