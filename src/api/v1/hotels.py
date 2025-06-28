from datetime import date

from fastapi import APIRouter
from fastapi import Body
from fastapi import status
from fastapi_cache.decorator import cache

from src.api.dependecies import CurrentUserDep
from src.api.dependecies import DbTransactionDep
from src.api.dependecies import HotelsParamsDep
from src.api.dependecies import PaginationDep
from src.exceptions.api.hotels import HotelNotFoundHTTPException
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.hotels import HotelCreateOrUpdateSchema
from src.schemas.hotels import HotelIdSchema
from src.schemas.hotels import HotelSchema
from src.schemas.hotels import PartialUpdateHotelSchema
from src.services.hotels import HotelService


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
    return await HotelService(transaction).get_hotels(
        params,
        pagination,
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
    return await HotelService(transaction).get_available_hotels(
        date_from,
        date_to,
        params,
        pagination,
    )


@router.get(
    "/{hotel_id}",
    response_model=HotelSchema,
    status_code=status.HTTP_200_OK,
    responses={
        HotelNotFoundHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": HotelNotFoundHTTPException.detail,
        },
    },
)
@cache(expire=60)
async def get_hotel(
    hotel_id: int,
    transaction: DbTransactionDep,
) -> HotelSchema:
    return await HotelService(transaction).get_hotel(
        hotel_id=hotel_id,
    )


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
    return await HotelService(transaction).add_hotel(
        data=data,
    )


@router.put(
    "/{hotel_id}",
    response_model=HotelIdSchema,
    status_code=status.HTTP_200_OK,
    responses={
        HotelNotFoundHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": HotelNotFoundHTTPException.detail,
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
) -> HotelIdSchema:
    await HotelService(transaction).update_hotel(
        hotel_id=hotel_id,
        data=data,
    )
    return HotelIdSchema(hotel_id=hotel_id)


@router.patch(
    "/{hotel_id}",
    response_model=HotelIdSchema,
    status_code=status.HTTP_200_OK,
    responses={
        HotelNotFoundHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": HotelNotFoundHTTPException.detail,
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
) -> HotelIdSchema:
    await HotelService(transaction).update_hotel_partial(
        data=data,
        hotel_id=hotel_id,
    )
    return HotelIdSchema(hotel_id=hotel_id)


@router.delete(
    "/{hotel_id}",
    response_model=HotelIdSchema,
    status_code=status.HTTP_200_OK,
    responses={
        HotelNotFoundHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": HotelNotFoundHTTPException.detail,
        },
    },
)
async def delete_hotel(
    hotel_id: int,
    transaction: DbTransactionDep,
) -> HotelIdSchema:
    await HotelService(transaction).delete_hotel(hotel_id=hotel_id)
    return HotelIdSchema(hotel_id=hotel_id)
