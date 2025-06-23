from fastapi import status

from src.exceptions.api.base import BaseHTTPException


class InvalidRoomIdForBookingHTTPException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid room id"
