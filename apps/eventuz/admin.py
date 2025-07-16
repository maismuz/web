from django.contrib import admin
from django.utils.html import format_html
from .models import *

class MidiaInline(admin.TabularInline):
    model = Midia
    extra = 1

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    inlines = [MidiaInline]
    list_display = ['nome', 'data', 'local', 'categoria', 'resumo_descricao', 'link_rede_social_clickavel', 'aprovado']
    list_display_links = ['nome']
    list_filter = ['categoria']
    # Removido list_editable para que aprovação seja feita na visualização
    fields = ['nome', 'data', 'local', 'descricao', 'contato', 'categoria', 'rede_social', 'aprovado']

    def resumo_descricao(self, obj):
        return format_html(f"<div style='max-width: 300px; white-space: normal;'>{obj.descricao[:100]}...</div>")
    resumo_descricao.short_description = "Descrição"

    def link_rede_social_clickavel(self, obj):
        link = obj.link_rede_social()
        if link:
            return format_html(f"<a href='{link}' target='_blank'>{link}</a>")
        return "-"
    link_rede_social_clickavel.short_description = "Rede Social"

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
