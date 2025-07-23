from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class Cemiterio(models.Model):
    """Model representing cemeteries."""
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Cemitério",
        help_text="Nome oficial do cemitério"
    )
    cidade = models.CharField(
        max_length=100,
        verbose_name="Cidade",
        help_text="Cidade onde o cemitério está localizado"
    )
    endereco = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Endereço",
        help_text="Endereço completo do cemitério"
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefone",
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
                message='Digite um número de telefone válido'
            )
        ]
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )

    class Meta:
        verbose_name = "Cemitério"
        verbose_name_plural = "Cemitérios"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.cidade}"


class AreaCemiterio(models.Model):
    """Model representing cemetery areas."""
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da Área",
        help_text="Nome ou identificação da área"
    )
    cemiterio = models.ForeignKey(
        Cemiterio,
        on_delete=models.PROTECT,
        related_name="areas",
        verbose_name="Cemitério"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição adicional da área"
    )

    class Meta:
        verbose_name = "Área do Cemitério"
        verbose_name_plural = "Áreas do Cemitério"
        ordering = ['cemiterio__nome', 'nome']
        unique_together = ('nome', 'cemiterio')

    def __str__(self):
        return f"{self.nome} - {self.cemiterio.nome}"


class Tumulo(models.Model):
    """Model representing tombs."""
    
    numero = models.CharField(
        max_length=50,
        verbose_name="Número do Túmulo",
        help_text="Número ou identificação do túmulo"
    )
    area = models.ForeignKey(
        AreaCemiterio,
        on_delete=models.PROTECT,
        related_name="tumulos",
        verbose_name="Área"
    )
    tipo = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Tipo de Túmulo",
        help_text="Tipo do túmulo (jazigo, gaveta, etc.)"
    )
    ocupado = models.BooleanField(
        default=False,
        verbose_name="Ocupado",
        help_text="Indica se o túmulo está ocupado"
    )

    class Meta:
        verbose_name = "Túmulo"
        verbose_name_plural = "Túmulos"
        ordering = ['area__cemiterio__nome', 'area__nome', 'numero']
        unique_together = ('numero', 'area')

    def __str__(self):
        return f"Túmulo {self.numero} - {self.area.nome}"


class HorarioVisitacao(models.Model):
    """Model representing visitation schedules."""
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Horário",
        help_text="Descrição do período de visitação"
    )
    cemiterio = models.ForeignKey(
        Cemiterio,
        on_delete=models.PROTECT,
        related_name="horarios_visitacao",
        verbose_name="Cemitério"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Indica se o horário está ativo"
    )

    class Meta:
        verbose_name = "Horário de Visitação"
        verbose_name_plural = "Horários de Visitação"
        ordering = ['cemiterio__nome', 'nome']

    def __str__(self):
        return f"{self.nome} - {self.cemiterio.nome}"


class HoraDiaVisitacao(models.Model):
    """Model representing specific visiting hours and days."""
    
    DIAS_SEMANA = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    
    hora_inicio = models.TimeField(
        verbose_name="Hora de Início",
        help_text="Horário de início da visitação"
    )
    hora_fim = models.TimeField(
        verbose_name="Hora de Fim",
        help_text="Horário de fim da visitação"
    )
    dia = models.CharField(
        max_length=10,
        choices=DIAS_SEMANA,
        verbose_name="Dia da Semana"
    )
    horario_visitacao = models.ForeignKey(
        HorarioVisitacao,
        on_delete=models.PROTECT,
        related_name="horas_dias",
        verbose_name="Horário de Visitação"
    )

    class Meta:
        verbose_name = "Hora e Dia de Visitação"
        verbose_name_plural = "Horas e Dias de Visitação"
        ordering = ['horario_visitacao', 'dia', 'hora_inicio']
        unique_together = ('dia', 'hora_inicio', 'horario_visitacao')

    def __str__(self):
        return f"{self.get_dia_display()} - {self.hora_inicio} às {self.hora_fim}"

    def clean(self):
        """Validate that start time is before end time."""
        if self.hora_inicio and self.hora_fim and self.hora_inicio >= self.hora_fim:
            raise ValidationError(
                'Hora de início deve ser anterior à hora de fim.'
            )


class Pessoa(models.Model):
    """Model representing deceased persons."""
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome Completo",
        help_text="Nome completo da pessoa falecida"
    )
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento"
    )
    data_falecimento = models.DateField(
        verbose_name="Data de Falecimento"
    )
    cemiterio = models.ForeignKey(
        Cemiterio,
        on_delete=models.PROTECT,
        related_name="pessoas",
        verbose_name="Cemitério",
        help_text="Cemitério onde está enterrado(a)"
    )
    tumulo = models.ForeignKey(
        Tumulo,
        on_delete=models.PROTECT,
        related_name="pessoas",
        verbose_name="Túmulo",
        help_text="Túmulo onde está enterrado(a)"
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações",
        help_text="Informações adicionais"
    )

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.data_nascimento} - {self.data_falecimento})"

    def clean(self):
        """Validate business rules."""
        if self.data_nascimento and self.data_falecimento:
            if self.data_nascimento >= self.data_falecimento:
                raise ValidationError(
                    'Data de nascimento deve ser anterior à data de falecimento.'
                )
        
        if self.tumulo and self.cemiterio:
            if self.tumulo.area.cemiterio != self.cemiterio:
                raise ValidationError(
                    'O túmulo deve pertencer ao cemitério selecionado.'
                )

    @property
    def idade_falecimento(self):
        """Calculate age at death."""
        if self.data_nascimento and self.data_falecimento:
            delta = self.data_falecimento - self.data_nascimento
            return delta.days // 365
        return None
