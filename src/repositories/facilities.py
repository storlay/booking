from src.models.facilities import Facilities
from src.models.facilities import RoomsFacilities
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilitySchema
from src.schemas.facilities import RoomFacilitySchema


class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = FacilitySchema


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilities
    schema = RoomFacilitySchema
