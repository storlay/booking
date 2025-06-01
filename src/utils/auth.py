from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(
    row_password: str,
) -> str:
    return pwd_context.hash(row_password)
