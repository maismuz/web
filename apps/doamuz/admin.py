from django.contrib import admin
from .models import (
    Estado, Cidade, Categoria, Doacao, Ongs, 
    Solicitacao, Pessoa, Feedback
)


class CidadeInline(admin.TabularInline):
    """Inline admin for cities."""
    model = Cidade
    extra = 0
    fields = ('nome',)


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    """Admin configuration for Estado model."""
    
    list_display = ('get_nome_completo', 'sigla', 'get_total_cidades')
    search_fields = ('sigla',)
    inlines = [CidadeInline]

    def get_nome_completo(self, obj):
        """Display full state name."""
        return obj.get_sigla_display()
    get_nome_completo.short_description = 'Estado'

    def get_total_cidades(self, obj):
        """Display total number of cities in state."""
        return obj.cidades.count()
    get_total_cidades.short_description = 'Total de Cidades'


@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    """Admin configuration for Cidade model."""
    
    list_display = ('nome', 'estado', 'get_total_ongs')
    list_filter = ('estado',)
    search_fields = ('nome', 'estado__sigla')

    def get_total_ongs(self, obj):
        """Display total number of NGOs in city."""
        return obj.ongs.count()
    get_total_ongs.short_description = 'Total de ONGs'


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin configuration for Categoria model."""
    
    list_display = ('nome', 'ativa', 'get_total_doacoes', 'get_total_solicitacoes')
    list_filter = ('ativa',)
    search_fields = ('nome', 'descricao')
    fieldsets = (
        ('Informações da Categoria', {
            'fields': ('nome', 'descricao', 'ativa')
        }),
    )

    def get_total_doacoes(self, obj):
        """Display total number of donations in category."""
        return obj.doacoes.count()
    get_total_doacoes.short_description = 'Total de Doações'

    def get_total_solicitacoes(self, obj):
        """Display total number of requests in category."""
        return obj.solicitacoes.count()
    get_total_solicitacoes.short_description = 'Total de Solicitações'


@admin.register(Doacao)
class DoacaoAdmin(admin.ModelAdmin):
    """Admin configuration for Doacao model."""
    
    list_display = ('titulo', 'categoria', 'status', 'quantidade_necessaria', 'data_limite', 'data_criacao')
    list_filter = ('status', 'categoria', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'contato')
    date_hierarchy = 'data_criacao'
    fieldsets = (
        ('Informações da Doação', {
            'fields': ('titulo', 'descricao', 'categoria')
        }),
        ('Detalhes', {
            'fields': ('quantidade_necessaria', 'data_limite', 'status')
        }),
        ('Contato', {
            'fields': ('contato',)
        }),
    )


@admin.register(Ongs)
class OngsAdmin(admin.ModelAdmin):
    """Admin configuration for Ongs model."""
    
    list_display = ('nome_organizacao', 'cidade', 'categoria', 'contato', 'ativa')
    list_filter = ('ativa', 'categoria', 'cidade__estado')
    search_fields = ('nome_organizacao', 'descricao', 'cnpj', 'contato')
    fieldsets = (
        ('Informações da Organização', {
            'fields': ('nome_organizacao', 'descricao', 'categoria', 'ativa')
        }),
        ('Localização', {
            'fields': ('cidade', 'endereco')
        }),
        ('Contato', {
            'fields': ('contato', 'email', 'horario_funcionamento')
        }),
        ('Documentação', {
            'fields': ('cnpj',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('cidade', 'categoria')


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    """Admin configuration for Solicitacao model."""
    
    list_display = ('titulo', 'nome_solicitante', 'tipo_solicitante', 'categoria', 'atendida', 'prazo', 'data_criacao')
    list_filter = ('atendida', 'tipo_solicitante', 'categoria', 'data_criacao')
    search_fields = ('titulo', 'nome_solicitante', 'descricao', 'contato')
    date_hierarchy = 'data_criacao'
    fieldsets = (
        ('Informações da Solicitação', {
            'fields': ('titulo', 'descricao', 'categoria', 'imagem')
        }),
        ('Solicitante', {
            'fields': ('tipo_solicitante', 'nome_solicitante', 'contato')
        }),
        ('Prazos e Status', {
            'fields': ('prazo', 'atendida')
        }),
    )


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    """Admin configuration for Pessoa model."""
    
    list_display = ('get_nome_display', 'categoria', 'titulo', 'prazo', 'data_cadastro')
    list_filter = ('mostrar_nome', 'categoria', 'data_cadastro')
    search_fields = ('nome', 'titulo', 'descricao', 'contato')
    date_hierarchy = 'data_cadastro'
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'mostrar_nome', 'categoria')
        }),
        ('Solicitação/Oferta', {
            'fields': ('titulo', 'descricao', 'prazo', 'imagem')
        }),
        ('Contato', {
            'fields': ('contato',)
        }),
    )

    def get_nome_display(self, obj):
        """Display name or anonymous."""
        return str(obj)
    get_nome_display.short_description = 'Nome'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Admin configuration for Feedback model."""
    
    list_display = ('categoria', 'avaliacao', 'get_avaliacao_display', 'data_comentario', 'email_contato')
    list_filter = ('avaliacao', 'categoria', 'data_comentario')
    search_fields = ('mensagem', 'categoria__nome', 'email_contato')
    date_hierarchy = 'data_comentario'
    fieldsets = (
        ('Avaliação', {
            'fields': ('categoria', 'avaliacao')
        }),
        ('Comentário', {
            'fields': ('mensagem',)
        }),
        ('Contato', {
            'fields': ('email_contato',)
        }),
    )

    def get_avaliacao_display(self, obj):
        """Display rating with stars."""
        return f"{'★' * obj.avaliacao}{'☆' * (5 - obj.avaliacao)}"
    get_avaliacao_display.short_description = 'Estrelas'