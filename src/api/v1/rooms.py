from fastapi import APIRouter
from fastapi import status
from fastapi_cache.decorator import cache
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from src.api.dependecies import DbTransactionDep
from src.api.dependecies import PaginationDep
from src.api.dependecies import RoomsParamsDep
from src.exceptions.api.hotels import HotelNotFoundException
from src.exceptions.api.rooms import RoomNotFoundException
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.base import BaseSuccessResponseSchema
from src.schemas.facilities import RoomFacilityAddSchema
from src.schemas.rooms import RoomCreateRequestSchema
from src.schemas.rooms import RoomCreateSchema
from src.schemas.rooms import RoomPartiallyUpdateSchema
from src.schemas.rooms import RoomSchema
from src.schemas.rooms import RoomUpdateSchema
from src.schemas.rooms import RoomWithRelsSchema


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
    return await transaction.rooms.get_available_for_hotel(
        hotel_id=params.hotel_id,
        date_from=params.date_from,
        date_to=params.date_to,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    response_model=RoomWithRelsSchema,
    status_code=status.HTTP_200_OK,
    responses={
        RoomNotFoundException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": RoomNotFoundException.detail,
        },
    },
)
@cache(expire=60)
async def get_hotel_room(
    hotel_id: int,
    room_id: int,
    transaction: DbTransactionDep,
) -> RoomWithRelsSchema:
    try:
        return await transaction.rooms.get_one_with_full_info(
            hotel_id=hotel_id,
            id=room_id,
        )
    except NoResultFound:
        raise RoomNotFoundException


@router.post(
    "/{hotel_id}/rooms",
    response_model=RoomSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        HotelNotFoundException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": HotelNotFoundException.detail,
        },
    },
)
async def add_room_to_hotel(
    hotel_id: int,
    transaction: DbTransactionDep,
    data: RoomCreateRequestSchema,
) -> RoomSchema:
    room_data = RoomCreateSchema(
        hotel_id=hotel_id,
        **data.model_dump(),
    )
    try:
        room = await transaction.rooms.add(room_data)
        if data.facilities_ids:
            facilities_to_assign = [
                RoomFacilityAddSchema(
                    room_id=room.id,
                    facility_id=facility_id,
                )
                for facility_id in data.facilities_ids
            ]
            await transaction.rooms_facilities.add_bulk(
                facilities_to_assign,
            )
        await transaction.commit()
    except IntegrityError:
        raise HotelNotFoundException
    return room


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    response_model=BaseSuccessResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={
        RoomNotFoundException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": RoomNotFoundException.detail,
        },
    },
)
async def update_hotel_room(
    hotel_id: int,
    room_id: int,
    transaction: DbTransactionDep,
    data: RoomUpdateSchema,
) -> BaseSuccessResponseSchema:
    room_data = RoomCreateSchema(
        hotel_id=hotel_id,
        **data.model_dump(),
    )
    try:
        await transaction.rooms.update_one(
            room_data,
            hotel_id=hotel_id,
            id=room_id,
        )
        if data.facilities_ids is not None:
            await transaction.rooms_facilities.set_room_facilities(
                room_id,
                data.facilities_ids,
            )

        await transaction.commit()
    except NoResultFound:
        raise RoomNotFoundException
    return BaseSuccessResponseSchema()


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    response_model=BaseSuccessResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={
        RoomNotFoundException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": RoomNotFoundException.detail,
        },
    },
)
async def update_hotel_room_partial(
    hotel_id: int,
    room_id: int,
    transaction: DbTransactionDep,
    data: RoomPartiallyUpdateSchema,
) -> BaseSuccessResponseSchema:
    try:
        await transaction.rooms.update_one(
            data,
            partially=True,
            hotel_id=hotel_id,
            id=room_id,
        )
        if data.facilities_ids is not None:
            await transaction.rooms_facilities.set_room_facilities(
                room_id,
                data.facilities_ids,
            )
        await transaction.commit()
    except NoResultFound:
        raise RoomNotFoundException
    return BaseSuccessResponseSchema()


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    response_model=BaseSuccessResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={
        RoomNotFoundException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": RoomNotFoundException.detail,
        },
    },
)
async def delete_hotel_room(
    hotel_id: int,
    room_id: int,
    transaction: DbTransactionDep,
) -> BaseSuccessResponseSchema:
    try:
        await transaction.rooms.delete_one(
            hotel_id=hotel_id,
            id=room_id,
        )
        await transaction.commit()
    except NoResultFound:
        raise RoomNotFoundException
    return BaseSuccessResponseSchema()
