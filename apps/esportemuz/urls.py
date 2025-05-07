from django.urls import include, path
from rest_framework.routers import DefaultRouter
from esportemuz.views import *

router = DefaultRouter()

router.register(r'modalidades', ModalidadeViewSet)
router.register(r'tipos', TipoCampeonatoViewSet)
router.register(r'campeonatos', CampeonatoViewSet)
router.register(r'equipes', EquipeViewSet)
# router.register(r'grupos', GrupoViewSet)
router.register(r'status', StatusPartidaViewSet)
router.register(r'partidas', PartidaViewSet)
router.register(r'classificacoes', ClassificacaoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
