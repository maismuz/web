# apps/movemuz/apps.py
from django.apps import AppConfig

class MovemuzConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.movemuz' # This should match 'apps.movemuz' in INSTALLED_APPS
    verbose_name = "Transporte MoveMuz" # Optional: a more descriptive name for admin