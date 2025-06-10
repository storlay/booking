from typing import Annotated

from fastapi import Depends

from src.schemas.hotels import HotelsQueryParamsSchema


HotelsParamsDep = Annotated[HotelsQueryParamsSchema, Depends()]
