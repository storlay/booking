from fastapi import status

from src.exceptions.api.base import BaseHTTPException


class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Room not found"


class AllRoomsAlreadyBookedHTTPException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "All available rooms already booked"
