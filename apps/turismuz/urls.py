from django.urls import path
from . import views

urlpatterns = [
    path('hometur/', views.hometur, name='hometur'),
    path('estabelecimentos/', views.estabelecimentos, name='estabelecimentos'),
    path('estabelecimento/<int:pk>/', views.estabelecimento_detail, name='estabelecimento_detail'),
    path('guias/', views.guias, name='guias'),
    path('publicacoes/', views.publicacoes, name='publicacoes'),
    path('publicacoes/<int:pk>/', views.publicacao_detail, name='publicacao_detail'),
    path('guia/<int:pk>/', views.guia_detail, name='guia_detail'),
]
