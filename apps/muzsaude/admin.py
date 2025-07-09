from django.contrib import admin
from .models import Paciente, Solicitacao, Agendamento


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'data_nascimento', 'telefone', 'criado_em')
    search_fields = ('nome_completo', 'cpf', 'telefone')
    list_filter = ('criado_em',)
    readonly_fields = ('criado_em',)
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'cpf', 'data_nascimento', 'telefone', 'endereco')
        }),
        ('Outros', {
            'fields': ('historico', 'consentimento_lgpd', 'criado_em')
        }),
    )


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'tipo', 'status', 'criado_em', 'atualizado_em')
    search_fields = ('paciente__nome_completo', 'tipo', 'descricao')
    list_filter = ('tipo', 'status', 'criado_em')
    readonly_fields = ('criado_em', 'atualizado_em')
    fieldsets = (
        ('Informações da Solicitação', {
            'fields': ('paciente', 'tipo', 'especialidade', 'descricao', 'arquivos')
        }),
        ('Status e Datas', {
            'fields': ('status', 'criado_em', 'atualizado_em')
        }),
    )


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('solicitacao', 'data_hora_agendada', 'local', 'status_agendamento', 'criado_em')
    search_fields = ('solicitacao__paciente__nome_completo', 'local')
    list_filter = ('status_agendamento', 'data_hora_agendada', 'criado_em')
    readonly_fields = ('criado_em',)
    fieldsets = (
        ('Informações do Agendamento', {
            'fields': ('solicitacao', 'data_hora_agendada', 'local', 'observacoes')
        }),
        ('Status e Datas', {
            'fields': ('status_agendamento', 'criado_em')
        }),
    )