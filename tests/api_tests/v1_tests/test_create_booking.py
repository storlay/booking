from datetime import date
from datetime import timedelta

import pytest
from fastapi import status

from tests.conftest import room_id_with_quantity


ROOM_ID, ROOM_QUANTITY = room_id_with_quantity()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (
            ROOM_ID,
            date.today().isoformat(),
            (date.today() + timedelta(weeks=1)).isoformat(),
            status.HTTP_201_CREATED,
        )
        for _ in range(ROOM_QUANTITY)
    ]
    + [
        (
            ROOM_ID,
            date.today().isoformat(),
            (date.today() + timedelta(weeks=1)).isoformat(),
            status.HTTP_400_BAD_REQUEST,
        )
    ],
)
async def test_create_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    user_ac,
    room,
):
    data_to_add = {
        "date_from": date_from,
        "date_to": date_to,
        "room_id": room_id,
    }
    response = await user_ac.post(
        "/v1/bookings",
        json=data_to_add,
    )
    print(response.json())
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert response_data["date_from"] == date_from
        assert response_data["date_to"] == date_to
        assert response_data["room_id"] == room_id
