from esportemuz.models import *

# Create your functions here.
def atualizar_classificacao(campeonato, equipe, gols_pro, gols_contra, resultado_antigo=None):
    classificacao, _ = Classificacao.objects.get_or_create(
        campeonato=campeonato, equipe=equipe,
        defaults={'pontos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0, 'gols_pro': 0, 'gols_contra': 0}
    )

    if resultado_antigo:
        classificacao.pontos -= resultado_antigo['pontos']
        classificacao.vitorias -= resultado_antigo['vitorias']
        classificacao.empates -= resultado_antigo['empates']
        classificacao.derrotas -= resultado_antigo['derrotas']
        classificacao.gols_pro -= resultado_antigo['gols_pro']
        classificacao.gols_contra -= resultado_antigo['gols_contra']

    classificacao.gols_pro += gols_pro
    classificacao.gols_contra += gols_contra

    if gols_pro > gols_contra:
        classificacao.vitorias += 1
        classificacao.pontos += 3
    elif gols_pro == gols_contra:
        classificacao.empates += 1
        classificacao.pontos += 1
    else:
        classificacao.derrotas += 1

    classificacao.save()