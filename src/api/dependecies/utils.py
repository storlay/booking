from src.config.config import settings
from src.exceptions.auth import InvalidAuthTokenException


def validate_jwt_type(
    payload: dict,
    valid_token_type: str,
) -> None:
    token_type = payload.get(settings.jwt.TOKEN_TYPE_FIELD)
    if token_type != valid_token_type:
        raise InvalidAuthTokenException
