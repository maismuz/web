from django.db import models
from django.core.validators import RegexValidator

class Paciente(models.Model):
    nome_completo = models.CharField(
        max_length=150,
        verbose_name="Nome Completo"
    )
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r'^\d{11}$', 'O CPF deve conter 11 dígitos.')],
        verbose_name="CPF"
    )
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento"
    )
    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone"
    )
    endereco = models.TextField(
        verbose_name="Endereço"
    )
    historico = models.TextField(
        blank=True,
        null=True,
        verbose_name="Histórico Médico"
    )
    consentimento_lgpd = models.BooleanField(
        default=False,
        verbose_name="Consentimento LGPD"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo


class Solicitacao(models.Model):
    CONSULTA = 'consulta'
    CIRURGIA = 'cirurgia'
    TRANSPORTE = 'transporte'

    PENDENTE = 'pendente'
    ANALISE = 'analise'
    AGENDADO = 'agendado'
    CONCLUIDO = 'concluido'

    TIPO_CHOICES = [
        (CONSULTA, 'Consulta'),
        (CIRURGIA, 'Cirurgia'),
        (TRANSPORTE, 'Transporte'),
    ]
    STATUS_CHOICES = [
        (PENDENTE, 'Pendente'),
        (ANALISE, 'Em Análise'),
        (AGENDADO, 'Agendado'),
        (CONCLUIDO, 'Concluído'),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="solicitacoes",
        verbose_name="Paciente"
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Solicitação"
    )
    especialidade = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Especialidade"
    )
    descricao = models.TextField(
        verbose_name="Descrição"
    )
    arquivos = models.FileField(
        upload_to='documentos/',
        blank=True,
        null=True,
        verbose_name="Arquivos"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDENTE,
        verbose_name="Status"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.paciente.nome_completo} - {self.tipo}"


class Agendamento(models.Model):
    AGENDADO = 'agendado'
    REALIZADO = 'realizado'
    CANCELADO = 'cancelado'

    STATUS_AGENDAMENTO = [
        (AGENDADO, 'Agendado'),
        (REALIZADO, 'Realizado'),
        (CANCELADO, 'Cancelado'),
    ]

    solicitacao = models.ForeignKey(
        Solicitacao,
        on_delete=models.CASCADE,
        related_name="agendamentos",
        verbose_name="Solicitação"
    )
    data_hora_agendada = models.DateTimeField(
        verbose_name="Data e Hora Agendada"
    )
    local = models.CharField(
        max_length=150,
        verbose_name="Local"
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações"
    )
    status_agendamento = models.CharField(
        max_length=20,
        choices=STATUS_AGENDAMENTO,
        default=AGENDADO,
        verbose_name="Status do Agendamento"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['data_hora_agendada']

    def __str__(self):
        return f"{self.solicitacao} - {self.data_hora_agendada}"