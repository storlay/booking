from fastapi import APIRouter
from fastapi import status
from fastapi_cache.decorator import cache

from src.api.dependecies import DbTransactionDep
from src.api.dependecies import PaginationDep
from src.exceptions.api.facilities import FacilityAlreadyExistsHTTPException
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.facilities import FacilityCreateSchema
from src.schemas.facilities import FacilitySchema
from src.services.facilities import FacilityService


router = APIRouter(
    prefix="/facilities",
    tags=["Facilities"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[FacilitySchema],
)
@cache(expire=60)
async def get_all_facilities(
    transaction: DbTransactionDep,
    pagination: PaginationDep,
) -> list[FacilitySchema]:
    return await FacilityService(transaction).get_all_facilities(
        pagination=pagination,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=FacilitySchema,
    responses={
        FacilityAlreadyExistsHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": FacilityAlreadyExistsHTTPException.detail,
        },
    },
)
async def create_facility(
    transaction: DbTransactionDep,
    data: FacilityCreateSchema,
) -> FacilitySchema:
    return await FacilityService(transaction).create_facility(
        data=data,
    )
