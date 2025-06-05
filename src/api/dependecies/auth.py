from typing import Annotated
from typing import Callable

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from src.api.dependecies.utils import validate_jwt_type
from src.config.config import settings
from src.db.database import async_session
from src.exceptions.auth import IncorrectAuthCredsException
from src.exceptions.auth import InvalidAuthTokenException
from src.repositories.users import UsersRepository
from src.schemas.users import UserAuthSchema
from src.schemas.users import UserSchema
from src.services.auth import AuthService
from src.services.jwt import JWTService


async def authenticate_user(
    data: UserAuthSchema,
) -> UserSchema:
    print(f"{data.password=}")
    async with async_session() as session:
        user = await UsersRepository(session).get_one_or_none_with_password(
            email=data.email,
        )
    if not user:
        raise IncorrectAuthCredsException
    if not AuthService.check_password(data.password, user.password):
        raise IncorrectAuthCredsException
    return user


def get_token_payload(
    token_data: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> dict:
    try:
        return JWTService.decode(token_data.credentials)
    except jwt.exceptions.InvalidTokenError:
        raise InvalidAuthTokenException


def get_current_user_by_token_type(token_type: str) -> Callable:
    async def get_user_from_payload(
        payload: dict = Depends(get_token_payload),
    ) -> UserSchema:
        validate_jwt_type(payload, token_type)
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidAuthTokenException

        user_id = int(user_id)
        async with async_session() as session:
            user = await UsersRepository(session).get_one_or_none(id=user_id)
        if not user:
            raise InvalidAuthTokenException
        return user

    return get_user_from_payload


AuthenticateUserDep = Annotated[
    UserSchema,
    Depends(authenticate_user),
]
CurrentUserDep = Annotated[
    UserSchema,
    Depends(get_current_user_by_token_type(settings.jwt.ACCESS_TOKEN_TYPE)),
]
CurrentUserForRefreshDep = Annotated[
    UserSchema,
    Depends(get_current_user_by_token_type(settings.jwt.REFRESH_TOKEN_TYPE)),
]
