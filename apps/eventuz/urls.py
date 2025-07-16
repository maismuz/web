from apps.eventuz.views import IndexView, EventosView, CadastrarEventosView, HistoricoView
from django.urls import path
from . import views


app_name = 'eventuz'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('eventos/', EventosView.as_view(), name='eventos'),
    path('cadastrar_eventos/', CadastrarEventosView.as_view(), name='cadastrar_eventos'),
    path('historico/', HistoricoView.as_view(), name='historico'),
    path('evento/<int:pk>/', views.DetalhesEventoView.as_view(), name='detalhes_evento'),
]
