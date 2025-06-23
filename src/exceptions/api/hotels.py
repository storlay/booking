from fastapi import status

from src.exceptions.api.base import BaseHTTPException


class HotelNotFoundHTTPException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Hotel not found"
