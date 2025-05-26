from fastapi import APIRouter
from fastapi import Body
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from src import storage
from src.schemas.hotels import CreateHotelSchema
from src.schemas.hotels import PartialUpdateHotelSchema


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/")
def get_hotels(
    page: int = Query(1, gt=0),
    per_page: int = Query(3, gt=0),
    name: str = Query(
        None,
        description="Hotel's name",
    ),
):
    if name:
        name = name.lower()
        # fmt: off
        result = [
            hotel
            for hotel in storage.HOTELS_DATA
            if name in hotel["name"].lower()
        ]
        # fmt: on
    else:
        result = storage.HOTELS_DATA
    offset = (page - 1) * per_page
    limit = offset + per_page
    return result[offset:limit]


@router.delete("/{hotel_id}")
def delete_hotel(
    hotel_id: int,
):
    # fmt: off
    storage.HOTELS_DATA = [
        hotel
        for hotel in storage.HOTELS_DATA
        if hotel["id"] != hotel_id
    ]
    # fmt: on
    return {"status": "ok"}


@router.post("/")
def add_hotel(
    data: CreateHotelSchema,
):
    storage.HOTELS_DATA.append(
        {
            "id": storage.HOTELS_DATA[-1]["id"] + 1,
            "title": data.title,
            "name": data.name,
        }
    )
    return {"status": "ok"}


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
    for hotel in storage.HOTELS_DATA:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {
                "status": "ok",
                "hotel_id": hotel_id,
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Hotel №{hotel_id} does not exists.",
    )


@router.patch("/{hotel_id}")
def update_hotel_partial(
    hotel_id: int,
    data: PartialUpdateHotelSchema,
):
    for hotel in storage.HOTELS_DATA:
        if hotel["id"] == hotel_id:
            if data.title is not None:
                hotel["title"] = data.title
            if data.name is not None:
                hotel["name"] = data.name
            return {
                "status": "ok",
                "hotel_id": hotel_id,
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Hotel №{hotel_id} does not exists.",
    )
