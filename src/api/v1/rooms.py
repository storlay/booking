from fastapi import APIRouter
from fastapi import Body
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from src.api.dependecies import PaginationDep
from src.db.database import async_session
from src.exceptions.hotels import HotelNotFoundException
from src.exceptions.rooms import RoomNotFoundException
from src.repositories.rooms import RoomsRepository
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
    pagination: PaginationDep,
    hotel_id: int,
) -> list[RoomSchema]:
    async with async_session() as session:
        return await RoomsRepository(session).get_all_for_hotel(
            hotel_id,
            pagination.limit,
            pagination.offset,
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
) -> RoomSchema:
    async with async_session() as session:
        try:
            return await RoomsRepository(session).get_one(
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
    data: RoomCreateRequestSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Luxe",
                "value": {
                    "title": "Luxe",
                    "description": "Super Luxe apartment",
                    "price": 1221212121,
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
    async with async_session() as session:
        try:
            result = await RoomsRepository(session).add(data)
            await session.commit()
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
    data: RoomUpdateSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Luxe",
                "value": {
                    "title": "Other Luxe",
                    "description": "Very very luxe apartment",
                    "price": 9999999,
                    "quantity": 1,
                },
            }
        }
    ),
) -> BaseSuccessResponseSchema:
    async with async_session() as session:
        try:
            await RoomsRepository(session).update_one(
                data,
                hotel_id=hotel_id,
                id=room_id,
            )
            await session.commit()
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
    data: RoomPartiallyUpdateSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Luxe",
                "value": {
                    "price": 9999999,
                },
            }
        }
    ),
) -> BaseSuccessResponseSchema:
    async with async_session() as session:
        try:
            await RoomsRepository(session).update_one(
                data,
                partially=True,
                hotel_id=hotel_id,
                id=room_id,
            )
            await session.commit()
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
) -> BaseSuccessResponseSchema:
    async with async_session() as session:
        try:
            await RoomsRepository(session).delete_one(
                hotel_id=hotel_id,
                id=room_id,
            )
            await session.commit()
        except NoResultFound:
            raise RoomNotFoundException
    return BaseSuccessResponseSchema()
