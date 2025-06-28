from fastapi import APIRouter
from fastapi import status
from fastapi_cache.decorator import cache

from src.api.dependecies import DbTransactionDep
from src.api.dependecies import PaginationDep
from src.api.dependecies import RoomsParamsDep
from src.exceptions.api.hotels import HotelNotFoundHTTPException
from src.exceptions.api.rooms import RoomNotFoundHTTPException
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.rooms import RoomCreateRequestSchema
from src.schemas.rooms import RoomIdSchema
from src.schemas.rooms import RoomPartiallyUpdateSchema
from src.schemas.rooms import RoomSchema
from src.schemas.rooms import RoomUpdateSchema
from src.schemas.rooms import RoomWithRelsSchema
from src.services.rooms import RoomService


router = APIRouter(
    prefix="/hotels",
    tags=["Rooms"],
)


@router.get(
    "/{hotel_id}/rooms",
    response_model=list[RoomWithRelsSchema],
    status_code=status.HTTP_200_OK,
)
@cache(expire=60)
async def get_all_hotel_rooms(
    transaction: DbTransactionDep,
    pagination: PaginationDep,
    params: RoomsParamsDep,
) -> list[RoomWithRelsSchema]:
    return await RoomService(transaction).get_all_hotel_rooms(
        pagination=pagination,
        params=params,
    )


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    response_model=RoomWithRelsSchema,
    status_code=status.HTTP_200_OK,
    responses={
        RoomNotFoundHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": RoomNotFoundHTTPException.detail,
        },
    },
)
@cache(expire=60)
async def get_hotel_room(
    hotel_id: int,
    room_id: int,
    transaction: DbTransactionDep,
) -> RoomWithRelsSchema:
    return await RoomService(transaction).get_hotel_room(
        hotel_id=hotel_id,
        room_id=room_id,
    )


@router.post(
    "/{hotel_id}/rooms",
    response_model=RoomSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        HotelNotFoundHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": HotelNotFoundHTTPException.detail,
        },
    },
)
async def add_room_to_hotel(
    hotel_id: int,
    transaction: DbTransactionDep,
    data: RoomCreateRequestSchema,
) -> RoomSchema:
    return await RoomService(transaction).add_room_to_hotel(
        hotel_id=hotel_id,
        data=data,
    )


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    response_model=RoomIdSchema,
    status_code=status.HTTP_200_OK,
    responses={
        RoomNotFoundHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": RoomNotFoundHTTPException.detail,
        },
    },
)
async def update_hotel_room(
    hotel_id: int,
    room_id: int,
    transaction: DbTransactionDep,
    data: RoomUpdateSchema,
) -> RoomIdSchema:
    await RoomService(transaction).update_hotel_room(
        hotel_id=hotel_id,
        room_id=room_id,
        data=data,
    )
    return RoomIdSchema(room_id=room_id)


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    response_model=RoomIdSchema,
    status_code=status.HTTP_200_OK,
    responses={
        RoomNotFoundHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": RoomNotFoundHTTPException.detail,
        },
    },
)
async def update_hotel_room_partial(
    hotel_id: int,
    room_id: int,
    transaction: DbTransactionDep,
    data: RoomPartiallyUpdateSchema,
) -> RoomIdSchema:
    await RoomService(transaction).update_hotel_room_partial(
        hotel_id=hotel_id,
        room_id=room_id,
        data=data,
    )
    return RoomIdSchema(room_id=room_id)


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    response_model=RoomIdSchema,
    status_code=status.HTTP_200_OK,
    responses={
        RoomNotFoundHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": RoomNotFoundHTTPException.detail,
        },
    },
)
async def delete_hotel_room(
    hotel_id: int,
    room_id: int,
    transaction: DbTransactionDep,
) -> RoomIdSchema:
    await RoomService(transaction).delete_hotel_room(
        hotel_id=hotel_id,
        room_id=room_id,
    )
    return RoomIdSchema(room_id=room_id)
