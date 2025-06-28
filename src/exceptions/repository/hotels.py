from src.exceptions.repository.base import BaseRepoException


class ObjectNotFoundRepoException(BaseRepoException):
    detail = "Object not found"


class CannotAddObjectRepoException(BaseRepoException):
    detail = "Cannot add object"