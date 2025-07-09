from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import *
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.conf import settings
# Register your models here.

class CategoriaResource(resources.ModelResource):
    class Meta:
        model = Categoria
        fields = ('id', 'nome', 'descricao')
        export_order = ('id', 'nome', 'descricao')

class CategoriaAdmin(ImportExportModelAdmin):
    resource_class = CategoriaResource
    list_display = ('id', 'nome', 'descricao')
    search_fields = ('nome',)
    list_filter = ('nome',)
    ordering = ('id',)
    list_per_page = 10
    list_display_links = ('id', 'nome')
    list_editable = ('descricao',)
    list_select_related = ('nome',)
    list_filter = ('nome',)
    list_display_links = ('id', 'nome')

class ItemAcervoResource(resources.ModelResource):
    class Meta:
        model = ItemAcervo
        fields = ('id', 'nome', 'categoria', 'descricao', 'origem', 'data_adicao', 'usuario_adicionado')
        export_order = ('id', 'nome', 'categoria', 'descricao', 'origem', 'data_adicao', 'usuario_adicionado')

class ItemAcervoAdmin(ImportExportModelAdmin):
    resource_class = ItemAcervoResource
    list_display = ('id', 'nome', 'categoria', 'descricao', 'origem', 'data_adicao', 'usuario_adicionado')
    search_fields = ('nome',)
    list_filter = ('categoria',)
    ordering = ('id',)
    list_per_page = 10
    list_display_links = ('id', 'nome')
    list_editable = ('descricao', 'origem')
    list_select_related = ('categoria',)
    list_filter = ('categoria',)
    list_display_links = ('id', 'nome')

class ImagemItemAcervoResource(resources.ModelResource):
    class Meta:
        model = ImagemItemAcervo
        fields = ('id', 'item_acervo', 'imagem')
        export_order = ('id', 'item_acervo', 'imagem')

class ImagemItemAcervoAdmin(ImportExportModelAdmin):
    resource_class = ImagemItemAcervoResource
    list_display = ('id', 'item_acervo', 'imagem')
    search_fields = ('item_acervo__nome',)
    list_filter = ('item_acervo',)
    ordering = ('id',)
    list_per_page = 10
    list_display_links = ('id', 'item_acervo')
    list_editable = ('imagem',)
    list_select_related = ('item_acervo',)
    list_filter = ('item_acervo',)
    list_display_links = ('id', 'item_acervo')

class PatrimonioResource(resources.ModelResource):
    class Meta:
        model = Patrimonio
        fields = ('id', 'nome', 'descricao', 'data_origem', 'localizacao', 'data_adicao', 'usuario_adicionado')
        export_order = ('id', 'nome', 'descricao', 'data_origem', 'localizacao', 'data_adicao', 'usuario_adicionado')

class ImagemPatrimonioInline(admin.TabularInline):
    model = ImagemPatrimonio
    extra = 1
    fields = ('imagem', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.imagem.url)
        return ""

    preview.short_description = "Pré-visualização"

class PatrimonioAdmin(ImportExportModelAdmin):
    resource_class = PatrimonioResource
    list_display = ('id', 'nome', 'descricao', 'data_origem', 'localizacao', 'data_adicao', 'usuario_adicionado')
    search_fields = ('nome',)
    list_filter = ('localizacao',)
    ordering = ('id',)
    list_per_page = 10
    list_display_links = ('id', 'nome')
    list_editable = ('descricao', 'data_origem')
    list_filter = ('localizacao',)
    list_display_links = ('id', 'nome')
    inlines = [ImagemPatrimonioInline] 

class ImagemPatrimonioResource(resources.ModelResource):
    class Meta:
        model = ImagemPatrimonio
        fields = ('id', 'patrimonio', 'imagem')
        export_order = ('id', 'patrimonio', 'imagem')

class ImagemPatrimonioAdmin(ImportExportModelAdmin):
    resource_class = ImagemPatrimonioResource
    list_display = ('id', 'patrimonio', 'imagem')
    search_fields = ('patrimonio__nome',)
    list_filter = ('patrimonio',)
    ordering = ('id',)
    list_per_page = 10
    list_display_links = ('id', 'patrimonio')
    list_editable = ('imagem',)
    list_select_related = ('patrimonio',)
    list_filter = ('patrimonio',)
    list_display_links = ('id', 'patrimonio')

class DocumentoHistoricoResource(resources.ModelResource):
    class Meta:
        model = DocumentoHistorico
        fields = ('id', 'titulo', 'descricao', 'data_origem', 'data_adicao', 'usuario_adicionado')
        export_order = ('id', 'titulo', 'descricao', 'data_origem', 'data_adicao', 'usuario_adicionado')

class DocumentoHistoricoAdmin(ImportExportModelAdmin):
    resource_class = DocumentoHistoricoResource
    list_display = ('id', 'titulo', 'descricao', 'data_origem', 'data_adicao', 'usuario_adicionado')
    search_fields = ('titulo',)
    list_filter = ('data_origem',)
    ordering = ('id',)
    list_per_page = 10
    list_display_links = ('id', 'titulo')
    list_editable = ('descricao', 'data_origem')
    list_select_related = ('data_origem',)
    list_filter = ('data_origem',)
    list_display_links = ('id', 'titulo')

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(ItemAcervo, ItemAcervoAdmin)
admin.site.register(ImagemItemAcervo, ImagemItemAcervoAdmin)
admin.site.register(Patrimonio, PatrimonioAdmin)
admin.site.register(ImagemPatrimonio, ImagemPatrimonioAdmin)
admin.site.register(DocumentoHistorico, DocumentoHistoricoAdmin)
