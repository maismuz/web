from django.urls import path
from .views import IndexView, EventosView, CadastrarEventosView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('eventos/', EventosView.as_view(), name='eventos'),
    path('cadastrar_eventos/', CadastrarEventosView.as_view(), name='cadastrar_eventos'),
]
