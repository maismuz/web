from django.contrib import admin
from .models import (
    Categoria, Objeto, FotoObjeto, Transacao, HistoricoTransacao,
    Mensagem, AvaliacaoUsuario, Oferta
)


class FotoObjetoInline(admin.TabularInline):
    """Inline admin for additional object photos."""
    model = FotoObjeto
    extra = 1
    fields = ('imagem', 'descricao')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin configuration for Categoria model."""
    
    list_display = ('nome', 'ativa', 'get_total_objetos', 'get_total_ofertas')
    list_filter = ('ativa',)
    search_fields = ('nome', 'descricao')
    fieldsets = (
        ('Informações da Categoria', {
            'fields': ('nome', 'descricao', 'ativa')
        }),
    )

    def get_total_objetos(self, obj):
        """Display total number of objects in category."""
        return obj.objetos.count()
    get_total_objetos.short_description = 'Total de Objetos'

    def get_total_ofertas(self, obj):
        """Display total number of offers in category."""
        return obj.ofertas.count()
    get_total_ofertas.short_description = 'Total de Ofertas'


@admin.register(Objeto)
class ObjetoAdmin(admin.ModelAdmin):
    """Admin configuration for Objeto model."""
    
    list_display = ('nome', 'tipo', 'preco', 'categoria', 'estado', 'usuario', 'ativo', 'data_cadastro')
    list_filter = ('tipo', 'categoria', 'estado', 'ativo', 'data_cadastro')
    search_fields = ('nome', 'descricao', 'usuario__username')
    date_hierarchy = 'data_cadastro'
    inlines = [FotoObjetoInline]
    fieldsets = (
        ('Informações do Objeto', {
            'fields': ('nome', 'descricao', 'imagem', 'categoria')
        }),
        ('Transação', {
            'fields': ('tipo', 'preco', 'estado')
        }),
        ('Status', {
            'fields': ('usuario', 'ativo')
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('categoria', 'usuario')


@admin.register(FotoObjeto)
class FotoObjetoAdmin(admin.ModelAdmin):
    """Admin configuration for FotoObjeto model."""
    
    list_display = ('objeto', 'descricao', 'imagem')
    list_filter = ('objeto__categoria', 'objeto__tipo')
    search_fields = ('objeto__nome', 'descricao')


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    """Admin configuration for Transacao model."""
    
    list_display = ('nome', 'tipo', 'status', 'preco', 'usuario', 'data_transacao')
    list_filter = ('tipo', 'status', 'categoria', 'data_transacao')
    search_fields = ('nome', 'descricao', 'usuario__username')
    date_hierarchy = 'data_transacao'
    fieldsets = (
        ('Informações da Transação', {
            'fields': ('nome', 'descricao', 'tipo', 'categoria')
        }),
        ('Valores e Status', {
            'fields': ('preco', 'status')
        }),
        ('Usuário', {
            'fields': ('usuario',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('categoria', 'usuario')


@admin.register(HistoricoTransacao)
class HistoricoTransacaoAdmin(admin.ModelAdmin):
    """Admin configuration for HistoricoTransacao model."""
    
    list_display = ('usuario', 'objeto_oferecido', 'objeto_recebido', 'status', 'data')
    list_filter = ('status', 'data')
    search_fields = ('usuario__username', 'objeto_oferecido__nome', 'objeto_recebido__nome')
    date_hierarchy = 'data'
    fieldsets = (
        ('Informações da Transação', {
            'fields': ('usuario', 'status')
        }),
        ('Objetos', {
            'fields': ('objeto_oferecido', 'objeto_recebido')
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'usuario', 'objeto_oferecido', 'objeto_recebido'
        )


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    """Admin configuration for Mensagem model."""
    
    list_display = ('remetente', 'destinatario', 'assunto_display', 'mensagem_resumida', 'status', 'data_envio')
    list_filter = ('status', 'data_envio')
    search_fields = ('remetente__username', 'destinatario__username', 'assunto', 'mensagem')
    date_hierarchy = 'data_envio'
    fieldsets = (
        ('Participantes', {
            'fields': ('remetente', 'destinatario')
        }),
        ('Mensagem', {
            'fields': ('assunto', 'mensagem', 'objeto_relacionado')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

    def assunto_display(self, obj):
        """Display subject or default text."""
        return obj.assunto or "Sem assunto"
    assunto_display.short_description = 'Assunto'

    def mensagem_resumida(self, obj):
        """Display truncated message."""
        return (obj.mensagem[:40] + '...') if len(obj.mensagem) > 40 else obj.mensagem
    mensagem_resumida.short_description = 'Mensagem'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'remetente', 'destinatario', 'objeto_relacionado'
        )


@admin.register(AvaliacaoUsuario)
class AvaliacaoUsuarioAdmin(admin.ModelAdmin):
    """Admin configuration for AvaliacaoUsuario model."""
    
    list_display = ('usuario_avaliado', 'usuario_avaliador', 'nota', 'get_nota_display', 'data_avaliacao')
    list_filter = ('nota', 'data_avaliacao')
    search_fields = ('usuario_avaliado__username', 'usuario_avaliador__username', 'comentario')
    date_hierarchy = 'data_avaliacao'
    fieldsets = (
        ('Avaliação', {
            'fields': ('usuario_avaliado', 'usuario_avaliador', 'nota')
        }),
        ('Comentário', {
            'fields': ('comentario',)
        }),
        ('Transação Relacionada', {
            'fields': ('transacao',),
            'classes': ('collapse',)
        }),
    )

    def get_nota_display(self, obj):
        """Display rating with stars."""
        return f"{'★' * obj.nota}{'☆' * (5 - obj.nota)}"
    get_nota_display.short_description = 'Estrelas'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'usuario_avaliado', 'usuario_avaliador', 'transacao'
        )


@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    """Admin configuration for Oferta model."""
    
    list_display = ('titulo', 'categoria', 'preco', 'usuario', 'ativa', 'esta_valida', 'data_criacao')
    list_filter = ('ativa', 'categoria', 'data_criacao', 'data_validade')
    search_fields = ('titulo', 'descricao', 'usuario__username')
    date_hierarchy = 'data_criacao'
    fieldsets = (
        ('Informações da Oferta', {
            'fields': ('titulo', 'descricao', 'categoria', 'preco')
        }),
        ('Validade e Status', {
            'fields': ('data_validade', 'ativa')
        }),
        ('Usuário', {
            'fields': ('usuario',)
        }),
    )

    def esta_valida(self, obj):
        """Display if offer is still valid."""
        return obj.esta_valida
    esta_valida.boolean = True
    esta_valida.short_description = 'Válida'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('categoria', 'usuario')
