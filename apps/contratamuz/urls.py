from apps.contratamuz import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicial, name='index '),
    path('vagas/', views.listar_vagas, name='listar_vagas'),
    path('servicos/', views.listar_servicos, name='listar_servicos'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
