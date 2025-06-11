"""
Configuração de URLs geral.

Aqui, são configuradas as rotas principais da aplicação.
Inclui rotas para:
- Aplicações
"""

from django.urls import path, include, re_path
from config import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [

    path('admin/', admin.site.urls),
    path('turismuz/', include('apps.turismuz.urls')),
    path('doamuz/', include('apps.doamuz.urls')),  # Certifique-se de que o caminho está correto

    path("", include("apps.core.urls")),]



# Configuração de arquivos de mídia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)