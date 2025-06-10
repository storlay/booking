from fastapi import APIRouter
from fastapi import status
from sqlalchemy.exc import IntegrityError

from src.api.dependecies import DbTransactionDep
from src.api.dependecies import PaginationDep
from src.exceptions.facilities import FacilityAlreadyExistsException
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.facilities import FacilityCreateSchema
from src.schemas.facilities import FacilitySchema


router = APIRouter(
    prefix="/facilities",
    tags=["Facilities"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[FacilitySchema],
)
async def get_all_facilities(
    transaction: DbTransactionDep,
    pagination: PaginationDep,
) -> list[FacilitySchema]:
    return await transaction.facilities.get_all(
        pagination.limit,
        pagination.offset,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=FacilitySchema,
    responses={
        FacilityAlreadyExistsException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": FacilityAlreadyExistsException.detail,
        },
    },
)
async def create_facility(
    transaction: DbTransactionDep,
    data: FacilityCreateSchema,
) -> FacilitySchema:
    try:
        result = await transaction.facilities.add(data)
        await transaction.commit()
        return result
    except IntegrityError:
        raise FacilityAlreadyExistsException
