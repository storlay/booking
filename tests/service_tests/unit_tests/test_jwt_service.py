from src.services.jwt import JWTService


def test_create_access_token_for_user():
    data = {"user_id": 1}
    jwt_token = JWTService().create_access_token_for_user(**data)
    assert jwt_token
    assert isinstance(jwt_token, str)
