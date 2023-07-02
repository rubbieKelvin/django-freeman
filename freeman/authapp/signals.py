import typing

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import AuthenticatorModel


# create an authenticator for each user when there
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_authenticator(
    sender: type[models.Model],
    instance: models.Model,
    created: bool,
    **kwargs: typing.Any
):
    if created:
        AuthenticatorModel.insertSingle({"user": instance})
