from django.contrib import admin
from .models import Mensagem

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
