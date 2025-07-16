from django.urls import path
from . import views

urlpatterns = [
    path('motoristas/', views.motoristas_table_view, name='motoristas_table'),
    path('combustiveis/', views.combustiveis_table_view, name='combustiveis_table'),
    path('tipo_veiculos/', views.tipo_veiculos_table_view, name='tipo_veiculos_table'),
    path('veiculos/', views.veiculos_table_view, name='veiculos_table'),
    path('locais/', views.locais_table_view, name='locais_table'),
    path('escala_veiculos/', views.escala_veiculos_table_view, name='escala_veiculos_table'),
    path('horario_transportes/', views.horario_transportes_table_view, name='horario_transportes_table'),
    path('viagens/', views.viagens_table_view, name='viagens_table'),
    path('passageiros/', views.passageiros_table_view, name='passageiros_table'),
    path('pontos/', views.pontos_table_view, name='pontos_table'),
    path('paradas/', views.paradas_table_view, name='paradas_table'),
    path('ocupacao_veiculos/', views.ocupacao_veiculos_table_view, name='ocupacao_veiculos_table'),
    # You might want a default table view or a list of tables here
    # For now, let's just redirect to motoristas as an example if someone hits /tabela/
    path('', views.motoristas_table_view, name='default_table_view'),
]