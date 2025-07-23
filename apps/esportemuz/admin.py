from django.contrib import admin
from .models import (
    Modalidade, Equipe, TipoCampeonato, Campeonato,
    LocalPartida, Partida, Classificacao
)


class ClassificacaoInline(admin.TabularInline):
    """Inline admin for team classifications."""
    model = Classificacao
    extra = 0
    fields = ('equipe', 'pontos', 'partidas_jogadas', 'vitorias', 'empates', 'derrotas')
    readonly_fields = ('saldo_gols',)


class PartidaInline(admin.TabularInline):
    """Inline admin for matches."""
    model = Partida
    extra = 0
    fields = ('equipe_mandante', 'equipe_visitante', 'data_hora', 'local', 'status')


@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    """Admin configuration for Modalidade model."""
    
    list_display = ('nome_display', 'ativa', 'get_total_campeonatos', 'data_criacao')
    list_filter = ('ativa', 'data_criacao')
    search_fields = ('nome',)
    date_hierarchy = 'data_criacao'
    fieldsets = (
        ('Informações da Modalidade', {
            'fields': ('nome', 'ativa')
        }),
    )

    def nome_display(self, obj):
        """Display formatted name."""
        return str(obj)
    nome_display.short_description = 'Nome'

    def get_total_campeonatos(self, obj):
        """Display total number of championships."""
        return obj.campeonatos.count()
    get_total_campeonatos.short_description = 'Total de Campeonatos'


@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    """Admin configuration for Equipe model."""
    
    list_display = ('nome_display', 'cidade', 'data_fundacao', 'ativa', 'data_criacao')
    list_filter = ('ativa', 'cidade', 'data_criacao')
    search_fields = ('nome', 'cidade')
    date_hierarchy = 'data_criacao'
    fieldsets = (
        ('Informações da Equipe', {
            'fields': ('nome', 'escudo', 'cidade', 'data_fundacao')
        }),
        ('Status', {
            'fields': ('ativa',)
        }),
    )

    def nome_display(self, obj):
        """Display formatted name."""
        return str(obj)
    nome_display.short_description = 'Nome'


@admin.register(TipoCampeonato)
class TipoCampeonatoAdmin(admin.ModelAdmin):
    """Admin configuration for TipoCampeonato model."""
    
    list_display = ('nome_display', 'ativo', 'get_total_campeonatos')
    list_filter = ('ativo',)
    search_fields = ('nome', 'descricao')
    fieldsets = (
        ('Informações do Tipo', {
            'fields': ('nome', 'descricao', 'ativo')
        }),
    )

    def nome_display(self, obj):
        """Display formatted name."""
        return str(obj)
    nome_display.short_description = 'Nome'

    def get_total_campeonatos(self, obj):
        """Display total number of championships."""
        return obj.campeonatos.count()
    get_total_campeonatos.short_description = 'Total de Campeonatos'


@admin.register(LocalPartida)
class LocalPartidaAdmin(admin.ModelAdmin):
    """Admin configuration for LocalPartida model."""
    
    list_display = ('nome_display', 'endereco', 'capacidade', 'ativo', 'get_total_partidas')
    list_filter = ('ativo',)
    search_fields = ('nome', 'endereco')
    fieldsets = (
        ('Informações do Local', {
            'fields': ('nome', 'endereco', 'capacidade', 'ativo')
        }),
    )

    def nome_display(self, obj):
        """Display formatted name."""
        return str(obj)
    nome_display.short_description = 'Nome'

    def get_total_partidas(self, obj):
        """Display total number of matches."""
        return obj.partidas.count()
    get_total_partidas.short_description = 'Total de Partidas'


@admin.register(Campeonato)
class CampeonatoAdmin(admin.ModelAdmin):
    """Admin configuration for Campeonato model."""
    
    list_display = ('nome_display', 'modalidade', 'tipo_campeonato', 'data_inicio', 'data_fim', 'status', 'total_equipes')
    list_filter = ('status', 'modalidade', 'tipo_campeonato', 'data_inicio')
    search_fields = ('nome', 'modalidade__nome', 'tipo_campeonato__nome')
    date_hierarchy = 'data_inicio'
    inlines = [ClassificacaoInline, PartidaInline]
    fieldsets = (
        ('Informações do Campeonato', {
            'fields': ('nome', 'modalidade', 'tipo_campeonato')
        }),
        ('Período', {
            'fields': ('data_inicio', 'data_fim')
        }),
        ('Status e Premiação', {
            'fields': ('status', 'premiacao')
        }),
    )

    def nome_display(self, obj):
        """Display formatted name."""
        return str(obj)
    nome_display.short_description = 'Nome'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('modalidade', 'tipo_campeonato')


@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    """Admin configuration for Partida model."""
    
    list_display = ('get_partida_display', 'campeonato', 'data_hora', 'local', 'get_placar', 'status')
    list_filter = ('status', 'campeonato', 'local', 'data_hora')
    search_fields = ('campeonato__nome', 'equipe_mandante__nome', 'equipe_visitante__nome')
    date_hierarchy = 'data_hora'
    fieldsets = (
        ('Informações da Partida', {
            'fields': ('campeonato', 'equipe_mandante', 'equipe_visitante')
        }),
        ('Data e Local', {
            'fields': ('data_hora', 'local')
        }),
        ('Resultado', {
            'fields': ('gols_mandante', 'gols_visitante', 'status')
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
    )

    def get_partida_display(self, obj):
        """Display match teams."""
        return f"{obj.equipe_mandante} vs {obj.equipe_visitante}"
    get_partida_display.short_description = 'Partida'

    def get_placar(self, obj):
        """Display match score."""
        if obj.status == 'encerrada':
            return f"{obj.gols_mandante} x {obj.gols_visitante}"
        return "-"
    get_placar.short_description = 'Placar'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'campeonato', 'equipe_mandante', 'equipe_visitante', 'local'
        )


@admin.register(Classificacao)
class ClassificacaoAdmin(admin.ModelAdmin):
    """Admin configuration for Classificacao model."""
    
    list_display = ('equipe', 'campeonato', 'pontos', 'partidas_jogadas', 'vitorias', 'empates', 'derrotas', 'saldo_gols', 'aproveitamento_display')
    list_filter = ('campeonato', 'campeonato__modalidade')
    search_fields = ('equipe__nome', 'campeonato__nome')
    readonly_fields = ('saldo_gols',)
    fieldsets = (
        ('Informações', {
            'fields': ('campeonato', 'equipe')
        }),
        ('Estatísticas', {
            'fields': ('pontos', 'partidas_jogadas', 'vitorias', 'empates', 'derrotas')
        }),
        ('Gols', {
            'fields': ('gols_pro', 'gols_contra', 'saldo_gols')
        }),
    )

    def aproveitamento_display(self, obj):
        """Display team performance percentage."""
        return f"{obj.aproveitamento}%"
    aproveitamento_display.short_description = 'Aproveitamento'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('campeonato', 'equipe')