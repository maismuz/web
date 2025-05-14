from django.urls import path
from . import views

urlpatterns = [
    path('', views.homedoa, name='homedoa'),  # URL raiz do app
    path('homedoa/', views.homedoa, name='homedoa'),  # URL para 'index/'
    path('instrucoes/', views.instrucoes, name='instrucoes'), 
    path('doacao/', views.instrucoes, name='doacao'), 
    path('doador/', views.instrucoes, name='doador'), 
    path('login/', views.instrucoes, name='login'), 
    path('ongs/', views.instrucoes, name='ongs'), 
]
