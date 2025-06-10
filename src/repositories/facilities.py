from src.models.facilities import Facilities
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilitySchema


class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = FacilitySchema
