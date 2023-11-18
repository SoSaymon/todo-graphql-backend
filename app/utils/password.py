import hashlib
from typing import Dict

import requests
from argon2 import PasswordHasher
from graphql import GraphQLError

ph = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hashes a given password using the Argon2 algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return ph.hash(password)


def is_password_safe(password: str) -> bool:
    """
    Checks if a given password is safe based on its length and its presence in the Have I Been Pwned database.

    Args:
        password (str): The password to be checked.

    Returns:
        bool: True if the password is safe, False otherwise.

    Raises:
        GraphQLError: If the password is not safe.
    """

    MIN_PASSWORD_LENGTH = 12

    if len(password) < MIN_PASSWORD_LENGTH:
        raise GraphQLError("Your password is not safe enough")

    password_sha1 = hashlib.sha1(password.encode()).hexdigest()

    if check_if_hash_is_present(get_hashes_from_hibp(password_sha1), password_sha1):
        raise GraphQLError("Your password is not safe enough")

    return True


def get_hashes_from_hibp(password_hash: str) -> str:
    """
    Retrieves the hashes from the Have I Been Pwned database that match the first 5 characters of the given password hash.

    Args:
        password_hash (str): The SHA1 hash of the password.

    Returns:
        str: The hashes from the HIBP database.
    """

    password_hash_prefix = password_hash[:5]
    url = "https://api.pwnedpasswords.com/range/"

    return requests.get(f"{url}{password_hash_prefix}").text


def check_if_hash_is_present(hash_output: str, password_hash: str) -> bool:
    """
    Checks if the given password hash is present in the hash output.

    Args:
        hash_output (str): The hash output from the HIBP database.
        password_hash (str): The SHA1 hash of the password.

    Returns:
        bool: True if the password hash is present in the hash output, False otherwise.
    """

    MAX_NUMBER_OF_PASSWORD_APPEARANCES = 5

    hash_dict = split_hashes(hash_output)
    password_hash_prefix = password_hash[:5]

    for key, value in hash_dict.items():
        key_with_prefix = f"{password_hash_prefix.upper()}{key}"

        if key_with_prefix == password_hash.upper():
            if value > MAX_NUMBER_OF_PASSWORD_APPEARANCES:
                return True


def split_hashes(hash_output: str) -> Dict[str, int]:
    """
    Splits the hash output into a dictionary where the keys are the hashes and the values are the counts.

    Args:
        hash_output (str): The hash output from the HIBP database.

    Returns:
        Dict[str, int]: A dictionary where the keys are the hashes and the values are the counts.
    """

    hash_dict = {}
    lines = hash_output.split("\r\n")
    for line in lines:
        if line:
            hash_, count = line.split(":")
            hash_dict[hash_] = int(count)
    return hash_dict
