from django.urls import path
from . import views

urlpatterns = [
    path('veiculo/cadastrar', views.cadastrar_veiculo, name='cadastrar_veiculo'),
    path('veiculos/', views.lista_veiculos, name='lista_veiculos'),
]