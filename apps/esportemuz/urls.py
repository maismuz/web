from apps.esportemuz.routers import router
from apps.esportemuz.views import *
from django.urls import include, path

app_name = 'esportemuz'

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', IndexView.as_view(), name='index'),
    path('equipe/', EquipeView.as_view(), name='equipe'),
    path('campeonato/', CampeonatoView.as_view(), name='campeonato'),
]
