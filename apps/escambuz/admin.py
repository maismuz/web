from django.contrib import admin
from .models import *


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']

admin.site.register(Categoria, CategoriaAdmin)

class ObjetoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'preco', 'categoria', 'usuario', 'estado', 'data_cadastro']
    search_fields = ['nome', 'descricao', 'usuario__username']
    list_filter = ['tipo', 'categoria', 'estado']

admin.site.register(Objeto, ObjetoAdmin)

class HistoricoTransacaoAdmin(admin.ModelAdmin):
    list_display = ['objeto_oferecido', 'objeto_recebido', 'usuario', 'data', 'status']
    search_fields = ['usuario__username']
    list_filter = ['data', 'status']

admin.site.register(HistoricoTransacao, HistoricoTransacaoAdmin)


