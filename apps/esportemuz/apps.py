from django.apps import AppConfig

class EsportemuzConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.esportemuz'
    verbose_name = 'EsporteMuz'
    verbose_name_plural = 'EsporteMuz'

    # def ready(self):
    #     import apps.esportemuz.signals