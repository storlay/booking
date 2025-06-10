from sqlalchemy import ColumnElement

from src.models.hotels import Hotels
from src.schemas.hotels import HotelsQueryParamsSchema


def get_hotels_filters_from_params(
    params: HotelsQueryParamsSchema,
) -> list[ColumnElement | None]:
    filters = []
    if params.title:
        filters.append(Hotels.title.icontains(params.title))
    if params.location:
        filters.append(Hotels.location.icontains(params.location))
    return filters
