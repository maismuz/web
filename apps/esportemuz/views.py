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

    @action(detail=True, methods=['post'])
    def organizar(self, request, pk=None):
        campeonato = self.get_object()
        tipo_campeonato = campeonato.tipo_campeonato.nome

        if tipo_campeonato == 'Pontos Corridos':
            organizar_pontos_corridos(campeonato)
        elif tipo_campeonato == 'Fase de Grupos':
            organizar_fase_grupos(campeonato)
        elif tipo_campeonato == 'Mata-Mata':
            organizar_mata_mata(campeonato)
        else:
            return Response({'detail': 'Tipo de campeonato não suportado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': 'Campeonato organizado com sucesso.'}, status=status.HTTP_200_OK)

# class EquipeViewSet(viewsets.ModelViewSet):
#     """
#     Um conjunto de visualizações para lidar com operações CRUD no modelo Equipe.
#     """
#     queryset = Equipe.objects.all()
#     serializer_class = EquipeSerializer

# class GrupoViewSet(viewsets.ModelViewSet):
#     """
#     Um conjunto de visualizações para lidar com operações CRUD no modelo Grupo.
#     """
#     queryset = Grupo.objects.all()
#     serializer_class = GrupoSerializer

#     def perform_create(self, serializer):
#         grupo = serializer.save()

#         for equipe in grupo.equipes.all():
#             if Grupo.objects.filter(campeonato=grupo.campeonato, equipes=equipe).exists():
#                 return Response({'detail': f'A equipe {equipe.nome} já está em outro grupo.'}, status=status.HTTP_400_BAD_REQUEST)
            
#     def perform_update(self, serializer):
#         grupo = serializer.save()

#         for equipe in grupo.equipes.all():
#             if Grupo.objects.filter(campeonato=grupo.campeonato, equipes=equipe).exclude(id=grupo.id).exists():
#                 return Response({'detail': f'A equipe {equipe.nome} já está em outro grupo.'}, status=status.HTTP_400_BAD_REQUEST)

# class StatusPartidaViewSet(viewsets.ModelViewSet):
#     """
#     Um conjunto de visualizações para lidar com operações CRUD no modelo StatusPartida.
#     """
#     queryset = StatusPartida.objects.all()
#     serializer_class = StatusPartidaSerializer

# class PartidaViewSet(viewsets.ModelViewSet):
#     """
#     Um conjunto de visualizações para lidar com operações CRUD no modelo Partida.
#     """
#     queryset = Partida.objects.all()
#     serializer_class = PartidaSerializer

#     def perform_create(self, serializer):
#         instance = serializer.save()

#         if instance.status.nome == 'Finalizada':
#             atualizar_classificacao(instance.campeonato)

#     def perform_update(self, serializer):
#         instance = serializer.save()

#         if instance.status.nome == 'Finalizada':
#             atualizar_classificacao(instance.campeonato)

# class ClassificacaoViewSet(viewsets.ModelViewSet):
#     """
#     Um conjunto de visualizações para lidar com operações CRUD no modelo Classificacao.
#     """
#     queryset = Classificacao.objects.all()
#     serializer_class = ClassificacaoSerializer