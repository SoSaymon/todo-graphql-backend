import hashlib

import pytest
from graphql import GraphQLError

from app.utils import password


@pytest.mark.password_utils
def test_hash_password_returns_hashed_password():
    hashed_password = password.hash_password("securepassword")
    assert hashed_password != "securepassword"


@pytest.mark.password_utils
def test_verify_password_with_correct_password():
    hashed_password = password.hash_password("securepassword")
    assert password.verify_password(hashed_password, "securepassword") is None


@pytest.mark.password_utils
def test_verify_password_with_incorrect_password():
    hashed_password = password.hash_password("securepassword")
    with pytest.raises(GraphQLError):
        password.verify_password(hashed_password, "wrongpassword")


@pytest.mark.password_utils
def test_is_password_safe_with_unsafe_password():
    with pytest.raises(GraphQLError):
        password.is_password_safe("short")


@pytest.mark.password_utils
def test_is_password_safe_with_safe_password():
    assert password.is_password_safe("longsecurepassword") is True


@pytest.mark.password_utils
def test_get_hashes_from_hibp_returns_hashes():
    password_hash = hashlib.sha1("securepassword".encode()).hexdigest()
    hashes = password.get_hashes_from_hibp(password_hash)
    assert isinstance(hashes, str)


@pytest.mark.password_utils
def test_check_if_hash_is_present_with_present_hash():
    password_hash = hashlib.sha1("password".encode()).hexdigest()
    hash_output = password.get_hashes_from_hibp(password_hash)
    assert password.check_if_hash_is_present(hash_output, password_hash) is True


@pytest.mark.password_utils
def test_check_if_hash_is_present_with_absent_hash():
    password_hash = hashlib.sha1("vb.g[%Brc+nV5Z'uk>mU4Y".encode()).hexdigest()
    hash_output = password.get_hashes_from_hibp(password_hash)
    assert password.check_if_hash_is_present(hash_output, password_hash) is False


@pytest.mark.password_utils
def test_split_hashes_returns_dict():
    password_hash = hashlib.sha1("password".encode()).hexdigest()
    hash_output = password.get_hashes_from_hibp(password_hash)
    hash_dict = password.split_hashes(hash_output)
    assert isinstance(hash_dict, dict)
