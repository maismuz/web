from django.urls import include, path
from rest_framework.routers import DefaultRouter
from esportemuz.views import *

router = DefaultRouter()

router.register(r'modalidades', ModalidadeViewSet, 'modalidade')
router.register(r'tipos-de-campeonatos', TipoCampeonatoViewSet, 'tipo-campeonato')
router.register(r'campeonatos', CampeonatoViewSet, 'campeonato')
router.register(r'equipes', EquipeViewSet, 'equipe')
router.register(r'grupos', GrupoViewSet, 'grupo')
router.register(r'status', StatusPartidaViewSet, 'status-partida')
router.register(r'partidas', PartidaViewSet, 'partida')
router.register(r'classificacoes', ClassificacaoViewSet, 'classificacao')

urlpatterns = [
    path('api/', include(router.urls)),
]
