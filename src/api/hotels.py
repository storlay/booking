from fastapi import APIRouter
from fastapi import Body
from fastapi import Query

from src.api.dependecies import PaginationDep
from src.schemas.hotels import CreateHotelSchema
from src.schemas.hotels import PartialUpdateHotelSchema


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/")
def get_hotels(
    pagination: PaginationDep,
    name: str = Query(
        None,
        description="Hotel's name",
    ),
):
    pass


@router.delete("/{hotel_id}")
def delete_hotel(
    hotel_id: int,
):
    pass


@router.post("/")
def add_hotel(
    data: CreateHotelSchema,
):
    pass


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
