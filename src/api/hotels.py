from fastapi import APIRouter
from fastapi import Body
from fastapi import Query
from sqlalchemy import insert
from sqlalchemy import select

from src.api.dependecies import PaginationDep
from src.db.database import async_session
from src.models.hotels import Hotels
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
    query = select(Hotels)
    if title:
        query = query.filter(Hotels.title.icontains(title))
    if location:
        query = query.filter(Hotels.location.icontains(location))
    query = query.limit(limit).offset(offset)
    async with async_session() as session:
        result = await session.execute(query)
    hotels = result.scalars().all()
    return hotels


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
    async with async_session() as session:
        add_hotel_stmt = insert(Hotels).values(**data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()


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
