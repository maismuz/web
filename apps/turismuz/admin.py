from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Avaliacao, Categorias, Estabelecimento, GuiaTuristico,
    ImagemPublicacao, Permissao, Publicacao
)


class ImagemPublicacaoInline(admin.TabularInline):
    """Inline admin for publication images."""
    model = ImagemPublicacao
    extra = 1
    fields = ('imagem', 'legenda', 'ordem')


@admin.register(Permissao)
class PermissaoAdmin(admin.ModelAdmin):
    """Admin configuration for Permissao model."""
    
    list_display = ('get_tipo_display', 'ativa')
    list_filter = ('tipo', 'ativa')
    search_fields = ('descricao',)
    fieldsets = (
        ('Informações da Permissão', {
            'fields': ('tipo', 'descricao', 'ativa')
        }),
    )

    def get_tipo_display(self, obj):
        """Display permission type."""
        return obj.get_tipo_display()
    get_tipo_display.short_description = 'Tipo'


@admin.register(Categorias)
class CategoriasAdmin(admin.ModelAdmin):
    """Admin configuration for Categorias model."""
    
    list_display = ('nome', 'ativa', 'get_total_estabelecimentos', 'get_total_publicacoes', 'data_criacao')
    list_filter = ('ativa', 'data_criacao')
    search_fields = ('nome', 'descricao')
    date_hierarchy = 'data_criacao'
    fieldsets = (
        ('Informações da Categoria', {
            'fields': ('nome', 'descricao', 'ativa')
        }),
    )

    def get_total_estabelecimentos(self, obj):
        """Display total number of establishments in category."""
        return obj.estabelecimentos.count()
    get_total_estabelecimentos.short_description = 'Estabelecimentos'

    def get_total_publicacoes(self, obj):
        """Display total number of publications in category."""
        return obj.publicacoes.count()
    get_total_publicacoes.short_description = 'Publicações'


@admin.register(Estabelecimento)
class EstabelecimentoAdmin(admin.ModelAdmin):
    """Admin configuration for Estabelecimento model."""
    
    list_display = ('nome', 'categoria', 'status', 'contato', 'get_nota_media', 'data_cadastro')
    list_filter = ('status', 'categoria', 'data_cadastro')
    search_fields = ('nome', 'endereco', 'descricao', 'contato')
    date_hierarchy = 'data_cadastro'
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'categoria', 'endereco', 'contato')
        }),
        ('Detalhes', {
            'fields': ('horario_funcionamento', 'descricao', 'imagem')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

    def get_nota_media(self, obj):
        """Display average rating."""
        avaliacoes = obj.avaliacoes.filter(aprovada=True)
        if avaliacoes.exists():
            media = sum(a.nota for a in avaliacoes) / avaliacoes.count()
            return f"{media:.1f}★"
        return "Sem avaliações"
    get_nota_media.short_description = 'Avaliação'

    # Custom actions
    def aprovar_estabelecimentos(self, request, queryset):
        """Bulk approve establishments."""
        updated = queryset.update(status='aprovado')
        self.message_user(
            request,
            f'{updated} estabelecimento(s) foram aprovado(s) com sucesso.'
        )
    aprovar_estabelecimentos.short_description = 'Aprovar estabelecimentos selecionados'

    def rejeitar_estabelecimentos(self, request, queryset):
        """Bulk reject establishments."""
        updated = queryset.update(status='rejeitado')
        self.message_user(
            request,
            f'{updated} estabelecimento(s) foram rejeitado(s).'
        )
    rejeitar_estabelecimentos.short_description = 'Rejeitar estabelecimentos selecionados'

    actions = [aprovar_estabelecimentos, rejeitar_estabelecimentos]


@admin.register(GuiaTuristico)
class GuiaTuristicoAdmin(admin.ModelAdmin):
    """Admin configuration for GuiaTuristico model."""
    
    list_display = ('nome', 'nivel_dificuldade', 'valor', 'entidade_responsavel', 'ativo', 'get_nota_media', 'data_cadastro')
    list_filter = ('nivel_dificuldade', 'ativo', 'data_cadastro')
    search_fields = ('nome', 'descricao', 'entidade_responsavel', 'contato')
    date_hierarchy = 'data_cadastro'
    fieldsets = (
        ('Informações do Guia', {
            'fields': ('nome', 'descricao', 'imagem')
        }),
        ('Detalhes do Tour', {
            'fields': ('duracao', 'nivel_dificuldade', 'valor', 'pontos_parada')
        }),
        ('Responsável', {
            'fields': ('entidade_responsavel', 'contato')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )

    def get_nota_media(self, obj):
        """Display average rating."""
        avaliacoes = obj.avaliacoes.filter(aprovada=True)
        if avaliacoes.exists():
            media = sum(a.nota for a in avaliacoes) / avaliacoes.count()
            return f"{media:.1f}★"
        return "Sem avaliações"
    get_nota_media.short_description = 'Avaliação'


@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    """Admin configuration for Publicacao model."""
    
    list_display = ('titulo', 'autor', 'categoria', 'status', 'visualizacoes', 'data_publicacao')
    list_filter = ('status', 'categoria', 'data_publicacao')
    search_fields = ('titulo', 'texto_noticia', 'autor')
    date_hierarchy = 'data_publicacao'
    inlines = [ImagemPublicacaoInline]
    fieldsets = (
        ('Conteúdo', {
            'fields': ('titulo', 'resumo', 'texto_noticia', 'categoria')
        }),
        ('Mídia', {
            'fields': ('imagem_principal', 'legenda_imagem')
        }),
        ('Publicação', {
            'fields': ('autor', 'status')
        }),
        ('Estatísticas', {
            'fields': ('visualizacoes',),
            'classes': ('collapse',)
        }),
    )

    # Custom actions
    def publicar_artigos(self, request, queryset):
        """Bulk publish articles."""
        updated = queryset.update(status='publicado')
        self.message_user(
            request,
            f'{updated} publicação(ões) foram publicada(s) com sucesso.'
        )
    publicar_artigos.short_description = 'Publicar artigos selecionados'

    def arquivar_artigos(self, request, queryset):
        """Bulk archive articles."""
        updated = queryset.update(status='arquivado')
        self.message_user(
            request,
            f'{updated} publicação(ões) foram arquivada(s).'
        )
    arquivar_artigos.short_description = 'Arquivar artigos selecionados'

    actions = [publicar_artigos, arquivar_artigos]


@admin.register(ImagemPublicacao)
class ImagemPublicacaoAdmin(admin.ModelAdmin):
    """Admin configuration for ImagemPublicacao model."""
    
    list_display = ('publicacao', 'legenda', 'ordem', 'get_preview')
    list_filter = ('publicacao__categoria',)
    search_fields = ('publicacao__titulo', 'legenda')
    fieldsets = (
        ('Informações da Imagem', {
            'fields': ('publicacao', 'imagem', 'legenda', 'ordem')
        }),
    )

    def get_preview(self, obj):
        """Display image preview."""
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px;" />',
                obj.imagem.url
            )
        return "Sem imagem"
    get_preview.short_description = 'Preview'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('publicacao')


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    """Admin configuration for Avaliacao model."""
    
    list_display = ('get_objeto_avaliado', 'usuario', 'nota', 'get_nota_display', 'aprovada', 'data_avaliacao')
    list_filter = ('tipo_avaliacao', 'nota', 'aprovada', 'data_avaliacao')
    search_fields = ('usuario', 'comentario', 'estabelecimento__nome', 'guia_turistico__nome')
    date_hierarchy = 'data_avaliacao'
    fieldsets = (
        ('Avaliação', {
            'fields': ('tipo_avaliacao', 'estabelecimento', 'guia_turistico', 'nota')
        }),
        ('Comentário', {
            'fields': ('comentario',)
        }),
        ('Avaliador', {
            'fields': ('usuario', 'email')
        }),
        ('Status', {
            'fields': ('aprovada',)
        }),
    )

    def get_objeto_avaliado(self, obj):
        """Display evaluated object."""
        if obj.estabelecimento:
            return f"Estabelecimento: {obj.estabelecimento.nome}"
        elif obj.guia_turistico:
            return f"Guia: {obj.guia_turistico.nome}"
        return "N/A"
    get_objeto_avaliado.short_description = 'Objeto Avaliado'

    def get_nota_display(self, obj):
        """Display rating with stars."""
        return f"{'★' * obj.nota}{'☆' * (5 - obj.nota)}"
    get_nota_display.short_description = 'Estrelas'

    # Custom actions
    def aprovar_avaliacoes(self, request, queryset):
        """Bulk approve evaluations."""
        updated = queryset.update(aprovada=True)
        self.message_user(
            request,
            f'{updated} avaliação(ões) foram aprovada(s) com sucesso.'
        )
    aprovar_avaliacoes.short_description = 'Aprovar avaliações selecionadas'

    def reprovar_avaliacoes(self, request, queryset):
        """Bulk disapprove evaluations."""
        updated = queryset.update(aprovada=False)
        self.message_user(
            request,
            f'{updated} avaliação(ões) foram reprovada(s).'
        )
    reprovar_avaliacoes.short_description = 'Reprovar avaliações selecionadas'

    actions = [aprovar_avaliacoes, reprovar_avaliacoes]

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('estabelecimento', 'guia_turistico')

