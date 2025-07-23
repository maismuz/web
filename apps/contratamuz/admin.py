from django.contrib import admin
from .models import Usuario, Servico, VagaEmprego, Candidatura, Avaliacao


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """Admin configuration for Usuario model."""
    
    list_display = ('nome', 'eh_empresa', 'eh_prestador', 'telefone', 'data_cadastro')
    list_filter = ('eh_empresa', 'eh_prestador', 'data_cadastro')
    search_fields = ('nome', 'telefone', 'biografia')
    date_hierarchy = 'data_cadastro'
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'imagem', 'telefone', 'biografia')
        }),
        ('Tipo de Usuário', {
            'fields': ('eh_empresa', 'eh_prestador')
        }),
    )


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    """Admin configuration for Servico model."""
    
    list_display = ('titulo', 'usuario', 'categoria', 'ativo', 'nota_media', 'criado_em')
    list_filter = ('categoria', 'ativo', 'criado_em')
    search_fields = ('titulo', 'descricao', 'categoria', 'usuario__nome')
    date_hierarchy = 'criado_em'
    fieldsets = (
        ('Informações do Serviço', {
            'fields': ('usuario', 'titulo', 'categoria', 'descricao', 'imagem')
        }),
        ('Contato e Status', {
            'fields': ('contato', 'ativo')
        }),
    )

    def nota_media(self, obj):
        """Display average rating in admin list."""
        nota = obj.nota_media
        return f"{nota}★" if nota else "Sem avaliações"
    nota_media.short_description = 'Nota Média'


@admin.register(VagaEmprego)
class VagaEmpregoAdmin(admin.ModelAdmin):
    """Admin configuration for VagaEmprego model."""
    
    list_display = ('titulo', 'usuario', 'salario', 'localizacao', 'categoria', 'ativa', 'criado_em')
    list_filter = ('ativa', 'categoria', 'localizacao', 'criado_em')
    search_fields = ('titulo', 'descricao', 'usuario__nome', 'localizacao')
    date_hierarchy = 'criado_em'
    fieldsets = (
        ('Informações da Vaga', {
            'fields': ('usuario', 'titulo', 'categoria', 'descricao')
        }),
        ('Detalhes', {
            'fields': ('salario', 'localizacao', 'ativa')
        }),
    )


@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    """Admin configuration for Candidatura model."""
    
    list_display = ('candidato', 'vaga', 'status', 'data_candidatura')
    list_filter = ('status', 'data_candidatura')
    search_fields = ('candidato__nome', 'vaga__titulo', 'mensagem')
    date_hierarchy = 'data_candidatura'
    fieldsets = (
        ('Candidatura', {
            'fields': ('candidato', 'vaga', 'status')
        }),
        ('Mensagem', {
            'fields': ('mensagem',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    """Admin configuration for Avaliacao model."""
    
    list_display = ('servico', 'avaliador', 'nota', 'criado_em')
    list_filter = ('nota', 'criado_em')
    search_fields = ('servico__titulo', 'avaliador__nome', 'comentario')
    date_hierarchy = 'criado_em'
    fieldsets = (
        ('Avaliação', {
            'fields': ('servico', 'avaliador', 'nota')
        }),
        ('Comentário', {
            'fields': ('comentario',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('servico', 'avaliador')