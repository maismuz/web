from apps.contratamuz import views
from django.urls import path

urlpatterns = [
    path('', views.inicial, name='inicial'),
    path('vagas/', views.listar_vagas, name='listar_vagas'),
]
