import bcrypt


class AuthService:
    @staticmethod
    def hash_password(
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(
            password.encode("utf-8"),
            salt,
        )

    @classmethod
    def check_password(
        cls,
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password,
        )
