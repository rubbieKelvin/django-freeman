import types
from django.apps import AppConfig


class AuthappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "freeman.authapp"

    def __init__(self, app_name: str, app_module: types.ModuleType | None) -> None:
        self.signals_initialized = False
        super().__init__(app_name, app_module)

    def ready(self) -> None:
        if not self.signals_initialized:
            # The ready() method may be executed more than once during testing,
            # so you may want to guard your signals from duplication,
            # especially if you’re planning to send them within tests.
            self.signals_initialized = True
            from . import signals  # type: ignore
        return super().ready()
