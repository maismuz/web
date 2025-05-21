from apps.contratamuz import views
from django.urls import path

urlpatterns = [
    path('', views.inicial, name='index '),
    path('vagas/', views.listar_vagas, name='listar_vagas'),
    path('servicos/', views.listar_servicos, name='listar_servicos'),
]
