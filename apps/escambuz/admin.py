from django.contrib import admin
from .models import *


@admin.register(Categoria1)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'preco', 'usuario', 'estado', 'data_transacao']
    list_filter = ['tipo', 'categoria', 'estado', 'data_transacao']
    search_fields = ['nome', 'descricao', 'usuario__username']
    autocomplete_fields = ['categoria', 'usuario']
    ordering = ['-data_transacao']
