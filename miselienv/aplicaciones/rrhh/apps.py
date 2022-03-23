from django.apps import AppConfig


class RrhhConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aplicaciones.rrhh'

    def ready(self):
        from . import signals
