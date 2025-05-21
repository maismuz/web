from django.contrib import admin
from django.urls import path
from apps.contratamuz import views

urlpatterns = [
    path('', views.inicial, name='inicial'),
    path('vagas/', views.listar_vagas, name='listar_vagas'),
    # adicione outras rotas conforme necessário
]
