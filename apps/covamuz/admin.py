from django.contrib import admin
from .models import (
    Cemiterio, AreaCemiterio, Tumulo, HorarioVisitacao,
    HoraDiaVisitacao, Pessoa
)


class AreaCemiterioInline(admin.TabularInline):
    """Inline admin for cemetery areas."""
    model = AreaCemiterio
    extra = 0
    fields = ('nome', 'descricao')


class HorarioVisitacaoInline(admin.TabularInline):
    """Inline admin for visitation schedules."""
    model = HorarioVisitacao
    extra = 0
    fields = ('nome', 'ativo')


@admin.register(Cemiterio)
class CemiterioAdmin(admin.ModelAdmin):
    """Admin configuration for Cemiterio model."""
    
    list_display = ('nome', 'cidade', 'telefone', 'data_cadastro')
    list_filter = ('cidade', 'data_cadastro')
    search_fields = ('nome', 'cidade', 'endereco')
    date_hierarchy = 'data_cadastro'
    inlines = [AreaCemiterioInline, HorarioVisitacaoInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'cidade')
        }),
        ('Contato e Localização', {
            'fields': ('endereco', 'telefone')
        }),
    )


class TumuloInline(admin.TabularInline):
    """Inline admin for tombs."""
    model = Tumulo
    extra = 0
    fields = ('numero', 'tipo', 'ocupado')


@admin.register(AreaCemiterio)
class AreaCemiterioAdmin(admin.ModelAdmin):
    """Admin configuration for AreaCemiterio model."""
    
    list_display = ('nome', 'cemiterio', 'get_total_tumulos')
    list_filter = ('cemiterio',)
    search_fields = ('nome', 'cemiterio__nome', 'descricao')
    inlines = [TumuloInline]
    fieldsets = (
        ('Informações da Área', {
            'fields': ('nome', 'cemiterio', 'descricao')
        }),
    )

    def get_total_tumulos(self, obj):
        """Display total number of tombs in area."""
        return obj.tumulos.count()
    get_total_tumulos.short_description = 'Total de Túmulos'


@admin.register(Tumulo)
class TumuloAdmin(admin.ModelAdmin):
    """Admin configuration for Tumulo model."""
    
    list_display = ('numero', 'area', 'get_cemiterio', 'tipo', 'ocupado', 'get_total_pessoas')
    list_filter = ('area__cemiterio', 'area', 'ocupado', 'tipo')
    search_fields = ('numero', 'area__nome', 'area__cemiterio__nome', 'tipo')
    fieldsets = (
        ('Informações do Túmulo', {
            'fields': ('numero', 'area', 'tipo', 'ocupado')
        }),
    )

    def get_cemiterio(self, obj):
        """Display cemetery name."""
        return obj.area.cemiterio.nome
    get_cemiterio.short_description = 'Cemitério'

    def get_total_pessoas(self, obj):
        """Display total number of people in tomb."""
        return obj.pessoas.count()
    get_total_pessoas.short_description = 'Pessoas Enterradas'


class HoraDiaVisitacaoInline(admin.TabularInline):
    """Inline admin for visiting hours and days."""
    model = HoraDiaVisitacao
    extra = 0
    fields = ('dia', 'hora_inicio', 'hora_fim')


@admin.register(HorarioVisitacao)
class HorarioVisitacaoAdmin(admin.ModelAdmin):
    """Admin configuration for HorarioVisitacao model."""
    
    list_display = ('nome', 'cemiterio', 'ativo', 'get_total_horarios')
    list_filter = ('cemiterio', 'ativo')
    search_fields = ('nome', 'cemiterio__nome')
    inlines = [HoraDiaVisitacaoInline]
    fieldsets = (
        ('Informações do Horário', {
            'fields': ('nome', 'cemiterio', 'ativo')
        }),
    )

    def get_total_horarios(self, obj):
        """Display total number of scheduled hours."""
        return obj.horas_dias.count()
    get_total_horarios.short_description = 'Horários Cadastrados'


@admin.register(HoraDiaVisitacao)
class HoraDiaVisitacaoAdmin(admin.ModelAdmin):
    """Admin configuration for HoraDiaVisitacao model."""
    
    list_display = ('horario_visitacao', 'dia', 'hora_inicio', 'hora_fim', 'get_cemiterio')
    list_filter = ('dia', 'horario_visitacao__cemiterio')
    search_fields = ('horario_visitacao__nome', 'horario_visitacao__cemiterio__nome')
    fieldsets = (
        ('Informações do Horário', {
            'fields': ('horario_visitacao', 'dia', 'hora_inicio', 'hora_fim')
        }),
    )

    def get_cemiterio(self, obj):
        """Display cemetery name."""
        return obj.horario_visitacao.cemiterio.nome
    get_cemiterio.short_description = 'Cemitério'


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    """Admin configuration for Pessoa model."""
    
    list_display = ('nome', 'data_nascimento', 'data_falecimento', 'cemiterio', 'tumulo', 'get_idade_falecimento')
    list_filter = ('cemiterio', 'data_falecimento', 'tumulo__area')
    search_fields = ('nome', 'cemiterio__nome', 'tumulo__numero')
    date_hierarchy = 'data_falecimento'
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'data_nascimento', 'data_falecimento')
        }),
        ('Localização', {
            'fields': ('cemiterio', 'tumulo')
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
    )

    def get_idade_falecimento(self, obj):
        """Display age at death."""
        idade = obj.idade_falecimento
        return f"{idade} anos" if idade is not None else "N/A"
    get_idade_falecimento.short_description = 'Idade no Falecimento'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('cemiterio', 'tumulo', 'tumulo__area')