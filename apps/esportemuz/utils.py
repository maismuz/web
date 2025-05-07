from esportemuz.models import *
from rest_framework.response import Response
from rest_framework import status

def organizar_pontos_corridos(self, campeonato):
        equipes = campeonato.equipes.all()
        for equipe in equipes:
            Classificacao.objects.create(campeonato=campeonato, equipe=equipe)
        
        # Ordenação alfabética para pontos corridos (sem grupos)
        equipes_sorted = sorted(equipes, key=lambda e: e.nome)
        # Classificar em ordem alfabética, você pode ajustar isso dependendo da lógica real.
        for idx, equipe in enumerate(equipes_sorted):
            classificacao = Classificacao.objects.get(campeonato=campeonato, equipe=equipe)
            classificacao.posicao = idx + 1
            classificacao.save()

def organizar_fase_grupos(self, campeonato):
        num_grupos = int(self.request.data.get('num_grupos'))
        equipes = campeonato.equipes.all()

        # Em fase de grupos, vamos dividir as equipes em grupos aleatórios
        import random
        random.shuffle(equipes)

        grupos = []
        for i in range(num_grupos):
            grupo = Grupo.objects.create(nome=f'Grupo {i+1}', campeonato=campeonato)
            grupos.append(grupo)

        for idx, equipe in enumerate(equipes):
            grupo_idx = idx % num_grupos
            grupo = grupos[grupo_idx]
            grupo.equipes.add(equipe)
            grupo.save()

        # Gerar partidas para cada grupo
        for grupo in grupos:
            equipes_grupo = grupo.equipes.all()
            for i in range(len(equipes_grupo)):
                for j in range(i+1, len(equipes_grupo)):
                    # Criar partidas para o grupo
                    Partida.objects.create(
                        campeonato=campeonato,
                        grupo=grupo,
                        equipe_mandante=equipes_grupo[i],
                        equipe_visitante=equipes_grupo[j],
                        data_hora=campeonato.data_inicio,  # Você pode personalizar isso
                        local="Local Exemplo",  # Também pode ser personalizado
                        status=StatusPartida.objects.first()  # Exemplo de status
                    )

def organizar_mata_mata(self, campeonato):
        equipes = campeonato.equipes.all()
        num_equipes = len(equipes)

        # Verifica se o número de equipes é válido para mata-mata
        if num_equipes < 2 or (num_equipes & (num_equipes - 1)) != 0:
            return Response({'detail': 'Número inválido de equipes para mata-mata.'}, status=status.HTTP_400_BAD_REQUEST)

        # Criar partidas de mata-mata
        for i in range(0, num_equipes, 2):
            Partida.objects.create(
                campeonato=campeonato,
                equipe_mandante=equipes[i],
                equipe_visitante=equipes[i + 1],
                data_hora=campeonato.data_inicio,  # Você pode personalizar isso
                local="Local Exemplo",  # Também pode ser personalizado
                status=StatusPartida.objects.first()  # Exemplo de status
            )