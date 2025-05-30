from fastapi import APIRouter
from fastapi import Body
from fastapi import Query
from sqlalchemy import insert
from sqlalchemy import select

from src.api.dependecies import PaginationDep
from src.db.database import async_session
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import CreateHotelSchema
from src.schemas.hotels import PartialUpdateHotelSchema


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
def delete_hotel(
    hotel_id: int,
):
    pass


@router.post("/")
async def add_hotel(
    data: CreateHotelSchema = Body(
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
    data = data.model_dump()
    async with async_session() as session:
        result = await HotelsRepository(session).add(data)
        await session.commit()
    return {
        "status": "OK",
        "data": result,
    }


@router.put("/{hotel_id}")
def update_hotel(
    hotel_id: int,
    title: str = Body(
        description="Hotel's title to update.",
    ),
    name: str = Body(
        description="Hotel's name to update.",
    ),
):
    pass


@router.patch("/{hotel_id}")
def update_hotel_partial(
    hotel_id: int,
    data: PartialUpdateHotelSchema,
):
    pass
