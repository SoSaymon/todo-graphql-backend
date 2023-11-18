import pytest
from app.utils.email import is_valid_email
from graphql import GraphQLError


@pytest.mark.utils
class TestEmailValidation:
    def test_is_valid_email(self):
        assert is_valid_email("test@example.com") == True

    def test_is_valid_email_with_invalid_email(self):
        with pytest.raises(GraphQLError):
            is_valid_email("invalid_email")

    def test_is_valid_email_with_empty_string(self):
        with pytest.raises(GraphQLError):
            is_valid_email("")
