from django.apps import AppConfig


class ConfigpanelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "configpanel"

    def ready(self) -> None:
        import configpanel.signals  # noqa: F401
