from src.models.facilities import Facilities
from src.models.facilities import RoomsFacilities
from src.repositories.mappers.base import BaseDataMapper
from src.schemas.facilities import FacilitySchema
from src.schemas.facilities import RoomFacilitySchema


class FacilitiesDataMapper(BaseDataMapper):
    schema = FacilitySchema
    model = Facilities


class RoomsFacilitiesDataMapper(BaseDataMapper):
    schema = RoomFacilitySchema
    model = RoomsFacilities
