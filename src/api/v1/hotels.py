from fastapi import APIRouter
from fastapi import Body
from fastapi import Query
from fastapi import status
from sqlalchemy.exc import NoResultFound
from starlette.status import HTTP_200_OK

from src.api.dependecies import PaginationDep
from src.db.database import async_session
from src.exceptions.hotels import HotelNotFoundException
from src.repositories.hotels import HotelsRepository
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
    "/",
    response_model=list[HotelSchema],
    status_code=status.HTTP_200_OK,
)
async def get_hotels(
    pagination: PaginationDep,
    title: str = Query(
        None,
        description="Hotel's title",
    ),
    location: str = Query(
        None,
        description="Hotel's location",
    ),
) -> list[HotelSchema]:
    async with async_session() as session:
        return await HotelsRepository(session).get_all(
            title,
            location,
            pagination.limit,
            pagination.offset,
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
async def get_hotel(
    hotel_id: int,
) -> HotelSchema:
    async with async_session() as session:
        try:
            return await HotelsRepository(session).get_one(
                id=hotel_id,
            )
        except NoResultFound:
            raise HotelNotFoundException


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
) -> BaseSuccessResponseSchema:
    async with async_session() as session:
        try:
            await HotelsRepository(session).delete_one(
                id=hotel_id,
            )
            await session.commit()
        except NoResultFound:
            raise HotelNotFoundException
    return BaseSuccessResponseSchema()


@router.post(
    "/",
    response_model=HotelSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_hotel(
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
    async with async_session() as session:
        result = await HotelsRepository(session).add(data)
        await session.commit()
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
    async with async_session() as session:
        try:
            await HotelsRepository(session).update_one(
                data,
                id=hotel_id,
            )
            await session.commit()
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
    async with async_session() as session:
        try:
            await HotelsRepository(session).update_one(
                data,
                partially=True,
                id=hotel_id,
            )
            await session.commit()
        except NoResultFound:
            raise HotelNotFoundException
    return BaseSuccessResponseSchema()
