from datetime import date

from fastapi import APIRouter
from fastapi import Body
from fastapi import status
from fastapi_cache.decorator import cache
from sqlalchemy.exc import NoResultFound
from starlette.status import HTTP_200_OK

from src.api.dependecies import CurrentUserDep
from src.api.dependecies import DbTransactionDep
from src.api.dependecies import HotelsParamsDep
from src.api.dependecies import PaginationDep
from src.api.v1.utils import get_hotels_filters_from_params
from src.exceptions.hotels import HotelNotFoundException
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.base import BaseSuccessResponseSchema
from src.schemas.hotels import HotelCreateOrUpdateSchema
from src.schemas.hotels import HotelSchema
from src.schemas.hotels import PartialUpdateHotelSchema


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get(
    "",
    response_model=list[HotelSchema],
    status_code=status.HTTP_200_OK,
)
@cache(expire=30)
async def get_hotels(
    _user: CurrentUserDep,
    pagination: PaginationDep,
    transaction: DbTransactionDep,
    params: HotelsParamsDep,
) -> list[HotelSchema]:
    filters = get_hotels_filters_from_params(params)
    return await transaction.hotels.get_filtered(
        pagination.limit,
        pagination.offset,
        *filters,
    )


@router.get(
    "/available",
    response_model=list[HotelSchema],
    status_code=status.HTTP_200_OK,
)
@cache(expire=15)
async def get_available_hotels(
    pagination: PaginationDep,
    transaction: DbTransactionDep,
    params: HotelsParamsDep,
    date_from: date,
    date_to: date,
) -> list[HotelSchema]:
    filters = get_hotels_filters_from_params(params)
    return await transaction.hotels.get_with_available_rooms(
        date_from,
        date_to,
        pagination.limit,
        pagination.offset,
        filters,
    )


@router.get(
    "/{hotel_id}",
    response_model=HotelSchema,
    status_code=status.HTTP_200_OK,
    responses={
        HotelNotFoundException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": HotelNotFoundException.detail,
        },
    },
)
@cache(expire=60)
async def get_hotel(
    hotel_id: int,
    transaction: DbTransactionDep,
) -> HotelSchema:
    try:
        return await transaction.hotels.get_one(
            id=hotel_id,
        )
    except NoResultFound:
        raise HotelNotFoundException


@router.post(
    "",
    response_model=HotelSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_hotel(
    transaction: DbTransactionDep,
    data: HotelCreateOrUpdateSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Dubai",
                "value": {
                    "title": "Dubai 5 stars",
                    "location": "Sheikh street, 1",
                },
            }
        }
    ),
) -> HotelSchema:
    result = await transaction.hotels.add(data)
    await transaction.commit()
    return result


@router.put(
    "/{hotel_id}",
    response_model=BaseSuccessResponseSchema,
    status_code=HTTP_200_OK,
    responses={
        HotelNotFoundException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": HotelNotFoundException.detail,
        },
    },
)
async def update_hotel(
    hotel_id: int,
    transaction: DbTransactionDep,
    data: HotelCreateOrUpdateSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Dubai",
                "value": {
                    "title": "Dubai 2 stars",
                    "location": "Sheikh street, 1212131",
                },
            }
        }
    ),
) -> BaseSuccessResponseSchema:
    try:
        await transaction.hotels.update_one(
            data,
            id=hotel_id,
        )
        await transaction.commit()
    except NoResultFound:
        raise HotelNotFoundException
    return BaseSuccessResponseSchema()


@router.patch(
    "/{hotel_id}",
    response_model=BaseSuccessResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={
        HotelNotFoundException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": HotelNotFoundException.detail,
        },
    },
)
async def update_hotel_partial(
    hotel_id: int,
    transaction: DbTransactionDep,
    data: PartialUpdateHotelSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Dubai",
                "value": {
                    "title": "Dubai Hotel",
                },
            }
        }
    ),
) -> BaseSuccessResponseSchema:
    try:
        await transaction.hotels.update_one(
            data,
            partially=True,
            id=hotel_id,
        )
        await transaction.commit()
    except NoResultFound:
        raise HotelNotFoundException
    return BaseSuccessResponseSchema()


@router.delete(
    "/{hotel_id}",
    response_model=BaseSuccessResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={
        HotelNotFoundException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": HotelNotFoundException.detail,
        },
    },
)
async def delete_hotel(
    hotel_id: int,
    transaction: DbTransactionDep,
) -> BaseSuccessResponseSchema:
    try:
        await transaction.hotels.delete_one(
            id=hotel_id,
        )
        await transaction.commit()
    except NoResultFound:
        raise HotelNotFoundException
    return BaseSuccessResponseSchema()
