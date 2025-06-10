from typing import Annotated

from fastapi import Depends

from src.schemas.rooms import RoomsQueryParamsSchema


RoomsParamsDep = Annotated[RoomsQueryParamsSchema, Depends()]
