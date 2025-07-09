# config/urls.py (assuming this is your main project urls file)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import homepage_view # Assuming homepage is in apps.core for this setup

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls),
    path('forms/', include('apps.movemuz.urls_forms')), # Corrected path
    path('tabela/', include('apps.movemuz.urls_table')), # Corrected path
    path('pagina/', include('apps.movemuz.urls_page')), # Corrected path
    path('', homepage_view, name='homepage'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Use STATIC_ROOT for staticfiles_dirs setup
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    path('veiculo/cadastrar', views.cadastrar_veiculo, name='cadastrar_veiculo'),
    path('veiculos/', views.lista_veiculos, name='lista_veiculos'),
]
>>>>>>> c82908cbfa9471dfd69a3d07cc441a2dfeda63f0
