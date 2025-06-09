from fastapi import APIRouter
from fastapi import status
from sqlalchemy.exc import NoResultFound

from src.api.dependecies import CurrentUserDep
from src.api.dependecies import DbTransactionDep
from src.exceptions.auth import InvalidAuthTokenException
from src.exceptions.bookings import InvalidRoomIdForBookingException
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.bookings import BookingCreateRequestSchema
from src.schemas.bookings import BookingCreateSchema
from src.schemas.bookings import BookingSchema


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get(
    "/",
    response_model=list[BookingSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_bookings(
    transaction: DbTransactionDep,
) -> list[BookingSchema]:
    return await transaction.bookings.get_all()


@router.get(
    "/me",
    response_model=list[BookingSchema],
    status_code=status.HTTP_200_OK,
)
async def get_me_bookings(
    user: CurrentUserDep,
    transaction: DbTransactionDep,
) -> list[BookingSchema]:
    return await transaction.bookings.get_filtered(user_id=user.id)


@router.post(
    "/",
    response_model=BookingSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        InvalidRoomIdForBookingException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": InvalidRoomIdForBookingException.detail,
        },
        InvalidAuthTokenException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": InvalidAuthTokenException.detail,
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
        raise InvalidRoomIdForBookingException

    data = BookingCreateSchema(
        user_id=user.id,
        price=room.price,
        **data.model_dump(),
    )
    result = await transaction.bookings.add(data)
    await transaction.commit()
    return result
