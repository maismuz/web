from esportemuz.models import *
from esportemuz.serializers import *
from esportemuz.utils import *
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
class ModalidadeViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Modalidade.
    """

    queryset = Modalidade.objects.all().order_by('id')
    serializer_class = ModalidadeSerializer

class EquipeViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Equipe.
    """

    queryset = Equipe.objects.all().order_by('id')
    serializer_class = EquipeSerializer

class TipoCampeonatoViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo TipoCampeonato.
    """

    queryset = TipoCampeonato.objects.all().order_by('id')
    serializer_class = TipoCampeonatoSerializer

class CampeonatoViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Campeonato.
    """

    queryset = Campeonato.objects.all().order_by('id')
    serializer_class = CampeonatoSerializer

    @action(detail=True, methods=['get'], url_path='organizar')
    def organizar_campeonato(self, request, pk=None):
        """
        Uma ação personalizada para organizar um campeonato (exibir equipes ordenadas).
        """

        try:
            campeonato = self.get_object()
            equipes = campeonato.equipes.all().order_by('nome')
            equipe_serializer = EquipeSerializer(equipes, many=True, context={'request': request})
            data = {
                "campeonato_id": str(campeonato.id),
                "nome_campeonato": campeonato.nome,
                "modalidade": campeonato.modalidade.nome,
                "tipo_campeonato": campeonato.tipo_campeonato.nome,
                "data_inicio": campeonato.data_inicio,
                "data_fim": campeonato.data_fim,
                "quantidade_equipes": equipes.count(),
                "tabela": equipe_serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        except Campeonato.DoesNotExist:
            return Response({"error": "Campeonato não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LocalPartidaViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo LocalPartida.
    """

    queryset = LocalPartida.objects.all().order_by('id')
    serializer_class = LocalPartidaSerializer

class StatusPartidaViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo StatusPartida.
    """

    queryset = StatusPartida.objects.all().order_by('id')
    serializer_class = StatusPartidaSerializer

class PartidaViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Partida.
    """

    queryset = Partida.objects.all().order_by('id')
    serializer_class = PartidaSerializer

class ClassificacaoViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Classificacao.
    """
    
    queryset = Classificacao.objects.all().order_by('id')
    serializer_class = ClassificacaoSerializer

    @action(detail=False, methods=['get'], url_path='tabela/(?P<campeonato_id>[^/.]+)')
    def tabela_campeonato(self, request, campeonato_id=None):
        """
        Exibir a tabela de classificação de um campeonato específico.
        """

        classificacoes = Classificacao.objects.filter(campeonato__id=campeonato_id).order_by(
            '-pontos',
            '-saldo_gols',
            '-vitorias',
            '-gols_pro'
        )
        serializer = self.get_serializer(classificacoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)