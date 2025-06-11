from django.urls import path
from . import views

urlpatterns = [
    path('veiculo/cadastrar', views.cadastrar_veiculo, name='cadastrar_veiculo'),
]