from django.contrib import admin
from .models import (Categoria, Objeto)
# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']

admin.site.register(Categoria, CategoriaAdmin)

class ObjetoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'preco', 'categoria', 'usuario', 'estado', 'data_cadastro']
    search_fields = ['nome', 'descricao', 'usuario__username']
    list_filter = ['tipo', 'categoria', 'estado']

admin.site.register(Objeto, ObjetoAdmin)