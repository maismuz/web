from apps.esportemuz.routers import router
from apps.esportemuz.views import *
from django.urls import include, path

app_name = 'esportemuz'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Home
    path('', HomeView.as_view(), name='home'),

    # Campeonatos
    path('campeonatos/', CampeonatoListView.as_view(), name='campeonato_list'),

    # Equipes
    path('equipes/', EquipeListView.as_view(), name='equipe_list'),
]
