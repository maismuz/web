from apps.turismuz import views
from django.urls import path

urlpatterns = [
    path('hometur/', views.hometur, name='hometur'),
    path('estabelecimentos/', views.estabelecimentos, name='estabelecimentos'),
    path('estabelecimento/<int:pk>/', views.estabelecimento_detail, name='estabelecimento_detail'),
    path('guias/', views.guias, name='guias'),
    path('publicacoes/', views.publicacoes, name='publicacoes'),
    path('publicacoes/<int:pk>/', views.publicacao_detail, name='publicacao_detail'),
    path('guia/<int:pk>/', views.guia_detail, name='guia_detail'),
    path('add-publicacao/', views.add_publicacao, name='add_publicacao'),
    path('add-estabelecimento/', views.add_estabelecimento, name='add_estabelecimento'),
    path('add-guia/', views.add_guia, name='add_guia'),
]
