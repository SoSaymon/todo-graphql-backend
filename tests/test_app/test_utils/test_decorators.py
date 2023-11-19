import pytest
from graphql import GraphQLError
from unittest.mock import Mock, patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.decorators import admin_user, logged_in
from app.db.models import User, Base
from app.utils.jwt import generate_jwt
from app.utils.password import hash_password


# This class tests the decorators used in the application
@pytest.mark.decorators
class TestDecorators:
    Session = None
    engine = None
    admin = None
    user = None

    @classmethod
    def setup_class(cls):
        """
        This method sets up the test environment.
        It creates an in-memory database and two users: an admin and a regular user.
        """
        # Creating an in-memory database
        cls.engine = create_engine("sqlite:///:memory:")
        cls.Session = sessionmaker(bind=cls.engine)

        # Creating all tables in the database
        Base.metadata.create_all(cls.engine)

        # Creating an admin user
        cls.admin = User(
            username="Admin",
            email="admin@admin.com",
            password_hash=hash_password("12345678"),
            is_admin=True,
            is_active=True,
        )

        # Creating a regular user
        cls.user = User(
            username="user",
            email="user@user.com",
            password_hash=hash_password("12345678"),
            is_admin=False,
            is_active=True,
        )

        # Adding the users to the database
        session = cls.Session()
        session.add(cls.admin)
        session.add(cls.user)
        session.commit()
        session.refresh(cls.admin)
        session.refresh(cls.user)
        session.close()

    def test_admin_user_decorator_with_admin_user(self):
        """
        This test checks if the admin_user decorator allows an admin user to access a function.
        """
        func = Mock()
        decorated_func = admin_user(func)
        user = self.admin
        info = Mock(context=Mock())

        # Generating a JWT for the admin user
        admin_jwt = generate_jwt(user.email)

        # Setting the Authorization header with the JWT
        auth_header = f"Bearer {admin_jwt}"
        info.context.get.return_value.headers.get.return_value = auth_header

        # Calling the decorated function
        decorated_func(None, info)

        # Checking if the function was called
        func.assert_called_once()

    def test_admin_user_decorator_with_non_admin_user(self):
        """
        This test checks if the admin_user decorator prevents a non-admin user from accessing a function.
        """
        func = Mock()
        decorated_func = admin_user(func)
        user = self.user
        info = Mock(context=Mock())

        # Generating a JWT for the regular user
        user_jwt = generate_jwt(user.email)

        # Setting the Authorization header with the JWT
        auth_header = f"Bearer {user_jwt}"
        info.context.get.return_value.headers.get.return_value = auth_header

        # Calling the decorated function and expecting a GraphQLError
        with patch("app.utils.user.get_authenticated_user") as mock_get_user:
            mock_get_user.return_value = (user,)
            with pytest.raises(GraphQLError):
                decorated_func(None, info)

        # Checking if the function was not called
        func.assert_not_called()

    def test_logged_in_decorator_with_logged_in_user(self):
        """
        This test checks if the logged_in decorator allows a logged-in user to access a function.
        """
        func = Mock()
        decorated_func = logged_in(func)
        user = self.admin
        info = Mock(context=Mock())

        # Generating a JWT for the logged-in user
        user_jwt = generate_jwt(user.email)

        # Setting the Authorization header with the JWT
        auth_header = f"Bearer {user_jwt}"
        info.context.get.return_value.headers.get.return_value = auth_header

        # Calling the decorated function
        with patch("app.utils.user.get_authenticated_user") as mock_get_user:
            mock_get_user.return_value = (user,)
            decorated_func(None, info)

        # Checking if the function was called
        func.assert_called_once()

    def test_logged_in_decorator_with_not_logged_in_user(self):
        """
        This test checks if the logged_in decorator prevents a not logged-in user from accessing a function.
        """
        func = Mock()
        decorated_func = logged_in(func)
        info = Mock()
        info.configure_mock(context={"headers": {"Authorization": "Bearer token"}})

        # Calling the decorated function and expecting a GraphQLError
        with patch("app.utils.user.get_authenticated_user") as mock_get_user:
            mock_get_user.return_value = (None,)
            with pytest.raises(GraphQLError):
                decorated_func(None, info)
        # Checking if the function was not called
        func.assert_not_called()
