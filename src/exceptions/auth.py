from fastapi import status

from src.exceptions.base import BaseHTTPException


class IncorrectAuthCredsException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"
