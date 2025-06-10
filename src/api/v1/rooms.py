from fastapi import APIRouter
from fastapi import Body
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from src.api.dependecies import DbTransactionDep
from src.api.dependecies import PaginationDep
from src.api.dependecies import RoomsParamsDep
from src.exceptions.hotels import HotelNotFoundException
from src.exceptions.rooms import RoomNotFoundException
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.base import BaseSuccessResponseSchema
from src.schemas.rooms import RoomCreateRequestSchema
from src.schemas.rooms import RoomCreateSchema
from src.schemas.rooms import RoomPartiallyUpdateSchema
from src.schemas.rooms import RoomSchema
from src.schemas.rooms import RoomUpdateSchema


router = APIRouter(
    prefix="/hotels",
    tags=["Rooms"],
)


@router.get(
    "/{hotel_id}/rooms",
    response_model=list[RoomSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_hotel_rooms(
    transaction: DbTransactionDep,
    pagination: PaginationDep,
    params: RoomsParamsDep,
) -> list[RoomSchema]:
    return await transaction.rooms.get_available_for_hotel(
        hotel_id=params.hotel_id,
        date_from=params.date_from,
        date_to=params.date_to,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    response_model=RoomSchema,
    status_code=status.HTTP_200_OK,
    responses={
        RoomNotFoundException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": RoomNotFoundException.detail,
        },
    },
)
async def get_hotel_room(
    hotel_id: int,
    room_id: int,
    transaction: DbTransactionDep,
) -> RoomSchema:
    try:
        return await transaction.rooms.get_one(
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
    data: RoomCreateRequestSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Luxe",
                "value": {
                    "title": "Luxe",
                    "description": "Super Luxe apartment",
                    "price": 12121,
                    "quantity": 2,
                },
            }
        }
    ),
) -> RoomSchema:
    data = RoomCreateSchema(
        hotel_id=hotel_id,
        **data.model_dump(),
    )
    try:
        result = await transaction.rooms.add(data)
        await transaction.commit()
    except IntegrityError:
        raise HotelNotFoundException
    return result


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
    data: RoomUpdateSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Luxe",
                "value": {
                    "title": "Other Luxe",
                    "description": "Very very luxe apartment",
                    "price": 999,
                    "quantity": 1,
                },
            }
        }
    ),
) -> BaseSuccessResponseSchema:
    try:
        await transaction.rooms.update_one(
            data,
            hotel_id=hotel_id,
            id=room_id,
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
    data: RoomPartiallyUpdateSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Luxe",
                "value": {
                    "price": 12111,
                },
            }
        }
    ),
) -> BaseSuccessResponseSchema:
    try:
        await transaction.rooms.update_one(
            data,
            partially=True,
            hotel_id=hotel_id,
            id=room_id,
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
