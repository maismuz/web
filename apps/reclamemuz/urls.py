from django.urls import path
from . import views
app_name = 'reclamemuz'

urlpatterns = [
    # path('home', views.index, name='index'),
    path('denunciar/', views.denuncias, name='denunciar'),
    path('denuncia_sucesso/', views.denuncia_sucesso, name='denuncia_sucesso'),
    # path('pagina_denuncias/', views.listar_denuncias, name='listar_denuncias'),
    path('denuncias/', views.listar_denuncias, name='listar_denuncias'),
    path('denuncia/<int:denuncia_id>/', views.detalhe_denuncia, name='detalhe_denuncia'),

]
