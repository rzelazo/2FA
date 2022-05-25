from django.apps import AppConfig


class CodesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'codes'

    def ready(self):
        # Implicitly connects a signal handler decorated with @receiver
        import codes.signals
