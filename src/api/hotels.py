from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Body
from fastapi import Query
from fastapi import status

from src.api.dependecies import PaginationDep
from src.db.database import async_session
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import CreateOrUpdateHotelSchema
from src.schemas.hotels import PartialUpdateHotelSchema
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.exc import NoResultFound


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/")
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
):
    limit = pagination.per_page
    offset = pagination.per_page * (pagination.page - 1)
    async with async_session() as session:
        return await HotelsRepository(session).get_all(
            title,
            location,
            limit,
            offset,
        )


@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int,
):
    async with async_session() as session:
        try:
            await HotelsRepository(session).delete_one(
                id=hotel_id,
            )
            await session.commit()
        except NoResultFound:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail={"message": "Hotel not found."},
            )
        except MultipleResultsFound:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail={"message": "Multiple hotels found."},
            )
    return {"status": "OK"}


@router.post("/")
async def add_hotel(
    data: CreateOrUpdateHotelSchema = Body(
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
):
    async with async_session() as session:
        result = await HotelsRepository(session).add(data)
        await session.commit()
    return {
        "status": "OK",
        "data": result,
    }


@router.put("/{hotel_id}")
async def update_hotel(
    hotel_id: int,
    data: CreateOrUpdateHotelSchema,
):
    async with async_session() as session:
        try:
            await HotelsRepository(session).update_one(
                data,
                id=hotel_id,
            )
            await session.commit()
        except NoResultFound:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail={"message": "Hotel not found."},
            )
        except MultipleResultsFound:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail={"message": "Multiple hotels found."},
            )
    return {"status": "OK"}


@router.patch("/{hotel_id}")
def update_hotel_partial(
    hotel_id: int,
    data: PartialUpdateHotelSchema,
):
    pass
