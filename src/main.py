from fastapi import Body
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from . import storage

app = FastAPI(
    title="Booking API",
)


@app.get("/hotels")
def get_hotels(
    name: str = Query(
        None,
        description="Hotel's name",
    ),
):
    if name:
        name = name.lower()
        # fmt: off
        return [
            hotel
            for hotel in storage.HOTELS_DATA
            if name in hotel["name"].lower()
        ]
        # fmt: on
    return storage.HOTELS_DATA


@app.delete("/hotels/{hotel_id}")
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


@app.post("/hotels")
def add_hotel(
    title: str = Body(
        embed=True,
        description="Hotel's title.",
    ),
):
    storage.HOTELS_DATA.append(
        {
            "id": storage.HOTELS_DATA[-1]["id"] + 1,
            "name": title,
        }
    )
    return {"status": "ok"}


@app.put("/hotels/{hotel_id}")
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


@app.patch("/hotels/{hotel_id}")
def update_hotel_partial(
    hotel_id: int,
    title: str | None = Body(
        None,
        description="Hotel's title to update.",
    ),
    name: str | None = Body(
        None,
        description="Hotel's name to update.",
    ),
):
    for hotel in storage.HOTELS_DATA:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {
                "status": "ok",
                "hotel_id": hotel_id,
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Hotel №{hotel_id} does not exists.",
    )
