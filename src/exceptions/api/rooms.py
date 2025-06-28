from fastapi import status

from src.exceptions.api.base import BaseHTTPException


class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Room not found"


class InvalidRoomFacilitiesHTTPException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid room facilities"
