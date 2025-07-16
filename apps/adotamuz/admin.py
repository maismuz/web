from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import (
    Animal, Raca, Adocao, TipoProcedimento, Procedimento,
    TipoDenuncia, Denuncia, InstituicaoParceira, Evento
)


class AnimalResource(resources.ModelResource):
    """Resource class for Animal import/export."""
    
    class Meta:
        model = Animal
        skip_unchanged = True
        report_skipped = True
        fields = ('nome', 'porte', 'raca', 'cor', 'localizacao', 'foto', 'descricao')


@admin.register(Animal)
class AnimalAdmin(ImportExportModelAdmin):
    """Admin configuration for Animal model."""
    
    resource_class = AnimalResource
    list_display = ('nome', 'porte', 'raca', 'cor', 'localizacao', 'data_cadastro')
    list_filter = ('porte', 'raca', 'cor', 'data_cadastro')
    search_fields = ('nome', 'raca__nome', 'descricao', 'localizacao')
    date_hierarchy = 'data_cadastro'
    fieldsets = (
        ('Informações do Animal', {
            'fields': ('nome', 'foto', 'cor', 'porte', 'raca', 'localizacao', 'descricao')
        }),
    )


@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    """Admin configuration for Raca model."""
    
    list_display = ('nome', 'especie', 'porte', 'data_cadastro')
    list_filter = ('especie', 'porte', 'data_cadastro')
    search_fields = ('nome', 'descricao')
    date_hierarchy = 'data_cadastro'


@admin.register(Adocao)
class AdocaoAdmin(admin.ModelAdmin):
    """Admin configuration for Adocao model."""
    
    list_display = ('nome_animal', 'contato', 'disponivel', 'data_cadastro')
    list_filter = ('disponivel', 'data_cadastro')
    search_fields = ('nome_animal', 'descricao', 'contato')
    date_hierarchy = 'data_cadastro'
    fieldsets = (
        ('Informações do Animal', {
            'fields': ('nome_animal', 'foto', 'descricao')
        }),
        ('Informações de Contato', {
            'fields': ('contato', 'disponivel')
        }),
    )


@admin.register(TipoProcedimento)
class TipoProcedimentoAdmin(admin.ModelAdmin):
    """Admin configuration for TipoProcedimento model."""
    
    list_display = ('nome', 'animal', 'instituicao_responsavel', 'data')
    list_filter = ('data', 'instituicao_responsavel')
    search_fields = ('nome', 'animal__nome', 'instituicao_responsavel__nome')
    date_hierarchy = 'data'
    fieldsets = (
        ('Informações do Procedimento', {
            'fields': ('nome', 'animal', 'instituicao_responsavel', 'data')
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Procedimento)
class ProcedimentoAdmin(admin.ModelAdmin):
    """Admin configuration for Procedimento model."""
    
    list_display = ('get_tipo_nome', 'get_animal_nome', 'get_data')
    list_filter = ('tipo__data', 'tipo__instituicao_responsavel')
    search_fields = ('tipo__nome', 'tipo__animal__nome')
    
    def get_tipo_nome(self, obj):
        return obj.tipo.nome
    get_tipo_nome.short_description = 'Tipo'
    
    def get_animal_nome(self, obj):
        return obj.tipo.animal.nome
    get_animal_nome.short_description = 'Animal'
    
    def get_data(self, obj):
        return obj.tipo.data
    get_data.short_description = 'Data'


@admin.register(TipoDenuncia)
class TipoDenunciaAdmin(admin.ModelAdmin):
    """Admin configuration for TipoDenuncia model."""
    
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    """Admin configuration for Denuncia model."""
    
    list_display = ('tipo', 'data', 'localizacao')
    list_filter = ('tipo', 'data')
    search_fields = ('descricao', 'localizacao', 'tipo__nome')
    date_hierarchy = 'data'
    fieldsets = (
        ('Informações da Denúncia', {
            'fields': ('tipo', 'data', 'localizacao', 'foto')
        }),
        ('Descrição', {
            'fields': ('descricao',)
        }),
    )


@admin.register(InstituicaoParceira)
class InstituicaoParceiraAdmin(admin.ModelAdmin):
    """Admin configuration for InstituicaoParceira model."""
    
    list_display = ('nome', 'cnpj', 'telefone')
    search_fields = ('nome', 'cnpj', 'telefone', 'servicos_ofertados')
    list_filter = ('nome',)
    fieldsets = (
        ('Informações da Instituição', {
            'fields': ('nome', 'cnpj', 'endereco', 'telefone')
        }),
        ('Serviços', {
            'fields': ('servicos_ofertados',)
        }),
    )


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """Admin configuration for Evento model."""
    
    list_display = ('nome', 'data', 'hora', 'local', 'organizador')
    search_fields = ('nome', 'local', 'organizador')
    list_filter = ('data', 'local', 'organizador')
    date_hierarchy = 'data'
    fieldsets = (
        ('Informações do Evento', {
            'fields': ('nome', 'data', 'hora', 'local', 'organizador')
        }),
    )
