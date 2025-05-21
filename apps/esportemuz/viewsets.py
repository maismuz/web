from apps.esportemuz.models import *
from apps.esportemuz.serializers import *
from apps.esportemuz.utils import *
from django.db.models import Sum
from itertools import combinations
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your viewsets here.
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

    @action(detail=True, methods=['get'], url_path='historico', url_name='historico')
    def historico(self, request, pk=None):
        """
        Retorna o histórico de partidas da equipe com base no ID fornecido.
        """

        equipe = self.get_object()
        partidas_mandante = Partida.objects.filter(equipe_mandante=equipe, encerrada=True)
        partidas_visitante = Partida.objects.filter(equipe_visitante=equipe, encerrada=True)
        partidas = list(partidas_mandante) + list(partidas_visitante)

        partidas.sort(key=lambda x: x.data_hora, reverse=True)

        data = []

        for partida in partidas:
            venceu = (
                (partida.equipe_mandante == equipe and partida.gols_mandante > partida.gols_visitante) or
                (partida.equipe_visitante == equipe and partida.gols_visitante > partida.gols_mandante)
            )
            serializer = PartidaSerializer(partida, context={'request': request}).data
            serializer['venceu'] = venceu

            data.append(serializer)

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'], url_path='estatisticas', url_name='estatisticas')
    def estatisticas(self, request, pk=None):
        """
        Retorna as estatísticas da equipe com base no ID fornecido.
        """

        equipe = self.get_object()
        classificacoes = Classificacao.objects.filter(equipe=equipe)

        total_partidas = sum(c.vitorias + c.empates + c.derrotas for c in classificacoes)
        total_pontos = sum(c.pontos for c in classificacoes)
        vitorias = sum(c.vitorias for c in classificacoes)
        empates = sum(c.empates for c in classificacoes)
        derrotas = sum(c.derrotas for c in classificacoes)
        gols_pro = sum(c.gols_pro for c in classificacoes)
        gols_contra = sum(c.gols_contra for c in classificacoes)
        media_gols_partida = gols_pro / total_partidas if total_partidas > 0 else 0
        saldo_gols = sum(c.saldo_gols for c in classificacoes)

        return Response(
            data={
                "total_partidas": total_partidas,
                "total_pontos": total_pontos,
                "vitorias": vitorias,
                "empates": empates,
                "derrotas": derrotas,
                "gols_pro": gols_pro,
                "gols_contra": gols_contra,
                "media_gols_partida": media_gols_partida,
                "saldo_gols": saldo_gols
            },
            status=status.HTTP_200_OK
        )

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

    @action(detail=True, methods=['post'], url_path='criar-campeonato', url_name='criar-campeonato')
    def criar_campeonato(self, request, pk=None):
        """
        Criar um campeonato com base no ID fornecido.
        """

        campeonato = self.get_object()

        for equipe in campeonato.equipes.all().order_by('nome'):
            Classificacao.objects.get_or_create(
                campeonato=campeonato,
                equipe=equipe,
                defaults={
                    'pontos': 0,
                    'vitorias': 0,
                    'empates': 0,
                    'derrotas': 0,
                    'gols_pro': 0,
                    'gols_contra': 0,
                    'saldo_gols': 0
                }
            )

        return Response(
            data={
                'message': 'Campeonato criado com sucesso!'
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], url_path='gerar-partidas', url_name='gerar-partidas')
    def gerar_partidas(self, request, pk=None):
        """
        Gerar partidas para o campeonato com base no ID fornecido.
        """

        campeonato = self.get_object()
        equipes = list(campeonato.equipes.all().order_by('nome'))
        partidas = []

        for equipe_mandante, equipe_visitante in combinations(equipes, 2):
            partida, created = Partida.objects.get_or_create(
                campeonato=campeonato,
                equipe_mandante=equipe_mandante,
                equipe_visitante=equipe_visitante,
                defaults={
                    'data_hora': now(),
                    'local': LocalPartida.objects.get_or_create(nome='poliesportivo')[0],
                    'gols_mandante': 0,
                    'gols_visitante': 0,
                    'encerrada': False
                }
            )

            if created:
                partidas.append(str(partida))
            else:
                partidas.append(f'Partida {partida} já existe.')
        
        if not partidas:
            return Response(
                data={
                    'message': 'Partidas já foram geradas anteriormente.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            data={
                'message': 'Partidas geradas com sucesso!',
                'partidas': partidas
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'], url_path='estatisticas', url_name='estatisticas')
    def estatisticas(self, request, pk=None):
        """
        Retorna as estatísticas do campeonato com base no ID fornecido.
        """

        campeonato = self.get_object()
        classificacoes = Classificacao.objects.filter(campeonato=campeonato).order_by('-pontos', '-vitorias', '-saldo_gols', '-gols_pro')
        total_partidas = Partida.objects.filter(campeonato=campeonato).count()
        total_partidas_encerradas = Partida.objects.filter(campeonato=campeonato, encerrada=True).count()
        total_partidas_nao_encerradas = total_partidas - total_partidas_encerradas
        total_gols = Partida.objects.filter(campeonato=campeonato).aggregate(Sum('gols_mandante'))['gols_mandante__sum'] + Partida.objects.filter(campeonato=campeonato).aggregate(Sum('gols_visitante'))['gols_visitante__sum']
        media_gols_partida = round(total_gols / total_partidas, 2) if total_partidas > 0 else 0
        maior_pontuacao = max(c.pontos for c in classificacoes) if classificacoes else 0
        maior_goleada = max(
            (partida.gols_mandante if partida.gols_mandante > partida.gols_visitante else partida.gols_visitante) for partida in Partida.objects.filter(campeonato=campeonato, encerrada=True)
        ) if Partida.objects.filter(campeonato=campeonato, encerrada=True).exists() else 0
        
        return Response(
            data={
                'total_partidas': total_partidas,
                'total_partidas_encerradas': total_partidas_encerradas,
                'total_partidas_nao_encerradas': total_partidas_nao_encerradas,
                'total_gols': total_gols,
                'media_gols_partida': media_gols_partida,
                'maior_pontuacao': maior_pontuacao,
                'maior_goleada': maior_goleada,
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'], url_path='partidas-agendadas', url_name='partidas-agendadas')
    def partidas_agendadas(self, request, pk=None):
        """
        Retorna as partidas agendadas para o campeonato com base no ID fornecido.
        """

        campeonato = self.get_object()
        partidas = campeonato.partidas.select_related('equipe_mandante', 'equipe_visitante', 'local').filter(encerrada=False).order_by('data_hora')
        data = [
            {
                'id': partida.id,
                'equipe_mandante': partida.equipe_mandante.nome,
                'equipe_visitante': partida.equipe_visitante.nome,
                'data_hora': partida.data_hora.strftime('%d/%m/%Y %H:%M'),
                'local': partida.local.nome,
                'placar': f'{partida.gols_mandante} x {partida.gols_visitante}' if partida.encerrada else None,
                'encerrada': partida.encerrada
            } for partida in partidas
        ]

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

class LocalPartidaViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo LocalPartida.
    """

    queryset = LocalPartida.objects.all().order_by('id')
    serializer_class = LocalPartidaSerializer

class PartidaViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Partida.
    """

    queryset = Partida.objects.all().order_by('id')
    serializer_class = PartidaSerializer

    @action(detail=True, methods=['post'], url_path='encerrar-partida')
    def encerrar_partida(self, request, pk=None):
        """
        Encerrar uma partida com base no ID fornecido.
        """

        partida = self.get_object()
        gols_mandante = request.data.get('gols_mandante')
        gols_visitante = request.data.get('gols_visitante')

        if gols_mandante is None or gols_visitante is None:
            return Response(
                data={
                    'message': 'Gols mandante e visitante são obrigatórios.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        partida.gols_mandante = gols_mandante
        partida.gols_visitante = gols_visitante
        partida.encerrada = True

        partida.save()

        # Atualiza a classificação das equipes
        equipe_mandante = Classificacao.objects.get(campeonato=partida.campeonato, equipe=partida.equipe_mandante)
        equipe_visitante = Classificacao.objects.get(campeonato=partida.campeonato, equipe=partida.equipe_visitante)

        equipe_mandante.gols_pro += partida.gols_mandante
        equipe_mandante.gols_contra += partida.gols_visitante
        equipe_visitante.gols_pro += partida.gols_visitante
        equipe_visitante.gols_contra += partida.gols_mandante

        if partida.gols_mandante > partida.gols_visitante:
            equipe_mandante.pontos += 3
            equipe_mandante.vitorias += 1
            equipe_visitante.derrotas += 1
        elif partida.gols_mandante < partida.gols_visitante:
            equipe_visitante.pontos += 3
            equipe_visitante.vitorias += 1
            equipe_mandante.derrotas += 1
        else:
            equipe_mandante.pontos += 1
            equipe_visitante.pontos += 1
            equipe_mandante.empates += 1
            equipe_visitante.empates += 1

        equipe_mandante.saldo_gols = equipe_mandante.gols_pro - equipe_mandante.gols_contra
        equipe_visitante.saldo_gols = equipe_visitante.gols_pro - equipe_visitante.gols_contra

        equipe_mandante.save()
        equipe_visitante.save()

        return Response(
            data={
                'message': 'Partida encerrada e classificação atualizada com sucesso!'
            },
            status=status.HTTP_200_OK
        )

class ClassificacaoViewSet(viewsets.ModelViewSet):
    """
    Um conjunto de visualizações para lidar com operações CRUD no modelo Classificacao.
    """
    
    queryset = Classificacao.objects.select_related('equipe', 'campeonato').all()
    serializer_class = ClassificacaoSerializer