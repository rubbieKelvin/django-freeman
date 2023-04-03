import re


def toSnakeCase(string: str) -> str:
    """ Convert a PascalCase string to snake_case """
    # Convert first character to lowercase
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    # Convert remaining uppercase characters to lowercase with underscore
    string = re.sub('([a-z0-9])([A-Z])', r'\1_\2', string)
    # Convert to all lowercase
    string = string.lower()
    return string
