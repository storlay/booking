from src.services.jwt import JWTService


def test_encode_and_decode_token():
    user_id = 1
    token = JWTService().create_access_token_for_user(user_id)
    assert token
    assert isinstance(token, str)
    decoded_payload = JWTService().decode(token)
    assert decoded_payload.get("sub")
    assert int(decoded_payload["sub"]) == user_id
