from esportemuz.models import *

def gerar_partidas_automaticamente(campeonato):
    """
    Gera partidas automaticamente para um determinado campeonato.

    Args:
        campeonato (Championship): O campeonato para o qual serão geradas as partidas.

    Retorna:
        None
    """

    equipes = list(campeonato.equipes.all())
    partidas = []

    if campeonato.tipo_campeonato.name == 'Pontos corridos':
        for i in range(len(equipes)):
            for j in range(i + 1, len(equipes)):
                partidas.append(Partida(
                    campeonato=campeonato,
                    equipe_mandante=equipes[i],
                    equipe_visitante=equipes[j],
                    data_hora=None,
                    local=None,
                    status=StatusPartida.objects.get_or_create(nome='Agendada')[0]
                ))
    elif campeonato.tipo_campeonato.name == 'Fase de grupos':
        for grupo in campeonato.grupos.all():
            equipes_grupo = list(grupo.equipes.all())

            for i in range(len(equipes_grupo)):
                for j in range(i + 1, len(equipes_grupo)):
                    partidas.append(Partida(
                        campeonato=campeonato,
                        grupo=grupo,
                        equipe_mandante=equipes_grupo[i],
                        equipe_visitante=equipes_grupo[j],
                        data_hora=None,
                        local=None,
                        status=StatusPartida.objects.get_or_create(nome='Agendada')[0]
                    ))

    Partida.objects.bulk_create(partidas)

def atualizar_classificacao(campeonato):
    """
    Atualiza a classificação de um campeonato com base nas partidas jogadas.

    Args:
        campeonato (Championship): O campeonato cuja classificação será atualizada.

    Retorna:
        None
    """

    Classificacao.objects.filter(campeonato=campeonato).delete()

    dados = {}

    for equipe in campeonato.equipes.all():
        dados[equipe.id] = {
            'equipe': equipe,
            'pontos': 0,
            'vitorias': 0,
            'empates': 0,
            'derrotas': 0,
            'gols_pro': 0,
            'gols_contra': 0,
            'saldo_gols': 0,
        }

    for partida in Partida.objects.filter(campeonato=campeonato, status=StatusPartida.objects.get_or_create('Finalizada')):
        equipe_mandante = partida.equipe_mandante
        equipe_visitante = partida.equipe_visitante
        gols_mandante = partida.gols_mandante
        gols_visitante = partida.gols_visitante

        dados[equipe_mandante.id]['gols_pro'] += gols_mandante
        dados[equipe_visitante.id]['gols_contra'] += gols_mandante
        dados[equipe_visitante.id]['gols_pro'] += gols_visitante
        dados[equipe_mandante.id]['gols_contra'] += gols_visitante

        if gols_mandante > gols_visitante:
            dados[equipe_mandante.id]['pontos'] += 3
            dados[equipe_mandante.id]['vitorias'] += 1
            dados[equipe_visitante.id]['derrotas'] += 1
        elif gols_mandante < gols_visitante:
            dados[equipe_visitante.id]['pontos'] += 3
            dados[equipe_visitante.id]['vitorias'] += 1
            dados[equipe_mandante.id]['derrotas'] += 1
        else:
            dados[equipe_mandante.id]['pontos'] += 1
            dados[equipe_visitante.id]['pontos'] += 1
            dados[equipe_mandante.id]['empates'] += 1
            dados[equipe_visitante.id]['empates'] += 1

    for dado in dados.values():
        Classificacao.objects.create(
            campeonato=campeonato,
            equipe=dado['equipe'],
            pontos=dado['pontos'],
            vitorias=dado['vitorias'],
            empates=dado['empates'],
            derrotas=dado['derrotas'],
            gols_pro=dado['gols_pro'],
            gols_contra=dado['gols_contra'],
            saldo_gols=dado['gols_pro'] - dado['gols_contra']
        )
