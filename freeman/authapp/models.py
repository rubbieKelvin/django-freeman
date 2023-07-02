import os
import typing
import binascii

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from freeman.models.abstract import AbstractSharedModel
from freeman.settings import FREEMAN_ALLOW_MULTIPLE_TOKENS_PER_USER


class AuthenticatorModel(AbstractSharedModel):
    last_updated = None
    last_login = models.DateTimeField(editable=False, null=True, default=None)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="authenticator",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} user={self.user}>"


class AuthenticationToken(AbstractSharedModel):
    auth = models.ForeignKey(
        AuthenticatorModel, on_delete=models.CASCADE, related_name="tokens"
    )

    key = models.CharField(max_length=62, editable=False)
    expires_on = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.key[:6]}...{self.key[-6:]}"

    def save(self, *args: typing.Any, **kwargs: typing.Any):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @property
    def user(self) -> models.Model:
        auth = typing.cast(AuthenticatorModel, self.auth)
        return auth.user

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(31)).decode()

    @property
    def is_expired(self):
        if self.expires_on:
            return timezone.now() > datetime.fromisoformat(str(self.expires_on))
        return False

    @classmethod
    def create(cls, *, auth: AuthenticatorModel, expires_on: datetime | None = None):
        return cls.insertSingle({"auth": auth, "expires_on": expires_on})

    class Meta:
        constraints = (
            []
            if FREEMAN_ALLOW_MULTIPLE_TOKENS_PER_USER
            else [models.UniqueConstraint(name="unique_token_model", fields=["auth"])]
        )


class BaseUserModel(AbstractSharedModel, AbstractBaseUser, PermissionsMixin):
    """Template for base user model to be built upon by external applications"""

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def __str__(self) -> str:
        username = getattr(self, self.USERNAME_FIELD, self.id)
        return str(username)
