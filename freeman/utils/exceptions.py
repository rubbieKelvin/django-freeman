import typing


class RequestError(Exception):
    """
    An exception class for representing errors that occur during a HTTP request.

    Attributes:
        reason (str): A human-readable string explaining the reason for the error.
        statusCode (int): The HTTP status code returned by the server.
        headers (dict): A dictionary containing the HTTP headers returned by the server.

    Example:
        >>> try:
        ...     # Make a HTTP request here
        ... except Exception as e:
        ...     raise RequestError("Request failed", statusCode=500, headers={"Content-Type": "application/json"}) from e
        ...
        Traceback (most recent call last):
          ...
        __main__.RequestError: Request failed (status code: 500, headers: {'Content-Type': 'application/json'})
    """

    def __init__(
        self,
        reason: str,
        statusCode: int = 400,
        headers: dict[str, str] | None = None,
        exception: BaseException | None = None,
    ):
        self.reason = reason
        self.statusCode = statusCode
        self.headers = headers
        self.exception = exception

        message = f"{reason} (status code: {statusCode}, headers: {headers})"
        super().__init__(message)

    def json(self) -> dict[str, typing.Any]:
        return {
            "reason": self.reason,
            "statusCode": self.statusCode,
            "exception": self.exception.__class__.__name__ if self.exception else None,
        }
