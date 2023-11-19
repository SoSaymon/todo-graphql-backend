from functools import wraps
from typing import Callable

from graphql import GraphQLError

from app.db.models import User
from app.utils.user import get_authenticated_user


def admin_user(func: Callable):
    """
    Decorator to check if the user is an admin.
    If the user is not an admin, a GraphQLError is raised.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user_token = get_authenticated_user(info.context)

        if user_token is None:
            raise GraphQLError("Authentication failed")

        user: User = user_token[0]

        if user.is_admin is not True:
            raise GraphQLError("You are not authorized to perform this action")

        return func(*args, **kwargs)

    return wrapper


def logged_in(func: Callable):
    """
    Decorator to check if the user is logged in.
    If the user is not logged in, a GraphQLError is raised.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user_token = get_authenticated_user(info.context)

        if user_token is None:
            raise GraphQLError("Authentication failed")

        user: User = user_token[0]

        if not user:
            raise GraphQLError("You have to be logged in to perform this action")
        return func(*args, **kwargs)

    return wrapper
