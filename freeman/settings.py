from django.conf import settings

FREEMAN_PICK_PARAM_NAME: str = getattr(settings, "FREEMAN_PICK_PARAM_NAME", "fields")
FREEMAN_ALLOW_MULTIPLE_TOKENS_PER_USER: bool = getattr(
    settings, "FREEMAN_ALLOW_MULTIPLE_TOKENS_PER_USER", False
)
