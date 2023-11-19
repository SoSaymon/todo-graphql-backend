from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple

import jwt
from graphql import GraphQLError

from app.utils.env import getenv

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
TOKEN_EXPIRATION_TIME_MINUTES = int(getenv("TOKEN_EXPIRATION_TIME_MINUTES"))


def generate_jwt(email: str) -> str:
    """
    Generates a JWT for the given email.

    The JWT's payload contains the email and an expiration time. The JWT is
    encoded using the secret key and algorithm specified by the environment
    variables SECRET_KEY and ALGORITHM.

    Args:
        email (str): The email to include in the JWT's payload.

    Returns:
        str: The encoded JWT.
    """
    expiration_time = get_expiration_date()

    payload = {"sub": email, "exp": expiration_time}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_expiration_date() -> datetime:
    """
    Calculates the expiration date for a JWT.

    The function adds the number of minutes specified by the environment variable TOKEN_EXPIRATION_TIME_MINUTES
    to the current date and time in UTC.

    Returns:
        datetime: The expiration date of the JWT.
    """
    return datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)


def verify_jwt(token: str) -> Tuple[bool, Dict]:
    """
    Verifies the given JWT.

    The JWT is decoded using the secret key and algorithm specified by the environment
    variables SECRET_KEY and ALGORITHM. The function checks if the token has expired
    and raises an error if it has. If the token is valid and has not expired, the function
    returns a tuple where the first element is a boolean indicating the validity of the token
    and the second element is the payload of the token.

    Args:
        token (str): The JWT to verify.

    Returns:
        tuple: A tuple where the first element is a boolean indicating the validity of the token
               and the second element is the payload of the token. Returns None if the token is invalid.

    Raises:
        GraphQLError: If the token is invalid or has expired.
    """

    try:
        payload: Dict = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        if datetime.now(timezone.utc) > datetime.fromtimestamp(
            payload.get("exp"), tz=timezone.utc
        ):
            raise GraphQLError("Token has expired")

        return True, payload

    except jwt.exceptions.PyJWTError:
        raise GraphQLError("Invalid authentication token")


def regenerate_jwt(token: str) -> str:
    """
    Regenerates a JWT.

    The function first verifies the given JWT. If the JWT is valid, the function generates a new JWT with the same payload
    but with a new expiration date. The new expiration date is calculated by the function get_expiration_date.

    Args:
        token (str): The JWT to regenerate.

    Returns:
        str: The regenerated JWT.

    Raises:
        GraphQLError: If the token is invalid.
    """
    is_verified, payload = verify_jwt(token)

    if is_verified:
        payload["exp"] = get_expiration_date()
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
