from fastapi import status

from src.exceptions.base import BaseHTTPException


class HotelNotFoundException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Hotel not found"


class MultipleHotelsFoundException(BaseHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Found many hotels, expected one"
