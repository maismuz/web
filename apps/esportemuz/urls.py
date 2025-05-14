from apps.esportemuz.views import *
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'modalidades', ModalidadeViewSet)
router.register(r'equipes', EquipeViewSet)
router.register(r'tipos', TipoCampeonatoViewSet)
router.register(r'campeonatos', CampeonatoViewSet)
router.register(r'locais', LocalPartidaViewSet)
router.register(r'partidas', PartidaViewSet)
router.register(r'classificacoes', ClassificacaoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
