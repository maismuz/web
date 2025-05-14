from django.contrib import admin
from .models import *

@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'remetente', 'destinatario', 'mensagem_resumida', 'data_envio', 'status')
    list_filter = ('status', 'data_envio')
    search_fields = ('remetente__username', 'destinatario__username', 'mensagem')
    ordering = ('-data_envio',)
    date_hierarchy = 'data_envio'

    def mensagem_resumida(self, obj):
        return (obj.mensagem[:40] + '...') if len(obj.mensagem) > 40 else obj.mensagem
    mensagem_resumida.short_description = 'Mensagem'

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'preco', 'data_criacao']
    search_fields = ['titulo']
    list_filter = ['data_criacao']

@admin.register(DenunciaIrregular)
class DenunciaIrregularAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'oferta', 'motivo_da_denuncia', 'status', 'data_denuncia']
    list_filter = ['status', 'motivo_da_denuncia', 'data_denuncia']
    search_fields = ['usuario__username', 'oferta__titulo']
    autocomplete_fields = ['usuario', 'oferta']
    ordering = ['-data_denuncia']
