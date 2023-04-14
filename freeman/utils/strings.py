import re

# Regex for email address validation
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# Regex for password with at least 6 characters validation
PASSWORD_WITH_AT_LEAST_6_CHARS_REGEX = re.compile(r"^[a-zA-Z0-9_]{6,}$")

# Strong password pattern (at least 8 characters, 1 uppercase, 1 lowercase, 1 digit, and 1 special character)
STRONG_PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
)

# Username pattern (only alphanumeric characters and underscores, between 3 and 20 characters long)
USERNAME_REGEX = re.compile(r"^\w{3,20}$")


def reduceChar(string: str, char: str = " ") -> str:
    """
    Reduces the number of occurrences of a given character if it appears more than once sequentially in the string.

    Args:
        string (str): The input string to be processed.
        char (str, optional): The character to be reduced. Defaults to " ".

    Returns:
        str: The resulting string with reduced sequential occurrences of the given character.
    """
    if len(char) != 1:
        raise ValueError("char should be a single character")

    res = [string[0]]
    for i in range(1, len(string)):
        if string[i] == char and string[i] == res[-1]:
            continue
        res.append(string[i])

    return "".join(res)


def reduceChars(string: str, chars: str | list[str]) -> str:
    """
    Reduces the number of occurrences of the specified character(s) in the string
    if they occur more than once sequentially.

    Args:
        string (str): The input string to reduce.
        chars (str or list of str): The character(s) to reduce. If a string is
            provided, only occurrences of that single character will be reduced.
            If a list of strings is provided, occurrences of all characters in
            the list will be reduced.

    Returns:
        str: The reduced string.

    Raises:
        ValueError: If chars is not a single character string or a list of
            strings.

    Examples:
        >>> reduceChars("hello    world!", " ")
        'hello world!'

        >>> reduceChars("AABBCC", ["A", "C"])
        'ABC'
    """
    res = string
    for char in chars:
        res = reduceChar(res, char)
    print(string, res)
    return res


def toSnakeCase(string: str) -> str:
    """Convert a PascalCase string to snake_case"""
    # reduce string
    string = reduceChars(string, ["_", " "]).replace(" ", "_")
    # Convert first character to lowercase
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    # Convert remaining uppercase characters to lowercase with underscore
    string = re.sub("([a-z0-9])([A-Z])", r"\1_\2", string)
    # Convert to all lowercase
    string = string.lower()
    return reduceChar(string, "_")
