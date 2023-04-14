import re
from freeman.utils.strings import (
    EMAIL_REGEX,
    PASSWORD_WITH_AT_LEAST_6_CHARS_REGEX,
    STRONG_PASSWORD_REGEX,
    USERNAME_REGEX,
)
from freeman.utils.strings import toSnakeCase


def test_toSnakeCase():
    assert toSnakeCase("MyString") == "my_string"
    assert toSnakeCase("AnotherString") == "another_string"
    assert toSnakeCase("ThisIsATestString") == "this_is_a_test_string"
    assert toSnakeCase("Some123String") == "some123_string"
    assert toSnakeCase("Has_Underscore") == "has_underscore"
    assert toSnakeCase("Test with Spaces") == "test_with_spaces"
    assert toSnakeCase("ALLCAPS") == "allcaps"


def test_email_regex():
    # valid email addresses
    assert re.match(EMAIL_REGEX, "example@gmail.com")
    assert re.match(EMAIL_REGEX, "example1234@example.co.uk")
    assert re.match(EMAIL_REGEX, "joe.smith@example.com")
    assert re.match(EMAIL_REGEX, "jane_doe123@example.com")

    # invalid email addresses
    assert not re.match(EMAIL_REGEX, "examplegmail.com")
    assert not re.match(EMAIL_REGEX, "example@gmailcom")
    assert not re.match(EMAIL_REGEX, "example@.com")


def test_password_with_at_least_6_chars_regex():
    # valid passwords
    assert re.match(PASSWORD_WITH_AT_LEAST_6_CHARS_REGEX, "password")
    assert re.match(PASSWORD_WITH_AT_LEAST_6_CHARS_REGEX, "PaSwOrD123")
    assert re.match(PASSWORD_WITH_AT_LEAST_6_CHARS_REGEX, "password123")

    # invalid passwords
    assert not re.match(PASSWORD_WITH_AT_LEAST_6_CHARS_REGEX, "pw")
    assert not re.match(PASSWORD_WITH_AT_LEAST_6_CHARS_REGEX, "12345")
    assert not re.match(PASSWORD_WITH_AT_LEAST_6_CHARS_REGEX, "password@#$")


def test_strong_password_regex():
    # valid passwords
    assert re.match(STRONG_PASSWORD_REGEX, "PaSwOrD123@")
    assert not re.match(STRONG_PASSWORD_REGEX, "password@#$123")
    assert not re.match(STRONG_PASSWORD_REGEX, "Password123")
    assert not re.match(STRONG_PASSWORD_REGEX, "p@$$w0rd")

    # invalid passwords
    assert not re.match(STRONG_PASSWORD_REGEX, "password123")
    assert not re.match(STRONG_PASSWORD_REGEX, "password@#$")
    assert not re.match(STRONG_PASSWORD_REGEX, "password")


def test_username_regex():
    # valid usernames
    assert re.match(USERNAME_REGEX, "user")
    assert re.match(USERNAME_REGEX, "user123")
    assert re.match(USERNAME_REGEX, "user_name")

    # ...
    assert not re.match(USERNAME_REGEX, "user.name")
    assert not re.match(USERNAME_REGEX, "u")
    assert not re.match(USERNAME_REGEX, "a_very_long_username_that_is_too_long")
