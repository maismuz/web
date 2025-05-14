from django.contrib import admin
from .models import Motorista, Local, Viagem

from .models import Combustivel, TipoVeiculo, Veiculo
from django.utils.safestring import mark_safe

@admin.register(Combustivel)
class CombustivelAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    ordering = ('nome',)


@admin.register(TipoVeiculo)
class TipoVeiculoAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'placa', 'cor', 'ano_fabricacao', 'tipo', 'combustivel', 'foto_preview')
    list_filter = ('tipo', 'combustivel', 'cor', 'ano_fabricacao')
    search_fields = ('modelo', 'placa')
    readonly_fields = ('foto_preview',)
    ordering = ('modelo',)

    fieldsets = (
        (None, {
            'fields': ('modelo', 'placa', 'cor', 'ano_fabricacao', 'tipo', 'combustivel')
        }),
        ('Foto do Veículo', {
            'fields': ('foto', 'foto_preview'),
        }),
    )

    def foto_preview(self, obj):
        if obj.foto:
            return mark_safe(f'<img src="{obj.foto.url}" width="128" height="128" />')
        return "Sem imagem"
    
    foto_preview.allow_tags = True
    foto_preview.short_description = "Prévia da Foto"
   
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
