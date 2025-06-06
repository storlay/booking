from src.models.bookings import Bookings
from src.repositories.base import BaseRepository
from src.schemas.bookings import BookingSchema


class BookingsRepository(BaseRepository):
    model = Bookings
    schema = BookingSchema
