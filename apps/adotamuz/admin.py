from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Animal, Raca, Adocao, TipoProcedimento, Procedimento, TipoDenuncia, Denuncia, InstituicaoParceira, Especie

class AnimalResource(resources.ModelResource):
    class Meta:
        model = Animal
        skip_unchanged = True
        report_skipped = True
        fields = ('nome', 'porte', 'raca', 'cor', 'localizacao', 'foto', 'descricao')

@admin.register(Animal)
class AnimalAdmin(ImportExportModelAdmin):
    resource_class = AnimalResource
    list_display = ('nome', 'porte', 'cor', 'localizacao')
    list_filter = ('porte', 'cor', 'localizacao')
    search_fields = ('nome', 'raca', 'descricao', 'localizacao') 
    fieldsets = (
        ('Informações do Animal', {
            'fields': ('nome', 'foto', 'cor', 'porte', 'raca', 'localizacao', 'descricao')
        }),
    )

@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'porte', 'data_cadastro')
    list_filter = ('especie', 'porte')
    search_fields = ('nome',)

@admin.register(Adocao)
class AdocaoAdmin(admin.ModelAdmin):
    list_display = ('nome_animal', 'contato', 'disponivel', 'data_cadastro')
    list_filter = ('disponivel',)
    search_fields = ('nome_animal', 'descricao')

@admin.register(TipoProcedimento)
class TipoProcedimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'animal', 'instituicao_responsavel', 'data')
    list_filter = ('data', 'instituicao_responsavel')
    search_fields = ('nome', 'animal__nome', 'instituicao_responsavel')

@admin.register(Procedimento)
class ProcedimentoAdmin(admin.ModelAdmin):
    list_display = ('tipo',)
    search_fields = ('tipo__nome',)

@admin.register(TipoDenuncia)
class TipoDenunciaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'data', 'localizacao')
    list_filter = ('tipo', 'data')
    search_fields = ('descricao', 'localizacao')


@admin.register(InstituicaoParceira)
class InstituicaoParceiraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'telefone')
    search_fields = ('nome', 'cnpj', 'telefone', 'servicos_ofertados')
    list_filter = ('nome',)
    fieldsets = (
        ('Informações da Instituição', {
            'fields': ('nome', 'cnpj', 'endereco', 'telefone', 'servicos_ofertados')
        }),
    )

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)