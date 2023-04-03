import typing
import logging
from django.http import JsonResponse, HttpResponse, HttpRequest
from freeman.utils.exceptions import RequestError

logger = logging.getLogger(__name__)


class FreemanExceptionHandlerMiddleware:
    def __init__(self, get_response: typing.Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> HttpResponse | None:
        if type(exception) == RequestError:
            logger.exception(exception)
            response = JsonResponse(
                {"error": exception.json()},
                status=exception.statusCode,
                headers=exception.headers,
            )
            return response
