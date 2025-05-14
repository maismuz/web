from django.contrib import admin
from .models import *

# Register your models here.

class ServicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'categoria', 'criado_em')
    list_filter = ('categoria',)
    search_fields = ('titulo', 'descricao', 'categoria', 'usuario__nome')

class VagaEmpregoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'salario', 'localizacao', 'categoria', 'ativa', 'criado_em')
    list_filter = ('ativa', 'categoria', 'localizacao')
    search_fields = ('titulo', 'descricao', 'usuario__nome')

class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ('candidato', 'vaga', 'data_candidatura')
    search_fields = ('candidato__nome', 'vaga__titulo')

class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('serviço', 'avaliador', 'nota', 'criado_em')
    list_filter = ('nota',)
    search_fields = ('serviço__titulo', 'avaliador__nome')



admin.site.register(Servico)
admin.site.register(VagaEmprego)
admin.site.register(Candidatura) 
admin.site.register(Avaliacao)