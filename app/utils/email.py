import re

from graphql import GraphQLError


def is_valid_email(email: str) -> bool:
    """
    Checks if the given string is a valid email address.

    Args:
        email (str): The string to be checked.

    Returns:
        bool: True if the string is a valid email address.

    Raises:
        GraphQLError: If the string is not a valid email address.
    """

    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.match(email_regex, email) is None:
        raise GraphQLError("Your email is not valid")

    return True
