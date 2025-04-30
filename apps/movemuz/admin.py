from django.contrib import admin
from .models import Motorista, Local, Viagem

@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'email', 'cnh_numero', 'data_nascimento', 'ativo')
    search_fields = ('nome', 'cpf', 'cnh_numero')
    list_filter = ('ativo', 'cnh_numero')
    ordering = ('nome',)
    list_per_page = 20

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'estado')
    search_fields = ('nome', 'cidade', 'estado')
    ordering = ('nome',)

@admin.register(Viagem)
class ViagemAdmin(admin.ModelAdmin):
    list_display = ('motorista', 'origem', 'destino', 'data_saida', 'data_chegada')
    search_fields = ('origem', 'destino', 'motorista__nome')
    list_filter = ('data_chegada', 'data_saida')
    ordering = ('-data_saida',)
    list_per_page = 20
