from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Motorista_MoveMuz, Combustivel, TipoVeiculo, Veiculo, Local,
    EscalaVeiculo, HorarioTransporte, Viagem, Passageiro, Ponto,
    Parada, OcupacaoVeiculo
)


# Inline admins
class EscalaVeiculoInline(admin.TabularInline):
    """Inline admin for vehicle schedules."""
    model = EscalaVeiculo
    extra = 0
    fields = ('motorista', 'data_inicio', 'data_fim', 'turno')


class ParadaInline(admin.TabularInline):
    """Inline admin for stops."""
    model = Parada
    extra = 0
    fields = ('ponto', 'ordem', 'horario', 'tempo_parada', 'passageiros_estimados')
    ordering = ['ordem']


class PassageiroInline(admin.TabularInline):
    """Inline admin for passengers."""
    model = Passageiro
    extra = 0
    fields = ('nome', 'documento', 'telefone', 'ponto_embarque', 'ponto_desembarque')


# Admin configurations
@admin.register(Motorista_MoveMuz)
class MotoristaAdmin(admin.ModelAdmin):
    """Admin configuration for Motorista_MoveMuz model."""
    
    list_display = ('nome', 'cnh_numero', 'categoria_cnh', 'get_idade', 'get_cnh_status', 'ativo', 'data_cadastro')
    list_filter = ('ativo', 'categoria_cnh', 'data_cadastro')
    search_fields = ('nome', 'cpf', 'cnh_numero', 'telefone')
    date_hierarchy = 'data_cadastro'
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'cpf', 'data_nascimento', 'telefone', 'email', 'endereco')
        }),
        ('Documentos de Habilitação', {
            'fields': ('cnh_numero', 'categoria_cnh', 'validade_cnh')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )

    def get_idade(self, obj):
        """Display driver's age."""
        idade = obj.idade
        return f"{idade} anos" if idade is not None else "N/A"
    get_idade.short_description = 'Idade'

    def get_cnh_status(self, obj):
        """Display CNH status."""
        if obj.cnh_valida:
            return format_html('<span style="color: green;">Válida</span>')
        else:
            return format_html('<span style="color: red;">Vencida</span>')
    get_cnh_status.short_description = 'Status CNH'


@admin.register(Combustivel)
class CombustivelAdmin(admin.ModelAdmin):
    """Admin configuration for Combustivel model."""
    
    list_display = ('nome', 'ativo', 'get_total_veiculos')
    list_filter = ('ativo',)
    search_fields = ('nome', 'descricao')
    fieldsets = (
        ('Informações do Combustível', {
            'fields': ('nome', 'descricao', 'ativo')
        }),
    )

    def get_total_veiculos(self, obj):
        """Display total number of vehicles using this fuel."""
        return obj.veiculos.count()
    get_total_veiculos.short_description = 'Total de Veículos'


@admin.register(TipoVeiculo)
class TipoVeiculoAdmin(admin.ModelAdmin):
    """Admin configuration for TipoVeiculo model."""
    
    list_display = ('nome', 'capacidade_padrao', 'get_total_veiculos')
    search_fields = ('nome', 'descricao')
    fieldsets = (
        ('Informações do Tipo', {
            'fields': ('nome', 'descricao', 'capacidade_padrao')
        }),
    )

    def get_total_veiculos(self, obj):
        """Display total number of vehicles of this type."""
        return obj.veiculos.count()
    get_total_veiculos.short_description = 'Total de Veículos'


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    """Admin configuration for Local model."""
    
    list_display = ('nome', 'cidade', 'estado', 'ativo')
    list_filter = ('estado', 'ativo')
    search_fields = ('nome', 'cidade', 'endereco')
    fieldsets = (
        ('Informações do Local', {
            'fields': ('nome', 'endereco', 'cidade', 'estado', 'cep')
        }),
        ('Localização', {
            'fields': ('coordenadas',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    """Admin configuration for Veiculo model."""
    
    list_display = ('get_veiculo_display', 'placa', 'tipo', 'capacidade', 'condicao_manutencao', 'quilometragem')
    list_filter = ('tipo', 'combustivel', 'condicao_manutencao', 'data_cadastro')
    search_fields = ('marca', 'modelo', 'placa', 'renavam')
    date_hierarchy = 'data_cadastro'
    inlines = [EscalaVeiculoInline]
    fieldsets = (
        ('Informações do Veículo', {
            'fields': ('marca', 'modelo', 'tipo', 'cor', 'ano_fabricacao', 'ano_modelo')
        }),
        ('Documentação', {
            'fields': ('placa', 'renavam', 'chassi')
        }),
        ('Especificações', {
            'fields': ('combustivel', 'capacidade', 'quilometragem')
        }),
        ('Estado e Manutenção', {
            'fields': ('condicao_manutencao', 'observacoes')
        }),
        ('Mídia', {
            'fields': ('foto',),
            'classes': ('collapse',)
        }),
    )

    def get_veiculo_display(self, obj):
        """Display vehicle information."""
        return f"{obj.marca} {obj.modelo} ({obj.ano_fabricacao})"
    get_veiculo_display.short_description = 'Veículo'


@admin.register(HorarioTransporte)
class HorarioTransporteAdmin(admin.ModelAdmin):
    """Admin configuration for HorarioTransporte model."""
    
    list_display = ('nome', 'get_rota', 'horario_partida', 'dias_funcionamento', 'veiculo', 'ativo')
    list_filter = ('dias_funcionamento', 'ativo', 'origem__cidade', 'destino__cidade')
    search_fields = ('nome', 'origem__nome', 'destino__nome', 'veiculo__modelo')
    inlines = [ParadaInline]
    fieldsets = (
        ('Informações da Linha', {
            'fields': ('nome', 'veiculo')
        }),
        ('Rota', {
            'fields': ('origem', 'destino')
        }),
        ('Horários', {
            'fields': ('horario_partida', 'horario_chegada_previsto', 'dias_funcionamento')
        }),
        ('Observações e Status', {
            'fields': ('observacoes', 'ativo')
        }),
    )

    def get_rota(self, obj):
        """Display route information."""
        return f"{obj.origem.cidade} → {obj.destino.cidade}"
    get_rota.short_description = 'Rota'


@admin.register(Ponto)
class PontoAdmin(admin.ModelAdmin):
    """Admin configuration for Ponto model."""
    
    list_display = ('nome', 'local', 'endereco', 'ativo')
    list_filter = ('local__cidade', 'ativo')
    search_fields = ('nome', 'endereco', 'local__nome')
    fieldsets = (
        ('Informações do Ponto', {
            'fields': ('nome', 'local', 'endereco')
        }),
        ('Localização', {
            'fields': ('coordenadas',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )


@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    """Admin configuration for Parada model."""
    
    list_display = ('get_linha', 'ponto', 'ordem', 'horario', 'tempo_parada', 'passageiros_estimados')
    list_filter = ('horario_transporte__nome', 'ponto__local__cidade')
    search_fields = ('horario_transporte__nome', 'ponto__nome')
    fieldsets = (
        ('Informações da Parada', {
            'fields': ('horario_transporte', 'ponto', 'ordem')
        }),
        ('Horários', {
            'fields': ('horario', 'tempo_parada')
        }),
        ('Estimativas', {
            'fields': ('passageiros_estimados',)
        }),
    )

    def get_linha(self, obj):
        """Display transport line name."""
        return obj.horario_transporte.nome
    get_linha.short_description = 'Linha'


@admin.register(Viagem)
class ViagemAdmin(admin.ModelAdmin):
    """Admin configuration for Viagem model."""
    
    list_display = ('get_linha', 'data_viagem', 'motorista', 'status', 'passageiros_transportados', 'get_quilometragem')
    list_filter = ('status', 'data_viagem', 'horario_transporte__nome')
    search_fields = ('horario_transporte__nome', 'motorista__nome')
    date_hierarchy = 'data_viagem'
    inlines = [PassageiroInline]
    fieldsets = (
        ('Informações da Viagem', {
            'fields': ('horario_transporte', 'motorista', 'data_viagem', 'status')
        }),
        ('Horários Reais', {
            'fields': ('horario_saida_real', 'horario_chegada_real')
        }),
        ('Controle de Quilometragem', {
            'fields': ('quilometragem_inicial', 'quilometragem_final')
        }),
        ('Passageiros e Observações', {
            'fields': ('passageiros_transportados', 'observacoes')
        }),
    )

    def get_linha(self, obj):
        """Display transport line name."""
        return obj.horario_transporte.nome
    get_linha.short_description = 'Linha'

    def get_quilometragem(self, obj):
        """Display distance traveled."""
        km = obj.quilometragem_percorrida
        return f"{km} km" if km is not None else "N/A"
    get_quilometragem.short_description = 'Km Percorrida'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('horario_transporte', 'motorista')


@admin.register(Passageiro)
class PassageiroAdmin(admin.ModelAdmin):
    """Admin configuration for Passageiro model."""
    
    list_display = ('nome', 'get_viagem_info', 'ponto_embarque', 'ponto_desembarque', 'telefone')
    list_filter = ('viagem__data_viagem', 'ponto_embarque__local__cidade')
    search_fields = ('nome', 'documento', 'telefone', 'viagem__horario_transporte__nome')
    fieldsets = (
        ('Informações do Passageiro', {
            'fields': ('viagem', 'nome', 'documento', 'telefone')
        }),
        ('Pontos de Embarque/Desembarque', {
            'fields': ('ponto_embarque', 'ponto_desembarque')
        }),
        ('Observações', {
            'fields': ('observacao',),
            'classes': ('collapse',)
        }),
    )

    def get_viagem_info(self, obj):
        """Display trip information."""
        return f"{obj.viagem.horario_transporte.nome} - {obj.viagem.data_viagem}"
    get_viagem_info.short_description = 'Viagem'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'viagem', 'viagem__horario_transporte', 'ponto_embarque', 'ponto_desembarque'
        )


@admin.register(EscalaVeiculo)
class EscalaVeiculoAdmin(admin.ModelAdmin):
    """Admin configuration for EscalaVeiculo model."""
    
    list_display = ('veiculo', 'motorista', 'data_inicio', 'data_fim', 'turno')
    list_filter = ('turno', 'data_inicio', 'data_fim')
    search_fields = ('veiculo__modelo', 'motorista__nome')
    date_hierarchy = 'data_inicio'
    fieldsets = (
        ('Informações da Escala', {
            'fields': ('veiculo', 'motorista', 'turno')
        }),
        ('Período', {
            'fields': ('data_inicio', 'data_fim')
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('veiculo', 'motorista')


@admin.register(OcupacaoVeiculo)
class OcupacaoVeiculoAdmin(admin.ModelAdmin):
    """Admin configuration for OcupacaoVeiculo model."""
    
    list_display = ('get_viagem_info', 'get_ocupacao_display', 'get_taxa_ocupacao', 'vagas_disponiveis', 'atualizado_em')
    list_filter = ('viagem__data_viagem', 'viagem__horario_transporte__nome')
    search_fields = ('viagem__horario_transporte__nome', 'viagem__motorista__nome')
    fieldsets = (
        ('Informações da Ocupação', {
            'fields': ('viagem',)
        }),
        ('Passageiros', {
            'fields': ('passageiros_confirmados', 'passageiros_em_espera')
        }),
    )

    def get_viagem_info(self, obj):
        """Display trip information."""
        return f"{obj.viagem.horario_transporte.nome} - {obj.viagem.data_viagem}"
    get_viagem_info.short_description = 'Viagem'

    def get_ocupacao_display(self, obj):
        """Display occupancy information."""
        capacidade = obj.viagem.horario_transporte.veiculo.capacidade
        return f"{obj.passageiros_confirmados}/{capacidade}"
    get_ocupacao_display.short_description = 'Ocupação'

    def get_taxa_ocupacao(self, obj):
        """Display occupancy rate."""
        return f"{obj.taxa_ocupacao}%"
    get_taxa_ocupacao.short_description = 'Taxa de Ocupação'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'viagem', 'viagem__horario_transporte', 'viagem__horario_transporte__veiculo'
        )