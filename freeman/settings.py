from django.conf import settings

FREEMAN_PARAMS_PICK = getattr(settings, "FREEMAN_PICK_PARAM_NAME", "fields")
