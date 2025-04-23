"""
Configuração WSGI para o projeto MaisMuz Web.

Este arquivo expõe o callable WSGI como uma variável de nível de módulo chamada ``application``.

Para mais informações sobre este arquivo, consulte:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Define a configuração padrão do Django para o ambiente
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Instancia o aplicativo WSGI
application = get_wsgi_application()
