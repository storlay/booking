from fastapi import APIRouter
from fastapi import status

from src.api.dependecies import AuthenticateUserDep
from src.api.dependecies import CurrentUserDep
from src.api.dependecies import CurrentUserForRefreshDep
from src.api.dependecies import DbTransactionDep
from src.exceptions.api.auth import IncorrectAuthCredsHTTPException
from src.exceptions.api.auth import InvalidAuthTokenHTTPException
from src.exceptions.api.auth import UserAlreadyExistsHTTPException
from src.schemas.auth import JWTInfoSchema
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.users import UserAuthSchema
from src.schemas.users import UserSchema
from src.services.auth import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication & Authorization"],
)


@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        UserAlreadyExistsHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": UserAlreadyExistsHTTPException.detail,
        },
    },
)
async def register_user(
    data: UserAuthSchema,
    transaction: DbTransactionDep,
) -> UserSchema:
    return await AuthService(transaction).register_user(
        data=data,
    )


@router.post(
    "/login",
    response_model=JWTInfoSchema,
    status_code=status.HTTP_200_OK,
    responses={
        IncorrectAuthCredsHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": IncorrectAuthCredsHTTPException.detail,
        },
    },
)
def login_user(
    user: AuthenticateUserDep,
) -> JWTInfoSchema:
    return AuthService().login_user(
        user_id=user.id,
    )


@router.post(
    "/refresh",
    response_model=JWTInfoSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses={
        InvalidAuthTokenHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": InvalidAuthTokenHTTPException.detail,
        },
    },
)
def refresh_jwt(
    user: CurrentUserForRefreshDep,
) -> JWTInfoSchema:
    return AuthService().refresh_jwt(
        user_id=user.id,
    )


@router.get(
    "/me",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    responses={
        InvalidAuthTokenHTTPException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": InvalidAuthTokenHTTPException.detail,
        },
    },
)
async def get_me(
    user: CurrentUserDep,
) -> UserSchema:
    return user
