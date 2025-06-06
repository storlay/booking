from fastapi import status

from src.exceptions.base import BaseHTTPException


class HotelNotFoundException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Hotel not found"
