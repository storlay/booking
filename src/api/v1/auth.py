from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.exc import IntegrityError

from src.db.database import async_session
from src.repositories.users import UsersRepository
from src.schemas.users import RegisterUserSchema
from src.utils.auth import hash_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication & Authorization"],
)


@router.post("/register")
async def register_user(
    data: RegisterUserSchema,
) -> None:
    data.password = hash_password(data.password)
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
