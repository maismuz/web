from apps.esportemuz.models import *
from apps.esportemuz.serializers import *
from apps.esportemuz.utils import *
from django.db.models import Sum
from itertools import combinations
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F

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
            data={
                'partidas': data
            },
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

    # @action(detail=True, methods=['post'], url_path='criar-campeonato', url_name='criar-campeonato')
    # def criar_campeonato(self, request, pk=None):
    #     """
    #     Criar um campeonato com base no ID fornecido.
    #     """

    #     campeonato = self.get_object()

    #     for equipe in campeonato.equipes.all().order_by('nome'):
    #         Classificacao.objects.get_or_create(
    #             campeonato=campeonato,
    #             equipe=equipe,
    #             defaults={
    #                 'pontos': 0,
    #                 'vitorias': 0,
    #                 'empates': 0,
    #                 'derrotas': 0,
    #                 'gols_pro': 0,
    #                 'gols_contra': 0,
    #                 'saldo_gols': 0
    #             }
    #         )

    #     return Response(
    #         data={
    #             'message': 'Campeonato criado com sucesso!'
    #         },
    #         status=status.HTTP_201_CREATED
    #     )
    
    @action(detail=True, methods=['post'], url_path='encerrar-campeonato', url_name='encerrar-campeonato')
    def encerrar_campeonato(self, request, pk=None):
        """
        Encerrar um campeonato com base no ID fornecido.
        """

        campeonato = self.get_object()
        classificacoes = Classificacao.objects.filter(campeonato=campeonato).order_by('-pontos', '-vitorias', '-saldo_gols', '-gols_pro')

        if not classificacoes.exists():
            return Response(
                data={
                    'message': 'Nenhuma classificação encontrada para o campeonato.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        campeao = classificacoes.first()
        rebaixado = classificacoes.last()
        campeonato.encerrado = True
        
        campeonato.save()

        return Response(
            data={
                'message': 'Campeonato encerrado com sucesso!',
                'campeao': {
                    'equipe': campeao.equipe.nome,
                    'pontos': campeao.pontos
                },
                'rebaixado': {
                    'equipe': rebaixado.equipe.nome,
                    'pontos': rebaixado.pontos
                }
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='criar-partidas', url_name='criar-partidas')
    def criar_partidas(self, request, pk=None):
        """
        Gerar partidas de ida e volta para o campeonato com base no ID fornecido.
        """

        campeonato = self.get_object()
        equipes = list(campeonato.equipes.all().order_by('nome'))
        partidas = []

        for equipe1, equipe2 in combinations(equipes, 2):
            # Partida de ida
            partida_ida, created_ida = Partida.objects.get_or_create(
                campeonato=campeonato,
                equipe_mandante=equipe1,
                equipe_visitante=equipe2,
                defaults={
                    'data_hora': None,
                    'local': None,
                    'gols_mandante': 0,
                    'gols_visitante': 0,
                    'encerrada': False
                }
            )

            if created_ida:
                partidas.append(f'{equipe1.nome} x {equipe2.nome} (ida)')
            else:
                partidas.append(f'Partida {equipe1.nome} x {equipe2.nome} (ida) já existe.')

            # Partida de volta
            partida_volta, created_volta = Partida.objects.get_or_create(
                campeonato=campeonato,
                equipe_mandante=equipe2,
                equipe_visitante=equipe1,
                defaults={
                    'data_hora': None,
                    'local': None,
                    'gols_mandante': 0,
                    'gols_visitante': 0,
                    'encerrada': False
                }
            )

            if created_volta:
                partidas.append(f'{equipe2.nome} x {equipe1.nome} (volta)')
            else:
                partidas.append(f'Partida {equipe2.nome} x {equipe1.nome} (volta) já existe.')

        if not partidas:
            return Response(
                data={
                    'message': 'Partidas já foram criadas anteriormente.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data={
                'message': 'Partidas de ida e volta criadas com sucesso!',
                'partidas': partidas
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], url_path='desfazer-partidas', url_name='desfazer-partidas')
    def desfazer_partidas(self, request, pk=None):
        """
        Desfazer partidas do campeonato com base no ID fornecido.
        """

        campeonato = self.get_object()
        partidas = Partida.objects.filter(campeonato=campeonato)

        if not partidas.exists():
            return Response(
                data={
                    'message': 'Nenhuma partida encontrada para desfazer.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        partidas.delete()

        classificacoes = Classificacao.objects.filter(campeonato=campeonato)

        classificacoes.update(
            pontos=0,
            partidas_jogadas=0,
            vitorias=0,
            empates=0,
            derrotas=0,
            gols_pro=0,
            gols_contra=0,
            saldo_gols=0
        )

        return Response(
            data={
                'message': 'Partidas desfeitas com sucesso!'
            },
            status=status.HTTP_200_OK
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
        total_gols = Partida.objects.filter(campeonato=campeonato).aggregate(total=Sum(F('gols_mandante') + F('gols_visitante')))['total'] or 0
        media_gols_partida = round(total_gols / total_partidas, 2) if total_partidas > 0 else 0
        menor_pontuacao = min(c.pontos for c in classificacoes) if classificacoes else 0
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
                'menor_pontuacao': menor_pontuacao,
                'maior_pontuacao': maior_pontuacao,
                'maior_goleada': maior_goleada,
                'campeao': {
                    'equipe': classificacoes.first().equipe.nome if classificacoes.exists() else None,
                    'pontos': classificacoes.first().pontos if classificacoes.exists() else None
                } if campeonato.encerrado else None,
                'rebaixado': {
                    'equipe': classificacoes.last().equipe.nome if classificacoes.exists() else None,
                    'pontos': classificacoes.last().pontos if classificacoes.exists() else None
                } if campeonato.encerrado else None
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
                'data_hora': partida.data_hora.strftime('%d/%m/%Y %H:%M') if partida.data_hora else None,
                'local': partida.local.nome if partida.local else None,
                'placar': f'{partida.gols_mandante} x {partida.gols_visitante}' if partida.encerrada else None,
                'encerrada': partida.encerrada
            } for partida in partidas
        ]

        return Response(
            data={
                'partidas': data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'], url_path='partidas-encerradas', url_name='partidas-encerradas')
    def partidas_encerradas(self, request, pk=None):
        """
        Retorna as partidas encerradas para o campeonato com base no ID fornecido.
        """

        campeonato = self.get_object()
        partidas = campeonato.partidas.filter(encerrada=True).order_by('-data_hora')
        data = [
            {
                'id': partida.id,
                'equipe_mandante': partida.equipe_mandante.nome,
                'equipe_visitante': partida.equipe_visitante.nome,
                'data_hora': partida.data_hora.strftime('%d/%m/%Y %H:%M') if partida.data_hora else None,
                'local': partida.local.nome if partida.local else None,
                'placar': f'{partida.gols_mandante} x {partida.gols_visitante}' if partida.encerrada else None,
                'encerrada': partida.encerrada
            } for partida in partidas
        ]

        return Response(
            data={
                'partidas': data
            },
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
        
        try:
            gols_mandante = int(request.data.get('gols_mandante'))
            gols_visitante = int(request.data.get('gols_visitante'))
        except (ValueError, TypeError):
            return Response(
                data={
                    'message': 'gols_mandante e gols_visitante devem ser números inteiros.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if gols_mandante is None or gols_visitante is None:
            return Response(
                data={
                    'message': 'gols_mandante e gols_visitante são obrigatórios.'
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

        equipe_mandante.partidas_jogadas += 1
        equipe_visitante.partidas_jogadas += 1
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

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.order_by('-pontos', '-saldo_gols', '-gols_pro', '-gols_contra', '-vitorias', '-empates', '-derrotas', 'equipe__nome')