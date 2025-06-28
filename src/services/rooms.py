from src.exceptions.api.hotels import HotelNotFoundHTTPException
from src.exceptions.api.rooms import InvalidRoomFacilitiesHTTPException
from src.exceptions.api.rooms import RoomNotFoundHTTPException
from src.exceptions.repository.hotels import CannotAddObjectRepoException
from src.exceptions.repository.hotels import ObjectNotFoundRepoException
from src.schemas.facilities import RoomFacilityAddSchema
from src.schemas.pagination import PaginationSchema
from src.schemas.rooms import RoomCreateRequestSchema
from src.schemas.rooms import RoomCreateSchema
from src.schemas.rooms import RoomPartiallyUpdateSchema
from src.schemas.rooms import RoomSchema
from src.schemas.rooms import RoomsQueryParamsSchema
from src.schemas.rooms import RoomUpdateSchema
from src.schemas.rooms import RoomWithRelsSchema
from src.services.base import BaseService


class RoomService(BaseService):
    async def get_all_hotel_rooms(
        self,
        pagination: PaginationSchema,
        params: RoomsQueryParamsSchema,
    ) -> list[RoomWithRelsSchema]:
        return await self.db.rooms.get_available_for_hotel(
            hotel_id=params.hotel_id,
            date_from=params.date_from,
            date_to=params.date_to,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    async def get_hotel_room(
        self,
        hotel_id: int,
        room_id: int,
    ) -> RoomWithRelsSchema:
        try:
            return await self.db.rooms.get_one_with_full_info(
                hotel_id=hotel_id,
                id=room_id,
            )
        except ObjectNotFoundRepoException:
            raise RoomNotFoundHTTPException

    async def add_room_to_hotel(
        self,
        hotel_id: int,
        data: RoomCreateRequestSchema,
    ) -> RoomSchema:
        room_data = RoomCreateSchema(
            hotel_id=hotel_id,
            **data.model_dump(),
        )
        try:
            room = await self.db.rooms.add(room_data)
        except CannotAddObjectRepoException:
            raise HotelNotFoundHTTPException

        if data.facilities_ids:
            facilities_to_assign = [
                RoomFacilityAddSchema(
                    room_id=room.id,
                    facility_id=facility_id,
                )
                for facility_id in data.facilities_ids
            ]
            try:
                await self.db.rooms_facilities.add_bulk(
                    facilities_to_assign,
                )
            except CannotAddObjectRepoException:
                raise InvalidRoomFacilitiesHTTPException

            await self.db.commit()
        return room

    async def update_hotel_room(
        self,
        hotel_id: int,
        room_id: int,
        data: RoomUpdateSchema,
    ) -> None:
        room_data = RoomCreateSchema(
            hotel_id=hotel_id,
            **data.model_dump(),
        )
        try:
            await self.db.rooms.update_one(
                room_data,
                hotel_id=hotel_id,
                id=room_id,
            )
            if data.facilities_ids is not None:
                await self.db.rooms_facilities.set_room_facilities(
                    room_id,
                    data.facilities_ids,
                )

            await self.db.commit()
        except ObjectNotFoundRepoException:
            raise RoomNotFoundHTTPException

    async def update_hotel_room_partial(
        self,
        hotel_id: int,
        room_id: int,
        data: RoomPartiallyUpdateSchema,
    ) -> None:
        try:
            await self.db.rooms.update_one(
                data,
                partially=True,
                hotel_id=hotel_id,
                id=room_id,
            )
            if data.facilities_ids is not None:
                await self.db.rooms_facilities.set_room_facilities(
                    room_id,
                    data.facilities_ids,
                )
            await self.db.commit()
        except ObjectNotFoundRepoException:
            raise RoomNotFoundHTTPException

    async def delete_hotel_room(
        self,
        hotel_id: int,
        room_id: int,
    ) -> None:
        try:
            await self.db.rooms.delete_one(
                hotel_id=hotel_id,
                id=room_id,
            )
            await self.db.commit()
        except ObjectNotFoundRepoException:
            raise RoomNotFoundHTTPException
