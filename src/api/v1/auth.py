from fastapi import APIRouter
from fastapi import status
from sqlalchemy.exc import IntegrityError

from src.api.dependecies import AuthenticateUserDep
from src.api.dependecies import CurrentUserDep
from src.api.dependecies import CurrentUserForRefreshDep
from src.api.dependecies import DbTransactionDep
from src.exceptions.auth import IncorrectAuthCredsException
from src.exceptions.auth import InvalidAuthTokenException
from src.exceptions.auth import UserAlreadyExistsException
from src.schemas.auth import JWTInfoSchema
from src.schemas.base import BaseHTTPExceptionSchema
from src.schemas.base import BaseSuccessResponseSchema
from src.schemas.users import UserAuthSchema
from src.schemas.users import UserSchema
from src.services.auth import AuthService
from src.services.jwt import JWTService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication & Authorization"],
)


@router.post(
    "/register",
    response_model=BaseSuccessResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        UserAlreadyExistsException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": UserAlreadyExistsException.detail,
        },
    },
)
async def register_user(
    data: UserAuthSchema,
    transaction: DbTransactionDep,
) -> BaseSuccessResponseSchema:
    data.password = AuthService.hash_password(data.password).decode("utf-8")
    try:
        await transaction.users.add(data)
        await transaction.commit()
    except IntegrityError:
        raise UserAlreadyExistsException
    return BaseSuccessResponseSchema()


@router.post(
    "/login",
    response_model=JWTInfoSchema,
    status_code=status.HTTP_200_OK,
    responses={
        IncorrectAuthCredsException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": IncorrectAuthCredsException.detail,
        },
    },
)
def login_user(
    user: AuthenticateUserDep,
) -> JWTInfoSchema:
    access_token = JWTService.create_access_token_for_user(user.id)
    refresh_token = JWTService.create_refresh_token_for_user(user.id)
    return JWTInfoSchema(
        access=access_token,
        refresh=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=JWTInfoSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses={
        InvalidAuthTokenException.status_code: {
            "model": BaseHTTPExceptionSchema,
            "description": InvalidAuthTokenException.detail,
        },
    },
)
def refresh_jwt(
    user: CurrentUserForRefreshDep,
) -> JWTInfoSchema:
    access_token = JWTService.create_access_token_for_user(user.id)
    return JWTInfoSchema(access=access_token)


@router.post(
    "/me",
    response_model=UserSchema,
)
async def get_me(
    user: CurrentUserDep,
) -> UserSchema:
    return user
