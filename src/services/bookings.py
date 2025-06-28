from src.exceptions.api.bookings import AllRoomsAlreadyBookedHTTPException
from src.exceptions.api.rooms import RoomNotFoundHTTPException
from src.exceptions.repository.bookings import RoomUnavailableRepoException
from src.exceptions.repository.hotels import ObjectNotFoundRepoException
from src.schemas.bookings import BookingCreateRequestSchema
from src.schemas.bookings import BookingCreateSchema
from src.schemas.bookings import BookingSchema
from src.schemas.pagination import PaginationSchema
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(
        self,
        pagination: PaginationSchema,
    ) -> list[BookingSchema]:
        return await self.db.bookings.get_all(
            pagination.limit,
            pagination.offset,
        )

    async def get_me_bookings(
        self,
        pagination: PaginationSchema,
        user_id: int,
    ) -> list[BookingSchema]:
        return await self.db.bookings.get_filtered(
            limit=pagination.limit,
            offset=pagination.offset,
            user_id=user_id,
        )

    async def create_booking(
        self,
        data: BookingCreateRequestSchema,
        user_id: int,
    ) -> BookingSchema:
        try:
            room = await self.db.rooms.get_one(id=data.room_id)
        except ObjectNotFoundRepoException:
            raise RoomNotFoundHTTPException

        data = BookingCreateSchema(
            user_id=user_id,
            price=room.price,
            **data.model_dump(),
        )
        try:
            booking = await self.db.bookings.add_booking(
                data,
                room.hotel_id,
            )
        except RoomUnavailableRepoException:
            raise AllRoomsAlreadyBookedHTTPException
        await self.db.commit()
        return booking
