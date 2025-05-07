from django.urls import path
from . import views

urlpatterns = [
    path('hometur/', views.hometur, name='hometur'),
    path('estabelecimentos/', views.estabelecimentos, name='estabelecimentos'),
    path('guias/', views.guias, name='guias'),
    path('publicacoes/', views.publicacoes, name='publicacoes'),
    path('publicacoes/<int:pk>/', views.publicacao_detail, name='publicacao_detail'),
]
