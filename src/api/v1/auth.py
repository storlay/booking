from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.exc import IntegrityError

from src.api.dependecies import AuthenticateUserDep
from src.api.dependecies import CurrentUserDep
from src.api.dependecies import CurrentUserForRefreshDep
from src.db.database import async_session
from src.repositories.users import UsersRepository
from src.schemas.auth import JWTInfoSchema
from src.schemas.users import UserAuthSchema
from src.schemas.users import UserSchema
from src.services.auth import AuthService
from src.services.jwt import JWTService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication & Authorization"],
)


@router.post("/register")
async def register_user(
    data: UserAuthSchema,
):
    data.password = AuthService.hash_password(data.password).decode("utf-8")
    async with async_session() as session:
        try:
            await UsersRepository(session).add(data)
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {data.email!r} already exists.",
            )
    return {"status": "OK"}


@router.post(
    "/login",
    response_model=JWTInfoSchema,
)
def login_user(
    user: AuthenticateUserDep,
) -> JWTInfoSchema:
    access_token = JWTService.create_access_token_for_user(user)
    refresh_token = JWTService.create_refresh_token_for_user(user)
    return JWTInfoSchema(
        access=access_token,
        refresh=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=JWTInfoSchema,
    response_model_exclude_none=True,
)
def refresh_jwt(
    user: CurrentUserForRefreshDep,
) -> JWTInfoSchema:
    access_token = JWTService.create_access_token_for_user(user)
    return JWTInfoSchema(access=access_token)


@router.post(
    "/me",
    response_model=UserSchema,
)
async def get_me(
    user: CurrentUserDep,
) -> UserSchema:
    return user
