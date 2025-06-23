from datetime import date
from datetime import timedelta

from fastapi import status


async def test_create_booking(
    user_ac,
    room,
):
    date_from = date.today()
    date_to = date_from + timedelta(weeks=1)
    room_id = room.id
    data_to_add = {
        "date_from": date_from.isoformat(),
        "date_to": date_to.isoformat(),
        "room_id": room_id,
    }
    response = await user_ac.post(
        "/v1/bookings",
        json=data_to_add,
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert response_data["date_from"] == date_from.isoformat()
    assert response_data["date_to"] == date_to.isoformat()
    assert response_data["room_id"] == room_id
