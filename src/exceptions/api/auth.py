from fastapi import status

from src.exceptions.api.base import BaseHTTPException


class IncorrectAuthCredsException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class InvalidAuthTokenException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid auth token"


class UserAlreadyExistsException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User with this email already exists"
