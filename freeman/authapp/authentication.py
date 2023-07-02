import typing
from django.db.models import Q, Model
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.authentication import BaseAuthentication
from .models import AuthenticationToken


class FreemanAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    PREFIX = "Bearer"

    def authenticate(
        self, request: Request
    ) -> tuple[Model, AuthenticationToken] | None:
        auth = typing.cast(str | None, request.META.get("HTTP_AUTHORIZATION", None))

        if not auth:
            return None

        prefix, token = auth.split()

        if prefix != self.PREFIX:
            raise exceptions.AuthenticationFailed("Invalid token header prefix")

        if len(token) != 62:
            raise exceptions.AuthenticationFailed(
                "Invalid token header. No credentials provided."
            )

        try:
            token = AuthenticationToken.findOneWhere(Q(key=token))
        except AuthenticationToken.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                "Invalid token header. Token does not exist."
            )

        if token.is_expired:
            raise exceptions.AuthenticationFailed("Token has expired")

        return (token.user, token)

    def authenticate_header(self, request):
        return self.PREFIX
