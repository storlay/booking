from fastapi import status

from src.exceptions.base import BaseHTTPException


class RoomNotFoundException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Room not found"
