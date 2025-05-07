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
    list_display = ['id', 'nome', 'modalidade', 'tipo_campeonato', 'data_inicio', 'data_fim']
    list_per_page = 10
    search_fields = ['nome']
    list_filter = ['modalidade', 'tipo_campeonato']

class EquipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_per_page = 10
    search_fields = ['nome']

class GrupoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'campeonato']
    list_per_page = 10
    search_fields = ['nome']
    list_filter = ['campeonato']

class StatusPartidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_per_page = 10
    search_fields = ['nome']

class PartidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'campeonato', 'equipe1', 'equipe2', 'data_hora', 'status']
    list_per_page = 10
    search_fields = ['campeonato__nome', 'equipe1__nome', 'equipe2__nome']
    list_filter = ['campeonato', 'status']

class ClassificacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'campeonato', 'equipe', 'pontos', 'vitorias', 'empates', 'derrotas', 'gols_pro', 'gols_contra']
    list_per_page = 10
    search_fields = ['campeonato__nome', 'equipe__nome']
    list_filter = ['campeonato']