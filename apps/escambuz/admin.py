from django.contrib import admin
from .models import Usuario, Mensagem


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    ordering = ('nome',)


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'remetente', 'destinatario', 'data', 'status')
    list_filter = ('status', 'data')
    search_fields = ('remetente__nome', 'destinatario__nome', 'mensagem')
    ordering = ('-data',)
    date_hierarchy = 'data'
