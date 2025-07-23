from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Paciente(models.Model):
    """Model representing patients."""
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    nome_completo = models.CharField(
        max_length=150,
        verbose_name="Nome Completo",
        help_text="Nome completo do paciente"
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$',
                message='CPF deve estar no formato 000.000.000-00 ou conter 11 dígitos'
            )
        ],
        verbose_name="CPF"
    )
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento"
    )
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        verbose_name="Sexo"
    )
    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone",
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
                message='Digite um número de telefone válido'
            )
        ]
    )
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail",
        help_text="E-mail para contato (opcional)"
    )
    endereco = models.TextField(
        verbose_name="Endereço",
        help_text="Endereço completo do paciente"
    )
    historico_medico = models.TextField(
        blank=True,
        verbose_name="Histórico Médico",
        help_text="Histórico médico do paciente"
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações",
        help_text="Observações gerais sobre o paciente"
    )
    consentimento_lgpd = models.BooleanField(
        default=False,
        verbose_name="Consentimento LGPD",
        help_text="Paciente consentiu com o tratamento dos dados pessoais"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Indica se o paciente está ativo no sistema"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['nome_completo']

    def __str__(self):
        return f"{self.nome_completo} - {self.cpf}"

    def clean(self):
        """Validate patient data."""
        if self.data_nascimento and self.data_nascimento > timezone.now().date():
            raise ValidationError(
                'Data de nascimento não pode ser no futuro.'
            )

    @property
    def idade(self):
        """Calculate patient's age."""
        if self.data_nascimento:
            hoje = timezone.now().date()
            idade = hoje.year - self.data_nascimento.year
            if hoje.month < self.data_nascimento.month or (
                hoje.month == self.data_nascimento.month and 
                hoje.day < self.data_nascimento.day
            ):
                idade -= 1
            return idade
        return None


class Solicitacao(models.Model):
    """Model representing health service requests."""
    
    TIPO_CHOICES = [
        ('consulta', 'Consulta Médica'),
        ('cirurgia', 'Cirurgia'),
        ('exame', 'Exame'),
        ('transporte', 'Transporte Médico'),
        ('medicamento', 'Medicamento'),
        ('fisioterapia', 'Fisioterapia'),
        ('outros', 'Outros'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('aprovado', 'Aprovado'),
        ('agendado', 'Agendado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
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
        verbose_name="Especialidade",
        help_text="Especialidade médica (se aplicável)"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada da solicitação"
    )
    justificativa = models.TextField(
        blank=True,
        verbose_name="Justificativa Médica",
        help_text="Justificativa médica para a solicitação"
    )
    prioridade = models.CharField(
        max_length=10,
        choices=PRIORIDADE_CHOICES,
        default='normal',
        verbose_name="Prioridade"
    )
    arquivos = models.FileField(
        upload_to='solicitacoes/documentos/',
        blank=True,
        null=True,
        verbose_name="Documentos",
        help_text="Documentos anexos (receitas, exames, etc.)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status"
    )
    observacoes_internas = models.TextField(
        blank=True,
        verbose_name="Observações Internas",
        help_text="Observações para uso interno da equipe"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.paciente.nome_completo} - {self.get_tipo_display()}"

    @property
    def dias_pendente(self):
        """Calculate days since request was created."""
        return (timezone.now().date() - self.criado_em.date()).days


class Agendamento(models.Model):
    """Model representing scheduled appointments."""
    
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('confirmado', 'Confirmado'),
        ('realizado', 'Realizado'),
        ('falta', 'Falta do Paciente'),
        ('cancelado', 'Cancelado'),
        ('reagendado', 'Reagendado'),
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
    data_hora_fim = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data e Hora de Fim",
        help_text="Data e hora prevista para o fim do atendimento"
    )
    profissional = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Profissional",
        help_text="Nome do profissional responsável"
    )
    local = models.CharField(
        max_length=150,
        verbose_name="Local",
        help_text="Local onde será realizado o atendimento"
    )
    endereco_local = models.TextField(
        blank=True,
        verbose_name="Endereço do Local",
        help_text="Endereço completo do local de atendimento"
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações",
        help_text="Observações sobre o agendamento"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='agendado',
        verbose_name="Status do Agendamento"
    )
    motivo_cancelamento = models.TextField(
        blank=True,
        verbose_name="Motivo do Cancelamento",
        help_text="Motivo em caso de cancelamento"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['data_hora_agendada']

    def __str__(self):
        return f"{self.solicitacao.paciente.nome_completo} - {self.data_hora_agendada.strftime('%d/%m/%Y %H:%M')}"

    def clean(self):
        """Validate appointment data."""
        if self.data_hora_agendada and self.data_hora_agendada < timezone.now():
            if self.status == 'agendado':
                raise ValidationError(
                    'Não é possível agendar para uma data no passado.'
                )
        
        if self.data_hora_fim and self.data_hora_agendada:
            if self.data_hora_fim <= self.data_hora_agendada:
                raise ValidationError(
                    'Data/hora de fim deve ser posterior à data/hora de início.'
                )

    @property
    def duracao_estimada(self):
        """Calculate estimated duration in minutes."""
        if self.data_hora_fim and self.data_hora_agendada:
            delta = self.data_hora_fim - self.data_hora_agendada
            return int(delta.total_seconds() / 60)
        return None

    @property
    def dias_ate_agendamento(self):
        """Calculate days until appointment."""
        if self.data_hora_agendada:
            delta = self.data_hora_agendada.date() - timezone.now().date()
            return delta.days
        return None