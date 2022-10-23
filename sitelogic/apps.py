from django.apps import AppConfig
from django.core.signals import request_finished


class SitelogicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sitelogic'

    def ready(self):
        import sitelogic.signals


