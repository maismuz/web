from django.contrib import admin
from django.utils.html import format_html
from .models import Paciente, Solicitacao, Agendamento


class SolicitacaoInline(admin.TabularInline):
    """Inline admin for patient requests."""
    model = Solicitacao
    extra = 0
    fields = ('tipo', 'especialidade', 'status', 'prioridade', 'criado_em')
    readonly_fields = ('criado_em',)
    ordering = ['-criado_em']


class AgendamentoInline(admin.TabularInline):
    """Inline admin for appointments."""
    model = Agendamento
    extra = 0
    fields = ('data_hora_agendada', 'local', 'status', 'profissional')
    ordering = ['data_hora_agendada']


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    """Admin configuration for Paciente model."""
    
    list_display = (
        'nome_completo', 'cpf', 'get_idade_display', 'sexo', 
        'telefone', 'ativo', 'consentimento_lgpd', 'criado_em'
    )
    list_filter = ('sexo', 'ativo', 'consentimento_lgpd', 'criado_em')
    search_fields = ('nome_completo', 'cpf', 'telefone', 'email')
    date_hierarchy = 'criado_em'
    readonly_fields = ('criado_em', 'atualizado_em')
    inlines = [SolicitacaoInline]
    fieldsets = (
        ('Informações Pessoais', {
            'fields': (
                'nome_completo', 'cpf', 'data_nascimento', 'sexo',
                'telefone', 'email'
            )
        }),
        ('Endereço', {
            'fields': ('endereco',)
        }),
        ('Informações Médicas', {
            'fields': ('historico_medico', 'observacoes'),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('ativo', 'consentimento_lgpd', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

    def get_idade_display(self, obj):
        """Display patient's age."""
        idade = obj.idade
        return f"{idade} anos" if idade is not None else "N/A"
    get_idade_display.short_description = 'Idade'

    # Custom actions
    def ativar_pacientes(self, request, queryset):
        """Bulk activate patients."""
        updated = queryset.update(ativo=True)
        self.message_user(
            request,
            f'{updated} paciente(s) foram ativado(s) com sucesso.'
        )
    ativar_pacientes.short_description = 'Ativar pacientes selecionados'

    def desativar_pacientes(self, request, queryset):
        """Bulk deactivate patients."""
        updated = queryset.update(ativo=False)
        self.message_user(
            request,
            f'{updated} paciente(s) foram desativado(s).'
        )
    desativar_pacientes.short_description = 'Desativar pacientes selecionados'

    actions = [ativar_pacientes, desativar_pacientes]


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    """Admin configuration for Solicitacao model."""
    
    list_display = (
        'paciente', 'tipo', 'especialidade', 'prioridade', 
        'status', 'get_dias_pendente', 'criado_em'
    )
    list_filter = ('tipo', 'status', 'prioridade', 'especialidade', 'criado_em')
    search_fields = (
        'paciente__nome_completo', 'paciente__cpf', 'descricao', 
        'especialidade', 'justificativa'
    )
    date_hierarchy = 'criado_em'
    readonly_fields = ('criado_em', 'atualizado_em')
    inlines = [AgendamentoInline]
    fieldsets = (
        ('Informações da Solicitação', {
            'fields': (
                'paciente', 'tipo', 'especialidade', 'prioridade'
            )
        }),
        ('Descrição', {
            'fields': ('descricao', 'justificativa')
        }),
        ('Documentos', {
            'fields': ('arquivos',),
            'classes': ('collapse',)
        }),
        ('Status e Observações', {
            'fields': ('status', 'observacoes_internas')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

    def get_dias_pendente(self, obj):
        """Display days since request was created."""
        dias = obj.dias_pendente
        if dias == 0:
            return "Hoje"
        elif dias == 1:
            return "1 dia"
        else:
            return f"{dias} dias"
    get_dias_pendente.short_description = 'Tempo Pendente'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('paciente')

    # Custom actions
    def aprovar_solicitacoes(self, request, queryset):
        """Bulk approve requests."""
        updated = queryset.update(status='aprovado')
        self.message_user(
            request,
            f'{updated} solicitação(ões) foram aprovada(s) com sucesso.'
        )
    aprovar_solicitacoes.short_description = 'Aprovar solicitações selecionadas'

    def colocar_em_analise(self, request, queryset):
        """Bulk put requests in analysis."""
        updated = queryset.update(status='em_analise')
        self.message_user(
            request,
            f'{updated} solicitação(ões) foram colocada(s) em análise.'
        )
    colocar_em_analise.short_description = 'Colocar em análise'

    actions = [aprovar_solicitacoes, colocar_em_analise]


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    """Admin configuration for Agendamento model."""
    
    list_display = (
        'get_paciente_nome', 'get_tipo_solicitacao', 'data_hora_agendada', 
        'local', 'profissional', 'status', 'get_dias_ate_agendamento'
    )
    list_filter = ('status', 'data_hora_agendada', 'local', 'criado_em')
    search_fields = (
        'solicitacao__paciente__nome_completo', 
        'solicitacao__paciente__cpf',
        'local', 'profissional', 'observacoes'
    )
    date_hierarchy = 'data_hora_agendada'
    readonly_fields = ('criado_em', 'atualizado_em')
    fieldsets = (
        ('Informações do Agendamento', {
            'fields': (
                'solicitacao', 'data_hora_agendada', 'data_hora_fim',
                'profissional'
            )
        }),
        ('Local', {
            'fields': ('local', 'endereco_local')
        }),
        ('Status e Observações', {
            'fields': ('status', 'observacoes', 'motivo_cancelamento')
        }),
        ('Datas do Sistema', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

    def get_paciente_nome(self, obj):
        """Display patient name."""
        return obj.solicitacao.paciente.nome_completo
    get_paciente_nome.short_description = 'Paciente'

    def get_tipo_solicitacao(self, obj):
        """Display request type."""
        return obj.solicitacao.get_tipo_display()
    get_tipo_solicitacao.short_description = 'Tipo'

    def get_dias_ate_agendamento(self, obj):
        """Display days until appointment."""
        dias = obj.dias_ate_agendamento
        if dias is None:
            return "N/A"
        elif dias < 0:
            return format_html(
                '<span style="color: red;">Há {} dias</span>',
                abs(dias)
            )
        elif dias == 0:
            return format_html(
                '<span style="color: orange; font-weight: bold;">Hoje</span>'
            )
        elif dias == 1:
            return format_html(
                '<span style="color: green;">Amanhã</span>'
            )
        else:
            return format_html(
                '<span style="color: blue;">Em {} dias</span>',
                dias
            )
    get_dias_ate_agendamento.short_description = 'Prazo'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'solicitacao', 'solicitacao__paciente'
        )

    # Custom actions
    def confirmar_agendamentos(self, request, queryset):
        """Bulk confirm appointments."""
        updated = queryset.update(status='confirmado')
        self.message_user(
            request,
            f'{updated} agendamento(s) foram confirmado(s) com sucesso.'
        )
    confirmar_agendamentos.short_description = 'Confirmar agendamentos selecionados'

    def marcar_como_realizado(self, request, queryset):
        """Bulk mark appointments as completed."""
        updated = queryset.update(status='realizado')
        self.message_user(
            request,
            f'{updated} agendamento(s) foram marcado(s) como realizado(s).'
        )
    marcar_como_realizado.short_description = 'Marcar como realizado'

    actions = [confirmar_agendamentos, marcar_como_realizado]