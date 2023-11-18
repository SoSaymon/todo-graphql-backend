from typing import Type

from graphene import Mutation, String, Field
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import User
from app.gql.types import UserObject
from app.utils.email import is_valid_email
from app.utils.password import is_password_safe, hash_password


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
