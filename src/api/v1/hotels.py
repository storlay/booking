from fastapi import APIRouter
from fastapi import Body
from fastapi import Query
from fastapi import status
from sqlalchemy.exc import NoResultFound
from starlette.status import HTTP_200_OK

from src.api.dependecies import DbTransactionDep
from src.api.dependecies import PaginationDep
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
async def get_hotels(
    pagination: PaginationDep,
    transaction: DbTransactionDep,
    title: str = Query(
        None,
        description="Hotel's title",
    ),
    location: str = Query(
        None,
        description="Hotel's location",
    ),
) -> list[HotelSchema]:
    return await transaction.hotels.get_all(
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
