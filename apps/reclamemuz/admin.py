from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import (
    Categoria, Denuncia, Comentario, Midia, 
    Notificacao, BuscaDenuncia
)


# Resources for import/export
class DenunciaResource(resources.ModelResource):
    """Resource class for Denuncia import/export."""
    
    class Meta:
        model = Denuncia
        fields = (
            'id', 'titulo', 'tipo', 'categoria', 'prioridade',
            'descricao', 'data_ocorrencia', 'logradouro_ocorrencia', 
            'bairro_ocorrencia', 'status', 'data_criacao'
        )
        export_order = fields


# Inline admins
class ComentarioInline(admin.TabularInline):
    """Inline admin for comments."""
    model = Comentario
    extra = 0
    fields = ('usuario', 'texto', 'eh_publico', 'data_hora')
    readonly_fields = ('data_hora',)
    ordering = ['-data_hora']


class MidiaInline(admin.TabularInline):
    """Inline admin for media files."""
    model = Midia
    extra = 0
    fields = ('tipo', 'arquivo', 'url_arquivo', 'descricao')


class NotificacaoInline(admin.TabularInline):
    """Inline admin for notifications."""
    model = Notificacao
    extra = 0
    fields = ('tipo', 'mensagem', 'lida', 'data_hora')
    readonly_fields = ('data_hora',)


# Admin configurations
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin configuration for Categoria model."""
    
    list_display = ('nome', 'ativa', 'get_total_denuncias')
    list_filter = ('ativa',)
    search_fields = ('nome', 'descricao')
    fieldsets = (
        ('Informações da Categoria', {
            'fields': ('nome', 'descricao', 'ativa')
        }),
    )

    def get_total_denuncias(self, obj):
        """Display total number of complaints in category."""
        return obj.denuncias.count()
    get_total_denuncias.short_description = 'Total de Denúncias'


@admin.register(Denuncia)
class DenunciaAdmin(ImportExportModelAdmin):
    """Admin configuration for Denuncia model."""
    
    resource_class = DenunciaResource
    list_display = (
        'titulo', 'tipo', 'prioridade', 'status', 'bairro_ocorrencia',
        'get_dias_pendente', 'data_ocorrencia', 'data_criacao'
    )
    list_filter = ('status', 'tipo', 'prioridade', 'categoria', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'bairro_ocorrencia', 'logradouro_ocorrencia')
    date_hierarchy = 'data_criacao'
    inlines = [ComentarioInline, MidiaInline, NotificacaoInline]
    fieldsets = (
        ('Informações da Denúncia', {
            'fields': ('titulo', 'tipo', 'categoria', 'prioridade', 'descricao')
        }),
        ('Local da Ocorrência', {
            'fields': ('data_ocorrencia', 'logradouro_ocorrencia', 'bairro_ocorrencia', 'ponto_referencia')
        }),
        ('Anexos e Status', {
            'fields': ('anexo', 'status', 'observacoes_internas')
        }),
    )
    readonly_fields = ('data_criacao', 'data_atualizacao')

    def get_dias_pendente(self, obj):
        """Display days since complaint was created."""
        dias = obj.dias_pendente
        if dias == 0:
            return "Hoje"
        elif dias == 1:
            return "1 dia"
        else:
            return f"{dias} dias"
    get_dias_pendente.short_description = 'Tempo Pendente'

    # Custom actions
    def marcar_como_resolvido(self, request, queryset):
        """Bulk mark complaints as resolved."""
        updated = queryset.update(status='resolvido')
        self.message_user(
            request,
            f'{updated} denúncia(s) foram marcada(s) como resolvida(s).'
        )
    marcar_como_resolvido.short_description = 'Marcar como resolvido'

    def colocar_em_analise(self, request, queryset):
        """Bulk put complaints in analysis."""
        updated = queryset.update(status='em_analise')
        self.message_user(
            request,
            f'{updated} denúncia(s) foram colocada(s) em análise.'
        )
    colocar_em_analise.short_description = 'Colocar em análise'

    actions = [marcar_como_resolvido, colocar_em_analise]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    """Admin configuration for Comentario model."""
    
    list_display = ('denuncia', 'usuario', 'get_resumo_texto', 'eh_publico', 'data_hora')
    list_filter = ('eh_publico', 'data_hora')
    search_fields = ('texto', 'usuario__username', 'denuncia__titulo')
    date_hierarchy = 'data_hora'
    fieldsets = (
        ('Comentário', {
            'fields': ('denuncia', 'usuario', 'texto', 'eh_publico')
        }),
    )

    def get_resumo_texto(self, obj):
        """Display truncated comment text."""
        return (obj.texto[:50] + '...') if len(obj.texto) > 50 else obj.texto
    get_resumo_texto.short_description = 'Texto (resumo)'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('usuario', 'denuncia')


@admin.register(Midia)
class MidiaAdmin(admin.ModelAdmin):
    """Admin configuration for Midia model."""
    
    list_display = ('denuncia', 'tipo', 'get_preview', 'descricao', 'data_upload')
    list_filter = ('tipo', 'data_upload')
    search_fields = ('denuncia__titulo', 'descricao')
    date_hierarchy = 'data_upload'
    fieldsets = (
        ('Informações da Mídia', {
            'fields': ('denuncia', 'tipo', 'descricao')
        }),
        ('Arquivo', {
            'fields': ('arquivo', 'url_arquivo')
        }),
    )

    def get_preview(self, obj):
        """Display media preview."""
        if obj.arquivo and obj.tipo == 'imagem':
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px;" />',
                obj.arquivo.url
            )
        elif obj.url_arquivo:
            return format_html(
                '<a href="{}" target="_blank">🔗 Ver arquivo</a>',
                obj.url_arquivo
            )
        elif obj.arquivo:
            return format_html(
                '<a href="{}" target="_blank">📎 Baixar arquivo</a>',
                obj.arquivo.url
            )
        return "-"
    get_preview.short_description = 'Preview'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('denuncia')


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    """Admin configuration for Notificacao model."""
    
    list_display = ('usuario', 'tipo', 'denuncia', 'lida', 'data_hora')
    list_filter = ('tipo', 'lida', 'data_hora')
    search_fields = ('mensagem', 'usuario__username', 'denuncia__titulo')
    date_hierarchy = 'data_hora'
    fieldsets = (
        ('Notificação', {
            'fields': ('usuario', 'denuncia', 'tipo', 'mensagem')
        }),
        ('Status', {
            'fields': ('lida',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('usuario', 'denuncia')

    # Custom actions
    def marcar_como_lida(self, request, queryset):
        """Bulk mark notifications as read."""
        updated = queryset.update(lida=True)
        self.message_user(
            request,
            f'{updated} notificação(ões) foram marcada(s) como lida(s).'
        )
    marcar_como_lida.short_description = 'Marcar como lida'

    actions = [marcar_como_lida]


@admin.register(BuscaDenuncia)
class BuscaDenunciaAdmin(admin.ModelAdmin):
    """Admin configuration for BuscaDenuncia model."""
    
    list_display = (
        'termo', 'usuario', 'categoria', 'status', 'bairro',
        'total_resultados', 'data_busca'
    )
    list_filter = ('categoria', 'status', 'tipo', 'bairro', 'data_busca')
    search_fields = ('termo', 'usuario__username', 'bairro')
    date_hierarchy = 'data_busca'
    fieldsets = (
        ('Termos de Busca', {
            'fields': ('usuario', 'termo')
        }),
        ('Filtros Aplicados', {
            'fields': ('categoria', 'status', 'tipo', 'bairro')
        }),
        ('Período', {
            'fields': ('data_inicial', 'data_final')
        }),
        ('Resultados', {
            'fields': ('total_resultados',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('usuario')
