from apps.esportemuz.viewsets import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'modalidades', ModalidadeViewSet)
router.register(r'equipes', EquipeViewSet)
router.register(r'tipos', TipoCampeonatoViewSet)
router.register(r'campeonatos', CampeonatoViewSet)
router.register(r'locais', LocalPartidaViewSet)
router.register(r'partidas', PartidaViewSet)
router.register(r'classificacoes', ClassificacaoViewSet)