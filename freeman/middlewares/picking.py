import json
import typing
from django.http import HttpResponse, HttpRequest
from freeman.utils.picking import pick
# from django.conf import settings

# FREEMAN_PICK_PARAM_NAME = getattr(settings, "FREEMAN_PICK_PARAM_NAME", "pick")
FREEMAN_PICK_PARAM_NAME = "pick"


class FreemanPickMiddleware:
    """
    Middleware that modifies the response of views by picking specific fields from JSON content.

    This middleware expects responses with a "Content-Type" header of "application/json".
    If the request has a "pick" query parameter with a valid JSON array of field names,
    this middleware will pick those fields from the JSON content of the response and return
    a new response with only those fields.

    Args:
        get_response: A callable that takes an `HttpRequest` object and returns an `HttpResponse`.
    """

    def __init__(self, get_response: typing.Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request and return a response.

        Args:
            request: The incoming `HttpRequest` object.

        Returns:
            An `HttpResponse` object.

        Raises:
            json.decoder.JSONDecodeError: If the "pick" query parameter is not a valid JSON array.
        """

        response = self.get_response(request)

        if response["Content-Type"] != "application/json":
            return response

        data = json.loads(response.content)
        pickparam = request.GET.get(FREEMAN_PICK_PARAM_NAME)

        if pickparam:
            try:
                pickdata = json.loads(pickparam)
            except json.decoder.JSONDecodeError:
                raise json.decoder.JSONDecodeError(
                    f'Picking parameter "?{FREEMAN_PICK_PARAM_NAME}" should be valid a json string',
                    pickparam,
                    0,
                )

            transformedResponse = pick(data, pickdata)
            response.content = json.dumps(transformedResponse)

        return response
