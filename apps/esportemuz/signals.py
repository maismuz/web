from .models import *
from .utils import atualizar_classificacao
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create your signals here.
@receiver(pre_save, sender=Partida)
def salvar_resultado_antigo(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        partida_antiga = Partida.objects.get(pk=instance.pk)
        instance._old_resultados = {
            'mandante': {
                'pontos': 3 if partida_antiga.gols_mandante > partida_antiga.gols_visitante else (1 if partida_antiga.gols_mandante == partida_antiga.gols_visitante else 0),
                'vitorias': 1 if partida_antiga.gols_mandante > partida_antiga.gols_visitante else 0,
                'empates': 1 if partida_antiga.gols_mandante == partida_antiga.gols_visitante else 0,
                'derrotas': 1 if partida_antiga.gols_mandante < partida_antiga.gols_visitante else 0,
                'gols_pro': partida_antiga.gols_mandante,
                'gols_contra': partida_antiga.gols_visitante,
            },
            'visitante': {
                'pontos': 3 if partida_antiga.gols_visitante > partida_antiga.gols_mandante else (1 if partida_antiga.gols_visitante == partida_antiga.gols_mandante else 0),
                'vitorias': 1 if partida_antiga.gols_visitante > partida_antiga.gols_mandante else 0,
                'empates': 1 if partida_antiga.gols_visitante == partida_antiga.gols_mandante else 0,
                'derrotas': 1 if partida_antiga.gols_visitante < partida_antiga.gols_mandante else 0,
                'gols_pro': partida_antiga.gols_visitante,
                'gols_contra': partida_antiga.gols_mandante,
            }
        }
    except Partida.DoesNotExist:
        instance._old_resultados = None


@receiver(post_save, sender=Partida)
def atualizar_classificacoes_partida(sender, instance, created, **kwargs):
    if not instance.campeonato or not instance.equipe_mandante or not instance.equipe_visitante:
        return

    resultado_antigo_mandante = resultado_antigo_visitante = None
    if not created and hasattr(instance, '_old_resultados'):
        resultado_antigo_mandante = instance._old_resultados['mandante']
        resultado_antigo_visitante = instance._old_resultados['visitante']

    atualizar_classificacao(
        instance.campeonato,
        instance.equipe_mandante,
        instance.gols_mandante,
        instance.gols_visitante,
        resultado_antigo=resultado_antigo_mandante
    )

    atualizar_classificacao(
        instance.campeonato,
        instance.equipe_visitante,
        instance.gols_visitante,
        instance.gols_mandante,
        resultado_antigo=resultado_antigo_visitante
    )
