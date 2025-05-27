from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int, Query(3, ge=1, le=100)]
