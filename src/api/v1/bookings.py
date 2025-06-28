from fastapi import APIRouter
from fastapi import status
from fastapi_cache.decorator import cache

from src.api.dependecies import CurrentUserDep
from src.api.dependecies import DbTransactionDep
from src.api.dependecies import PaginationDep
from src.exceptions.api.auth import InvalidAuthTokenHTTPException
from src.exceptions.api.bookings import AllRoomsAlreadyBookedHTTPException
from src.exceptions.api.rooms import RoomNotFoundHTTPException
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.bookings import BookingCreateRequestSchema
from src.schemas.bookings import BookingSchema
from src.services.bookings import BookingService


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get(
    "",
    response_model=list[BookingSchema],
    status_code=status.HTTP_200_OK,
)
@cache(10)
async def get_all_bookings(
    transaction: DbTransactionDep,
    pagination: PaginationDep,
) -> list[BookingSchema]:
    return await BookingService(transaction).get_all_bookings(
        pagination=pagination,
    )


@router.get(
    "/me",
    response_model=list[BookingSchema],
    status_code=status.HTTP_200_OK,
)
@cache(10)
async def get_me_bookings(
    user: CurrentUserDep,
    transaction: DbTransactionDep,
    pagination: PaginationDep,
) -> list[BookingSchema]:
    return await BookingService(transaction).get_me_bookings(
        pagination=pagination,
        user_id=user.id,
    )


@router.post(
    "",
    response_model=BookingSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        RoomNotFoundHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": RoomNotFoundHTTPException.detail,
        },
        InvalidAuthTokenHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": InvalidAuthTokenHTTPException.detail,
        },
        AllRoomsAlreadyBookedHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": AllRoomsAlreadyBookedHTTPException.detail,
        },
    },
)
async def create_booking(
    user: CurrentUserDep,
    transaction: DbTransactionDep,
    data: BookingCreateRequestSchema,
) -> BookingSchema:
    return await BookingService(transaction).create_booking(
        data=data,
        user_id=user.id,
    )
