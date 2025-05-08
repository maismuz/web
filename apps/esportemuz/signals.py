from esportemuz.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Partida)
def atualizar_classificacao(sender, instance, created, **kwargs):
    # Só atualiza se a partida estiver finalizada
    if instance.status.nome != 'finalizada':
        return

    campeonato = instance.campeonato
    mandante = instance.equipe_mandante
    visitante = instance.equipe_visitante
    gols_mandante = instance.gols_mandante
    gols_visitante = instance.gols_visitante

    def atualizar_para(equipe, gols_feitos, gols_sofridos, venceu=False, empatou=False):
        classificacao, _ = Classificacao.objects.get_or_create(
            campeonato=campeonato,
            equipe=equipe,
        )
        classificacao.gols_pro += gols_feitos
        classificacao.gols_contra += gols_sofridos
        classificacao.saldo_gols = classificacao.gols_pro - classificacao.gols_contra

        if venceu:
            classificacao.vitorias += 1
            classificacao.pontos += 3
            classificacao.empates = 0
        elif empatou:
            classificacao.empates += 1
            classificacao.pontos += 1
        else:
            classificacao.derrotas += 1

        classificacao.save()

    if gols_mandante > gols_visitante:
        atualizar_para(mandante, gols_mandante, gols_visitante, venceu=True)
        atualizar_para(visitante, gols_visitante, gols_mandante)
    elif gols_visitante > gols_mandante:
        atualizar_para(visitante, gols_visitante, gols_mandante, venceu=True)
        atualizar_para(mandante, gols_mandante, gols_visitante)
    else:
        atualizar_para(mandante, gols_mandante, gols_visitante, empatou=True)
        atualizar_para(visitante, gols_visitante, gols_mandante, empatou=True)