from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt
from passlib.context import CryptContext

from src.config.config import settings


class AuthService:
    PWD_CONTEXT = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    def create_access_token(
        self,
        data: dict,
    ) -> str:
        to_encode = data.copy()
        expire_delta = timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(timezone.utc) + expire_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt.SECRET_KEY,
            algorithm=settings.jwt.ALGORITHM,
        )
        return encoded_jwt

    def hash_password(
        self,
        row_password: str,
    ) -> str:
        return self.PWD_CONTEXT.hash(row_password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return self.PWD_CONTEXT.verify(
            plain_password,
            hashed_password,
        )
