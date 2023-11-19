import pytest
from app.db.models import User
from datetime import datetime


@pytest.mark.models
class TestUser:
    def setup(self):
        self.user = User(
            id=1,
            username="user1",
            email="user1@example.com",
            password_hash="password",
            is_admin=False,
            is_active=True,
            created_at=datetime.now(),
        )

    def test_create_user(self):
        assert self.user.id == 1
        assert self.user.username == "user1"
        assert self.user.email == "user1@example.com"
        assert self.user.password_hash == "password"
        assert not self.user.is_admin
        assert self.user.is_active
        assert self.user.created_at
