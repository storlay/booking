from src.models.bookings import Bookings
from src.repositories.base import BaseRepository
from src.repositories.mappers.bookings import BookingsDataMapper


class BookingsRepository(BaseRepository):
    model = Bookings
    mapper = BookingsDataMapper
