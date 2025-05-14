from django.contrib import admin
from esportemuz.models import *

# Register your models here.
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_per_page = 10

class TipoCampeonatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_per_page = 10

class CampeonatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'modalidade', 'tipo_campeonato', 'data_inicio', 'data_fim','equipes']
    list_per_page = 10
    search_fields = ['nome']
    list_filter = ['modalidade', 'tipo_campeonato']

class EquipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome','escudo']
    list_per_page = 10
    search_fields = ['nome']

class LocalPartidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_per_page = 10
    search_fields = ['nome']

class PartidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'campeonato', 'equipe_mandante', 'equipe_visitante', 'data_hora', 'status', 'gols_mandante', 'gols_visitante', 'local','encerrada']
    list_per_page = 10
    search_fields = ['campeonato__nome', 'equipe_mandante__nome', 'equipe_visitante__nome']
    list_filter = ['campeonato', 'status', 'local']

class ClassificacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'campeonato', 'equipe', 'pontos', 'vitorias', 'empates', 'derrotas', 'gols_pro', 'gols_contra','saldo_gols']
    list_per_page = 10
    search_fields = ['campeonato__nome', 'equipe__nome']
    list_filter = ['campeonato']