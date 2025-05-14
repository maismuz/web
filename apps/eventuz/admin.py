from django.contrib import admin
from django.utils.html import format_html
from .models import *

class MidiaInline(admin.TabularInline):
    model = Midia
    extra = 1

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    inlines = [MidiaInline]
    list_display = ['nome', 'data', 'local', 'categoria', 'resumo_descricao', 'aprovado']
    list_display_links = ['nome']
    list_filter = ['categoria']
    list_editable = ['aprovado']
    fields = ['nome', 'data', 'local', 'descricao', 'contato', 'categoria', ]

    def resumo_descricao(self, obj):
        return format_html(f"<div style='max-width: 300px; white-space: normal;'>{obj.descricao[:100]}...</div>")
    resumo_descricao.short_description = "Descrição"

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
