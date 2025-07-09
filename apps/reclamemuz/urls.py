from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='index'),
    path('pagina_denuncias', views.listar_denuncias, name='listar_denuncias'),
]
