from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import status
from sqlalchemy.exc import IntegrityError

from src.api.v1.dependecies import CurrentUserDep
from src.db.database import async_session
from src.repositories.users import UsersRepository
from src.schemas.users import UserAuthSchema
from src.services.auth import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication & Authorization"],
)


@router.post("/register")
async def register_user(
    data: UserAuthSchema,
):
    data.password = AuthService().hash_password(data.password)
    async with async_session() as session:
        try:
            await UsersRepository(session).add(
                data,
            )
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {data.email!r} already exists.",
            )
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserAuthSchema,
    response: Response,
):
    async with async_session() as session:
        user = await UsersRepository(session).get_one_or_none_with_password(
            email=data.email,
        )
    if not user or not AuthService().verify_password(data.password, user.password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {
        "status": "OK",
        "data": {
            "access": access_token,
        },
    }


@router.post("/logout")
async def logout_user(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.post("/me")
async def get_me(
    user: CurrentUserDep,
):
    return user
