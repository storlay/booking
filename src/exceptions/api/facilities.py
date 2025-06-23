from fastapi import status

from src.exceptions.api.base import BaseHTTPException


class FacilityAlreadyExistsException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Facility with this title already exists"
