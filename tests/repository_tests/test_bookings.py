from datetime import date
from datetime import timedelta

from pydantic import BaseModel

from src.schemas.bookings import BookingCreateSchema
from src.schemas.bookings import BookingUpdateSchema


async def test_bookings_crud(
    db,
    room,
    user,
):
    data_to_create = BookingCreateSchema(
        user_id=user.id,
        price=room.price,
        date_from=date(year=2025, month=1, day=1),
        date_to=date(year=2025, month=2, day=2),
        room_id=room.id,
    )
    created_booking = await db.bookings.add(data_to_create)
    assert isinstance(created_booking, BaseModel)
    assert created_booking.user_id == data_to_create.user_id
    assert created_booking.price == data_to_create.price
    assert created_booking.date_from == data_to_create.date_from
    assert created_booking.date_to == data_to_create.date_to
    assert created_booking.room_id == data_to_create.room_id

    received_booking = await db.bookings.get_one_or_none(id=created_booking.id)
    assert isinstance(received_booking, BaseModel)
    assert created_booking.user_id == received_booking.user_id
    assert created_booking.price == received_booking.price
    assert created_booking.date_from == received_booking.date_from
    assert created_booking.date_to == received_booking.date_to
    assert created_booking.room_id == received_booking.room_id

    data_to_update = BookingUpdateSchema(
        date_from=data_to_create.date_from + timedelta(weeks=1),
        date_to=data_to_create.date_to + timedelta(weeks=1),
    )
    updated_booking_id = await db.bookings.update_one(
        data_to_update,
        id=received_booking.id,
    )
    assert type(updated_booking_id) == int
    assert updated_booking_id == received_booking.id
    updated_booking = await db.bookings.get_one_or_none(id=updated_booking_id)
    assert updated_booking.date_from == data_to_update.date_from
    assert updated_booking.date_to == data_to_update.date_to

    deleted_booking_id = await db.bookings.delete_one(id=updated_booking.id)
    assert type(updated_booking_id) == int
    deleted_booking = await db.bookings.get_one_or_none(id=deleted_booking_id)
    assert deleted_booking is None
