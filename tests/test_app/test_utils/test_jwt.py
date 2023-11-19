from datetime import datetime, timezone, timedelta

import jwt
import pytest
from app.utils.jwt import generate_jwt, verify_jwt, regenerate_jwt
from graphql import GraphQLError

# Secret key for JWT
SECRET_KEY = "test-secret-code"
# Algorithm used for JWT
ALGORITHM = "HS256"


@pytest.mark.jwt_utils
def test_generate_jwt_creates_valid_token():
    """
    Test case for generating a JWT and verifying it.
    The test asserts that the token is valid and the payload contains the correct subject.
    """
    email = "test@example.com"
    token = generate_jwt(email)
    is_valid, payload = verify_jwt(token)
    assert is_valid
    assert payload["sub"] == email


@pytest.mark.jwt_utils
def test_verify_jwt_with_invalid_token():
    """
    Test case for verifying an invalid JWT.
    The test asserts that a GraphQLError is raised when an invalid token is verified.
    """
    with pytest.raises(GraphQLError):
        verify_jwt("invalid_token")


@pytest.mark.jwt_utils
def test_verify_jwt_with_expired_token():
    """
    Test case for verifying an expired JWT.
    The test asserts that a GraphQLError is raised when an expired token is verified.
    """
    email = "test@example.com"
    token = generate_jwt(email)
    # Simulate token expiration by manually setting the expiration time in the past
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=ALGORITHM,
        options={"verify_signature": False},  # Skip signature verification
    )
    payload["exp"] = datetime.now(timezone.utc) - timedelta(minutes=1)
    expired_token = jwt.encode(
        payload,
        None,
        algorithm="none",
    )
    with pytest.raises(GraphQLError):
        verify_jwt(expired_token)


@pytest.mark.jwt_utils
def test_regenerate_jwt_with_valid_token():
    """
    Test case for regenerating a JWT from a valid token and verifying it.
    The test asserts that the regenerated token is valid and the payload contains the correct subject.
    """
    email = "test@example.com"
    token = generate_jwt(email)
    regenerated_token = regenerate_jwt(token)
    is_valid, payload = verify_jwt(regenerated_token)
    assert is_valid
    assert payload["sub"] == email


@pytest.mark.jwt_utils
def test_regenerate_jwt_with_invalid_token():
    """
    Test case for regenerating a JWT from an invalid token.
    The test asserts that a GraphQLError is raised when an invalid token is regenerated.
    """
    with pytest.raises(GraphQLError):
        regenerate_jwt("invalid_token")
