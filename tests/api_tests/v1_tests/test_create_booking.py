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
            status.HTTP_409_CONFLICT,
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
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert response_data["date_from"] == date_from
        assert response_data["date_to"] == date_to
        assert response_data["room_id"] == room_id


@pytest.mark.parametrize(
    "room_id, date_from, date_to, bookings_count",
    [
        (
            ROOM_ID,
            date.today().isoformat(),
            (date.today() + timedelta(weeks=1)).isoformat(),
            i,
        )
        for i in range(1, ROOM_QUANTITY + 1)
    ],
)
async def test_create_and_get_me_bookings(
    room_id,
    date_from,
    date_to,
    bookings_count,
    clear_bookings,
    user_ac,
):
    create_booking_data = {
        "date_from": date_from,
        "date_to": date_to,
        "room_id": room_id,
    }
    create_booking_response = await user_ac.post(
        "/v1/bookings",
        json=create_booking_data,
    )
    assert create_booking_response.status_code == status.HTTP_201_CREATED

    get_me_bookings_response = await user_ac.get(
        "/v1/bookings/me",
        params={
            "page": 1,
            "per_page": ROOM_QUANTITY,
        },
    )
    assert get_me_bookings_response.status_code == status.HTTP_200_OK
    assert len(get_me_bookings_response.json()) == bookings_count
