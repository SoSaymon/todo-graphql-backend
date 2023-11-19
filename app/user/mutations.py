from datetime import datetime
from typing import Type, Optional

from graphene import Mutation, String, Field
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import User
from app.gql.types import UserObject
from app.utils.email import is_valid_email
from app.utils.jwt import generate_jwt, regenerate_jwt
from app.utils.password import is_password_safe, hash_password, verify_password
from app.utils.user import get_authenticated_user


class RegisterUser(Mutation):
    """
    Mutation class for registering a new user.

    Attributes:
        username (String): The username of the new user.
        email (String): The email of the new user.
        password (String): The password of the new user.
        user (Field): The newly created user object.
    """

    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)

    user = Field(UserObject)

    @staticmethod
    def mutate(
        root, info, username: str, email: str, password: str
    ) -> Type["RegisterUser"]:
        """
        Register a new user.

        Args:
            root: The root object that GraphQL uses to look up the initial value for the query.
            info: The GraphQLResolveInfo object containing information about the query.
            username (str): The username of the new user.
            email (str): The email of the new user.
            password (str): The password of the new user.

        Returns:
            RegisterUser: A RegisterUser object with the newly created user.

        Raises:
            GraphQLError: If the username or email already exists.
        """

        session = Session()

        is_valid_email(email)

        user = session.query(User).filter(User.email == email).first()

        if user:
            raise GraphQLError("Email already exists")

        user = session.query(User).filter(User.username == username).first()

        if user:
            raise GraphQLError("Username already taken")

        is_password_safe(password)

        password_hash = hash_password(password)

        user = User(username=username, email=email, password_hash=password_hash)

        session.add(user)
        session.commit()
        session.refresh(user)

        return RegisterUser(user=user)


class LoginUser(Mutation):
    """
    Mutation class for logging in a user.

    The class takes an email and password as arguments and verifies them against the database.
    If the email and password are valid, the function generates a JWT token and returns it.
    If the email and password are not valid, the function raises a GraphQLError.

    Attributes:
        email (String): The email of the user trying to log in.
        password (String): The password of the user trying to log in.
        token (String): The JWT token generated upon successful login.

    Raises:
        GraphQLError: If the email or password is invalid.
    """

    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, password: str, email: str) -> Type["LoginUser"]:
        """
        Authenticates a user and generates a JWT token.

        The method takes an email and password as arguments and verifies them against the database.
        If the email and password are valid, the method generates a JWT token and returns it.
        If the email and password are not valid, the method raises a GraphQLError.

        Args:
            root: The root object that GraphQL uses to look up the initial value for the query.
            info: The GraphQLResolveInfo object containing information about the query.
            password (str): The password of the user trying to log in.
            email (str): The email of the user trying to log in.

        Returns:
            LoginUser: A LoginUser object with the generated JWT token.

        Raises:
            GraphQLError: If the email or password is invalid.
        """
        session = Session()
        user = session.query(User).filter(User.email == email).first()

        if not user:
            raise GraphQLError("Invalid email or password")

        verify_password(user.password_hash, password)

        if not user.is_active:
            raise GraphQLError(
                "Your account is not active yet, please confirm your email or contact our support team"
            )

        token = generate_jwt(email)

        user.last_login = datetime.now()

        session.commit()
        session.refresh(user)
        session.close()

        return LoginUser(token=token)


class RegenerateJWT(Mutation):
    """
    Mutation class for regenerating a JWT token.

    The class takes no arguments and uses the authenticated user's current JWT token.
    If the token is valid, the function regenerates a new JWT token and returns it.
    If the token is not valid, the function raises a GraphQLError.

    Attributes:
        token (String): The regenerated JWT token.

    Raises:
        GraphQLError: If the token is invalid.
    """

    token = String()

    @staticmethod
    def mutate(root, info) -> Type["RegenerateJWT"]:
        """
        Regenerates a JWT token for the authenticated user.

        The method takes no arguments and uses the authenticated user's current JWT token.
        If the token is valid, the method regenerates a new JWT token and returns it.
        If the token is not valid, the method raises a GraphQLError.

        Args:
            root: The root object that GraphQL uses to look up the initial value for the query.
            info: The GraphQLResolveInfo object containing information about the query.

        Returns:
            RegenerateJWT: A RegenerateJWT object with the regenerated JWT token.

        Raises:
            GraphQLError: If the token is invalid.
        """
        user, token = get_authenticated_user(info.context)
        token = regenerate_jwt(token)

        return RegenerateJWT(token=token)
