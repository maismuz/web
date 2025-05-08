from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from esportemuz.models import *
from esportemuz.serializers import *
from esportemuz.utils import *

# Create your views here.
class ModalidadeViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Modalidade.
    """

    queryset = Modalidade.objects.all()
    serializer_class = ModalidadeSerializer

class TipoCampeonatoViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo TipoCampeonato.
    """

    queryset = TipoCampeonato.objects.all()
    serializer_class = TipoCampeonatoSerializer

class CampeonatoViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Campeonato.
    """

    queryset = Campeonato.objects.all()
    serializer_class = CampeonatoSerializer

class EquipeViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Equipe.
    """

    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

class StatusPartidaViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo StatusPartida.
    """

    queryset = StatusPartida.objects.all()
    serializer_class = StatusPartidaSerializer

class PartidaViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Partida.
    """

    queryset = Partida.objects.all()
    serializer_class = PartidaSerializer

class ClassificacaoViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Classificacao.
    """
    
    queryset = Classificacao.objects.all()
    serializer_class = ClassificacaoSerializer