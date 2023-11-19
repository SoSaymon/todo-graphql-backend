from typing import Dict, Tuple

from graphql import GraphQLError

from app.db.database import Session
from app.db.models import User
from app.utils.jwt import verify_jwt


def get_authenticated_user(context: Dict) -> Tuple[User, str]:
    """
    Authenticates the user based on the JWT token from the request header.

    The function retrieves the 'Authorization' header from the request object in the context.
    If the header is present and correctly formatted, the function verifies the JWT token.
    If the token is valid, the function queries the database for a user with the email from the token payload.
    If the user is found, the function does not raise an error, effectively authenticating the user.
    If the user is not found or the token is invalid, the function raises a GraphQLError.

    Args:
        context (Dict): The context dictionary containing the request object.

    Returns:
    User: Returns a User object that has been successfully authenticated. If authentication fails, the function will raise a GraphQLError exception.

    Raises:
        GraphQLError: If the 'Authorization' header is missing, incorrectly formatted, or the token is invalid.
                      Also raises an error if the user corresponding to the email in the token payload is not found.
    """
    request_object = context.get("request")
    if request_object is None:
        raise GraphQLError("Missing request object in context")
    auth_header: str = request_object.headers.get("Authorization")

    token = [None]

    if auth_header and "Bearer" in auth_header:
        token = auth_header.split(" ")

    if token and len(token) == 2:
        token = token[1]

        is_verified, payload = verify_jwt(token)

        session = Session()
        user: User = (
            session.query(User).filter(User.email == payload.get("sub")).first()
        )

        if not user:
            raise GraphQLError("Couldn't authenticate user")

        return user, token
    else:
        raise GraphQLError("Missing authentication token")
