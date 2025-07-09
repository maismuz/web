from django.urls import path
from . import views
app_name = 'reclamemuz'

urlpatterns = [
    path('home', views.index, name='index'),
    path('denunciar/', views.denuncias, name='denunciar'),
    path('denuncia-sucesso/', views.denuncia_sucesso, name='denuncia_sucesso'),
]
