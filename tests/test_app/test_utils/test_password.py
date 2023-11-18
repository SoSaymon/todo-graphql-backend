import pytest
from app.utils.password import hash_password, is_password_safe
from argon2 import PasswordHasher
from graphql import GraphQLError

ph = PasswordHasher()


@pytest.mark.utils
class TestPasswordUtils:
    def test_hash_password(self):
        password = "password123"
        hashed_password = hash_password(password)
        assert ph.verify(hashed_password, password) == True

    def test_is_password_safe_with_safe_password(self):
        assert is_password_safe("ThisIsASafePassword123!") == True

    def test_is_password_safe_with_unsafe_password(self):
        with pytest.raises(GraphQLError):
            is_password_safe("unsafe")
