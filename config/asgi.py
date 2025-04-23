"""
Configuração ASGI para o projeto MaisMuz Web.

Este arquivo expõe o callable ASGI como uma variável de nível de módulo chamada ``application``.

Para mais informações sobre este arquivo, consulte:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Define a configuração padrão do Django para o ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Instancia o aplicativo ASGI
application = get_asgi_application()
