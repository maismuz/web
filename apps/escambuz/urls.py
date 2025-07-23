from django.urls import path
from . import views

urlpatterns = [
    # Rota para a página inicial do Escambuz (com o carrossel)
    # Acessível em: /escambuz/
    path('', views.home_view, name='escambuz-index'),

    # Rota para a página de gerenciamento de Categorias e Objetos
    # Acessível em: /escambuz/gerenciar/
    path('gerenciar/', views.categoria_objeto_view, name='categoria_objeto'),
    
    # Rota interna para processar o formulário de adição de objeto (não é acessada diretamente)
    path('adicionar_objeto/', views.adicionar_objeto, name='adicionar_objeto'),

    # Rota para a conversa entre usuários
    # Acessível em: /escambuz/conversar/1/ (onde 1 é o ID do usuário)
    path('conversar/<int:destinatario_id>/', views.iniciar_conversa, name='iniciar_conversa'),
]