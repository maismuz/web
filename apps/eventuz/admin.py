from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Categoria, Evento, Midia


class MidiaInline(admin.TabularInline):
    """Inline admin for event media."""
    model = Midia
    extra = 1
    fields = ('tipo', 'titulo', 'arquivo', 'url_video', 'ordem')
    ordering = ['ordem']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin configuration for Categoria model."""
    
    list_display = ('nome', 'ativa', 'get_total_eventos', 'data_criacao')
    list_filter = ('ativa', 'data_criacao')
    search_fields = ('nome', 'descricao')
    date_hierarchy = 'data_criacao'
    fieldsets = (
        ('Informações da Categoria', {
            'fields': ('nome', 'descricao', 'ativa')
        }),
    )

    def get_total_eventos(self, obj):
        """Display total number of events in category."""
        return obj.eventos.count()
    get_total_eventos.short_description = 'Total de Eventos'


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """Admin configuration for Evento model."""
    
    list_display = (
        'nome', 'data_hora', 'local', 'categoria', 'organizador', 
        'status', 'get_resumo_descricao', 'get_link_rede_social'
    )
    list_filter = ('status', 'categoria', 'data_hora')
    search_fields = ('nome', 'organizador', 'local', 'descricao')
    date_hierarchy = 'data_hora'
    inlines = [MidiaInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'categoria', 'descricao')
        }),
        ('Data e Local', {
            'fields': ('data_hora', 'data_fim', 'local')
        }),
        ('Organizador', {
            'fields': ('organizador', 'cnpj')
        }),
        ('Contato', {
            'fields': ('contato', 'telefone', 'email')
        }),
        ('Redes Sociais e Site', {
            'fields': ('rede_social', 'site'),
            'classes': ('collapse',)
        }),
        ('Detalhes do Evento', {
            'fields': ('valor_ingresso', 'capacidade'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )
    readonly_fields = ('data_criacao', 'data_atualizacao')

    def get_resumo_descricao(self, obj):
        """Display truncated description."""
        descricao = obj.descricao[:100] + '...' if len(obj.descricao) > 100 else obj.descricao
        return format_html(
            '<div style="max-width: 300px; white-space: normal;">{}</div>',
            descricao
        )
    get_resumo_descricao.short_description = "Descrição"

    def get_link_rede_social(self, obj):
        """Display clickable social media link."""
        link = obj.link_rede_social()
        if link:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>',
                link,
                obj.rede_social[:30] + '...' if len(obj.rede_social) > 30 else obj.rede_social
            )
        return "-"
    get_link_rede_social.short_description = "Rede Social"

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('categoria')

    # Custom actions
    def aprovar_eventos(self, request, queryset):
        """Bulk approve events."""
        updated = queryset.update(status='aprovado')
        self.message_user(
            request,
            f'{updated} evento(s) foram aprovado(s) com sucesso.'
        )
    aprovar_eventos.short_description = 'Aprovar eventos selecionados'

    def rejeitar_eventos(self, request, queryset):
        """Bulk reject events."""
        updated = queryset.update(status='rejeitado')
        self.message_user(
            request,
            f'{updated} evento(s) foram rejeitado(s).'
        )
    rejeitar_eventos.short_description = 'Rejeitar eventos selecionados'

    actions = [aprovar_eventos, rejeitar_eventos]


@admin.register(Midia)
class MidiaAdmin(admin.ModelAdmin):
    """Admin configuration for Midia model."""
    
    list_display = ('get_titulo_display', 'evento', 'tipo', 'get_preview', 'ordem', 'data_upload')
    list_filter = ('tipo', 'data_upload', 'evento__categoria')
    search_fields = ('titulo', 'evento__nome')
    date_hierarchy = 'data_upload'
    fieldsets = (
        ('Informações da Mídia', {
            'fields': ('evento', 'tipo', 'titulo', 'ordem')
        }),
        ('Arquivo/URL', {
            'fields': ('arquivo', 'url_video')
        }),
    )

    def get_titulo_display(self, obj):
        """Display title or default text."""
        return obj.titulo or f"{obj.get_tipo_display()} sem título"
    get_titulo_display.short_description = 'Título'

    def get_preview(self, obj):
        """Display media preview."""
        if obj.is_foto() and obj.arquivo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.arquivo.url
            )
        elif obj.is_video():
            if obj.url_video:
                return format_html(
                    '<a href="{}" target="_blank">🎥 Ver vídeo</a>',
                    obj.url_video
                )
            elif obj.arquivo:
                return format_html(
                    '<a href="{}" target="_blank">🎥 Ver vídeo</a>',
                    obj.arquivo.url
                )
        return "-"
    get_preview.short_description = 'Preview'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('evento', 'evento__categoria')
