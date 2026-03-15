from django.apps import AppConfig


class PostingConfig(AppConfig):
    name = 'posting'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import posting.signals
