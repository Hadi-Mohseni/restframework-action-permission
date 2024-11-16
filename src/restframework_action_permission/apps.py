from restframework_action_permission.management import create_permission
from django.db.models.signals import post_migrate
from django.apps import AppConfig


class RestframeworkActionPermissionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "restframework_action_permission"

    def ready(self) -> None:
        post_migrate.connect(create_permission)
        return super().ready()
