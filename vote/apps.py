from django.apps import AppConfig
# from . import signals


class VoteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vote'


def ready(self):
    import vote.signals




