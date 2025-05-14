from django.contrib import admin
from apps.esportemuz.models import *

# Register your models here.
@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_per_page = 10

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'escudo']
    list_per_page = 10

@admin.register(TipoCampeonato)
class TipoCampeonatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_per_page = 10

@admin.register(Campeonato)
class CampeonatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'modalidade', 'tipo_campeonato', 'data_inicio', 'data_fim']
    list_per_page = 10

@admin.register(LocalPartida)
class LocalPartidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_per_page = 10

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'campeonato', 'equipe_mandante', 'equipe_visitante', 'data_hora', 'gols_mandante', 'gols_visitante', 'local', 'encerrada']
    list_per_page = 10
    search_fields = ['campeonato__nome', 'equipe_mandante__nome', 'equipe_visitante__nome']
    list_filter = ['campeonato', 'local']

@admin.register(Classificacao)
class ClassificacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'campeonato', 'equipe', 'pontos', 'vitorias', 'empates', 'derrotas', 'gols_pro', 'gols_contra','saldo_gols']
    list_per_page = 10