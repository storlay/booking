from fastapi import status

from src.exceptions.api.base import BaseHTTPException


class AllRoomsAlreadyBookedHTTPException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "All available rooms already booked"
