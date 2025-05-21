from apps.eventuz.views import IndexView, EventosView, CadastrarEventosView
from django.urls import path

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('eventos/', EventosView.as_view(), name='eventos'),
    path('cadastrar_eventos/', CadastrarEventosView.as_view(), name='cadastrar_eventos'),
]
