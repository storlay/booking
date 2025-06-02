from typing import Annotated

import jwt.exceptions
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status

from src.db.database import async_session
from src.repositories.users import UsersRepository
from src.schemas.pagination import PaginationParams
from src.schemas.users import UserSchema
from src.services.auth import AuthService


def get_access_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Token not provided.",
        )
    return access_token


async def get_current_user(
    access_token: str = Depends(get_access_token),
) -> UserSchema:
    try:
        token_payload = AuthService().decode_token(access_token)
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    user_id = token_payload["user_id"]
    async with async_session() as session:
        return await UsersRepository(session).get_one_or_none(id=user_id)


CurrentUserDep = Annotated[UserSchema, Depends(get_current_user)]
PaginationDep = Annotated[PaginationParams, Depends()]
