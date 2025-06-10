from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select

from src.models.facilities import Facilities
from src.models.facilities import RoomsFacilities
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilitySchema
from src.schemas.facilities import RoomFacilityAddSchema
from src.schemas.facilities import RoomFacilitySchema


class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = FacilitySchema


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilities
    schema = RoomFacilitySchema

    async def set_room_facilities(
        self,
        room_id: int,
        facilities_ids: list[int],
    ):
        # fmt: off
        current_facilities_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        result = await self.session.execute(current_facilities_query)
        current_facilities_ids = result.scalars().all()
        ids_to_delete = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert = list(set(facilities_ids) - set(current_facilities_ids))
        if ids_to_delete:
            stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete),
                )
            )
            await self.session.execute(stmt)
        if ids_to_insert:
            to_add = [
                RoomFacilityAddSchema(
                    facility_id=facility_id,
                    room_id=room_id,
                ).model_dump()
                for facility_id in ids_to_insert
            ]
            stmt = insert(self.model).values(to_add)
            await self.session.execute(stmt)
        # fmt: on
