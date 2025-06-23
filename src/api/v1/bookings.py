from fastapi import APIRouter
from fastapi import status
from fastapi_cache.decorator import cache
from sqlalchemy.exc import NoResultFound

from src.api.dependecies import CurrentUserDep
from src.api.dependecies import DbTransactionDep
from src.api.dependecies import PaginationDep
from src.exceptions.api.auth import InvalidAuthTokenHTTPException
from src.exceptions.api.bookings import InvalidRoomIdForBookingHTTPException
from src.exceptions.repository.bookings import RoomUnavailableException
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.bookings import BookingCreateRequestSchema
from src.schemas.bookings import BookingCreateSchema
from src.schemas.bookings import BookingSchema


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
    return await transaction.bookings.get_all(
        pagination.limit,
        pagination.offset,
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
    return await transaction.bookings.get_filtered(
        limit=pagination.limit,
        offset=pagination.offset,
        user_id=user.id,
    )


@router.post(
    "",
    response_model=BookingSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        InvalidRoomIdForBookingHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": InvalidRoomIdForBookingHTTPException.detail,
        },
        InvalidAuthTokenHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": InvalidAuthTokenHTTPException.detail,
        },
    },
)
async def create_booking(
    user: CurrentUserDep,
    transaction: DbTransactionDep,
    data: BookingCreateRequestSchema,
) -> BookingSchema:
    try:
        room = await transaction.rooms.get_one(id=data.room_id)
    except NoResultFound:
        raise InvalidRoomIdForBookingHTTPException

    data = BookingCreateSchema(
        user_id=user.id,
        price=room.price,
        **data.model_dump(),
    )
    try:
        result = await transaction.bookings.add_booking(data)
    except RoomUnavailableException:
        raise
    await transaction.commit()
    return result
