from django.urls import path

from . import views

urlpatterns = [
    path('', views.categoria_objeto, name='categoria_objeto'),
    path('conversar/<int:destinatario_id>/', views.iniciar_conversa, name='iniciar_conversa'),
    path('home/', views.home_view, name='home'),
    path('adicionar_objeto/', views.adicionar_objeto, name='adicionar_objeto'), 
]