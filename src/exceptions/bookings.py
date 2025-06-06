from fastapi import status

from src.exceptions.base import BaseHTTPException


class InvalidRoomIdForBookingException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid room id"
