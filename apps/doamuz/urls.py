from django.urls import path
from . import views

urlpatterns = [
    path('', views.homedoa, name='homedoa'),  # URL raiz do app
    path('homedoa/', views.homedoa, name='homedoa'),  # URL para 'index/'
    path('instrucoes/', views.instrucoes, name='instrucoes'), 
    path('doacao/', views.doacao, name='doacao'), 
    path('doador/', views.doador, name='doador'), 
    path('login/', views.login, name='login'), 
    path('ongs/', views.ongs, name='ongs'), 
]
