from django.apps import AppConfig


class ActivitytrackConfig(AppConfig):
    name = 'activitytrack'

    def ready(self):
        from .signals import log_user_logged_in_success