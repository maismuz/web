from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Páginas principais
    path('', views.inicial, name='home'),
    path('vagas/', views.listar_vagas, name='listar_vagas'),
    path('servicos/', views.listar_servicos, name='listar_servicos'),
    path('servicos/<int:servico_id>/', views.detalhe_servico, name='detalhe_servico'),
    path('publicar/', views.publicar_servico, name='publicar_servico'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    
    # URLs de autenticação
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('meus-servicos/', views.meus_servicos_view, name='meus_servicos'),
    path('publicar-servico/', views.publicar_servico_auth, name='publicar_servico_auth'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

