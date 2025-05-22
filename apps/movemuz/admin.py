from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Combustivel, TipoVeiculo, Veiculo, Local,
    Viagem, Passageiro, Motorista, HorarioTransporte
)

@admin.register(Combustivel)
class CombustivelAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    ordering = ('nome',)


@admin.register(TipoVeiculo)
class TipoVeiculoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    ordering = ('nome',)


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'placa', 'tipo', 'capacidade', 'condicao_manutencao', 'ano_fabricacao', 'foto_preview')
    list_filter = ('tipo', 'combustivel', 'condicao_manutencao', 'ano_fabricacao')
    search_fields = ('modelo', 'placa')
    readonly_fields = ('foto_preview',)
    ordering = ('modelo',)

    fieldsets = (
        (None, {
            'fields': ('modelo', 'placa', 'cor', 'ano_fabricacao', 'tipo', 'combustivel', 'capacidade', 'condicao_manutencao')
        }),
        ('Foto do veículo', {
            'fields': ('foto', 'foto_preview'),
        }),
    )

    def foto_preview(self, obj):
        if obj.foto:
            return mark_safe(f'<img src="{obj.foto.url}" width="128" height="128" />')
        return "Sem imagem"

    foto_preview.short_description = "Prévia da foto"


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'estado')
    search_fields = ('nome', 'cidade', 'estado')
    ordering = ('nome',)


@admin.register(Viagem)
class ViagemAdmin(admin.ModelAdmin):
    list_display = ('motorista', 'origem', 'destino', 'data_saida', 'data_chegada')
    search_fields = ('origem__nome', 'destino__nome', 'motorista__nome')
    list_filter = ('data_chegada', 'data_saida')
    ordering = ('-data_saida',)
    list_per_page = 20


@admin.register(Passageiro)
class PassageiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'documento', 'viagem')
    search_fields = ('nome', 'documento', 'viagem__origem__nome', 'viagem__destino__nome')
    list_filter = ('viagem',)
    ordering = ('nome',)


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'cnh_numero', 'ativo')
    search_fields = ('nome', 'cpf', 'cnh_numero')
    list_filter = ('ativo',)
    ordering = ('nome',)


@admin.register(HorarioTransporte)
class HorarioTransporteAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'origem', 'destino', 'horario_partida', 'dias_semana')
    search_fields = ('origem__nome', 'destino__nome', 'dias_semana')
    list_filter = ('dias_semana',)
