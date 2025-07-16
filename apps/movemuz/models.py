from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


ESTADOS_BRASIL = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
]


class Motorista_MoveMuz(models.Model):
    """Model representing drivers."""
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome Completo"
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="CPF",
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$',
                message='CPF deve estar no formato 000.000.000-00 ou conter 11 dígitos'
            )
        ]
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
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail"
    )
    cnh_numero = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="Número da CNH",
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='CNH deve conter 11 dígitos'
            )
        ]
    )
    categoria_cnh = models.CharField(
        max_length=5,
        verbose_name="Categoria da CNH",
        help_text="Ex: A, B, C, D, E"
    )
    validade_cnh = models.DateField(
        verbose_name="Validade da CNH"
    )
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento"
    )
    endereco = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Endereço"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )

    class Meta:
        verbose_name = "Motorista"
        verbose_name_plural = "Motoristas"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - CNH: {self.cnh_numero}"

    def clean(self):
        """Validate driver data."""
        if self.data_nascimento and self.data_nascimento > timezone.now().date():
            raise ValidationError(
                'Data de nascimento não pode ser no futuro.'
            )
        
        if self.validade_cnh and self.validade_cnh < timezone.now().date():
            raise ValidationError(
                'CNH vencida. Atualize a validade.'
            )

    @property
    def idade(self):
        """Calculate driver's age."""
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

    @property
    def cnh_valida(self):
        """Check if CNH is valid."""
        return self.validade_cnh >= timezone.now().date()


class Combustivel(models.Model):
    """Model representing fuel types."""
    
    nome = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nome do Combustível"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição do tipo de combustível"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )

    class Meta:
        verbose_name = 'Combustível'
        verbose_name_plural = 'Combustíveis'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class TipoVeiculo(models.Model):
    """Model representing vehicle types."""
    
    nome = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nome do Tipo"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição do tipo de veículo"
    )
    capacidade_padrao = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Capacidade Padrão",
        help_text="Capacidade padrão para este tipo de veículo"
    )

    class Meta:
        verbose_name = 'Tipo de Veículo'
        verbose_name_plural = 'Tipos de Veículos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Local(models.Model):
    """Model representing locations."""
    
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome do Local"
    )
    endereco = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Endereço"
    )
    cidade = models.CharField(
        max_length=100,
        verbose_name="Cidade"
    )
    estado = models.CharField(
        max_length=2,
        choices=ESTADOS_BRASIL,
        verbose_name="Estado"
    )
    cep = models.CharField(
        max_length=9,
        blank=True,
        verbose_name="CEP",
        validators=[
            RegexValidator(
                regex=r'^\d{5}-?\d{3}$',
                message='CEP deve estar no formato 00000-000'
            )
        ]
    )
    coordenadas = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Coordenadas GPS",
        help_text="Coordenadas GPS (opcional)"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"
        ordering = ['estado', 'cidade', 'nome']

    def __str__(self):
        return f"{self.nome} - {self.cidade}/{self.estado}"


class Veiculo(models.Model):
    """Model representing vehicles."""
    
    CONDICAO_CHOICES = [
        ('excelente', 'Excelente'),
        ('bom', 'Bom'),
        ('regular', 'Regular'),
        ('manutencao', 'Em Manutenção'),
        ('inativo', 'Inativo'),
    ]

    modelo = models.CharField(
        max_length=100,
        verbose_name="Modelo"
    )
    marca = models.CharField(
        max_length=50,
        verbose_name="Marca"
    )
    placa = models.CharField(
        max_length=8,
        unique=True,
        verbose_name="Placa",
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$|^[A-Z]{3}[0-9]{4}$',
                message='Placa deve estar no formato ABC1234 ou ABC1D23'
            )
        ]
    )
    cor = models.CharField(
        max_length=30,
        verbose_name="Cor"
    )
    ano_fabricacao = models.IntegerField(
        verbose_name="Ano de Fabricação",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year + 1)
        ]
    )
    ano_modelo = models.IntegerField(
        verbose_name="Ano do Modelo",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year + 1)
        ]
    )
    foto = models.ImageField(
        upload_to='veiculos/',
        blank=True,
        null=True,
        verbose_name="Foto"
    )
    tipo = models.ForeignKey(
        TipoVeiculo,
        on_delete=models.PROTECT,
        related_name='veiculos',
        verbose_name="Tipo"
    )
    combustivel = models.ForeignKey(
        Combustivel,
        on_delete=models.PROTECT,
        related_name='veiculos',
        verbose_name="Combustível"
    )
    capacidade = models.PositiveIntegerField(
        verbose_name="Capacidade",
        help_text="Número de passageiros"
    )
    renavam = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="RENAVAM",
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='RENAVAM deve conter 11 dígitos'
            )
        ]
    )
    chassi = models.CharField(
        max_length=17,
        unique=True,
        verbose_name="Chassi"
    )
    quilometragem = models.PositiveIntegerField(
        default=0,
        verbose_name="Quilometragem"
    )
    condicao_manutencao = models.CharField(
        max_length=15,
        choices=CONDICAO_CHOICES,
        default='bom',
        verbose_name="Condição de Manutenção"
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações"
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['marca', 'modelo']

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"

    @property
    def disponivel(self):
        """Check if vehicle is available."""
        return self.condicao_manutencao in ['excelente', 'bom', 'regular']


class HorarioTransporte(models.Model):
    """Model representing transport schedules."""
    
    DIAS_SEMANA_CHOICES = [
        ('segunda_sexta', 'Segunda a Sexta'),
        ('sabados', 'Sábados'),
        ('domingos', 'Domingos'),
        ('fins_semana', 'Fins de Semana'),
        ('todos_dias', 'Todos os Dias'),
        ('personalizado', 'Personalizado'),
    ]

    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da Linha",
        help_text="Nome identificador da linha de transporte"
    )
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        related_name="horarios",
        verbose_name="Veículo"
    )
    origem = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        related_name="horarios_origem",
        verbose_name="Origem"
    )
    destino = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        related_name="horarios_destino",
        verbose_name="Destino"
    )
    horario_partida = models.TimeField(
        verbose_name="Horário de Partida"
    )
    horario_chegada_previsto = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Horário de Chegada Previsto"
    )
    dias_funcionamento = models.CharField(
        max_length=20,
        choices=DIAS_SEMANA_CHOICES,
        verbose_name="Dias de Funcionamento"
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )

    class Meta:
        verbose_name = "Horário de Transporte"
        verbose_name_plural = "Horários de Transporte"
        ordering = ['origem__nome', 'horario_partida']

    def __str__(self):
        return f"{self.nome}: {self.origem} → {self.destino} ({self.horario_partida.strftime('%H:%M')})"

    def clean(self):
        """Validate schedule data."""
        if self.horario_chegada_previsto and self.horario_partida:
            if self.horario_chegada_previsto <= self.horario_partida:
                raise ValidationError(
                    'Horário de chegada deve ser posterior ao horário de partida.'
                )


class Ponto(models.Model):
    """Model representing boarding/alighting points."""
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Ponto"
    )
    endereco = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Endereço",
        help_text="Endereço ou descrição da localização"
    )
    local = models.ForeignKey(
        Local,
        on_delete=models.PROTECT,
        related_name="pontos",
        verbose_name="Local"
    )
    coordenadas = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Coordenadas GPS"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )

    class Meta:
        verbose_name = "Ponto de Embarque/Desembarque"
        verbose_name_plural = "Pontos de Embarque/Desembarque"
        ordering = ['local__nome', 'nome']

    def __str__(self):
        return f"{self.nome} - {self.local.cidade}"


class Parada(models.Model):
    """Model representing stops in transport routes."""
    
    horario_transporte = models.ForeignKey(
        HorarioTransporte,
        on_delete=models.CASCADE,
        related_name='paradas',
        verbose_name="Horário de Transporte"
    )
    ponto = models.ForeignKey(
        Ponto,
        on_delete=models.CASCADE,
        related_name="paradas",
        verbose_name="Ponto"
    )
    horario = models.TimeField(
        verbose_name="Horário da Parada"
    )
    ordem = models.PositiveIntegerField(
        verbose_name="Ordem",
        help_text="Ordem da parada na rota"
    )
    tempo_parada = models.PositiveIntegerField(
        default=2,
        verbose_name="Tempo de Parada (minutos)"
    )
    passageiros_estimados = models.PositiveIntegerField(
        default=0,
        verbose_name="Passageiros Estimados"
    )

    class Meta:
        verbose_name = "Parada"
        verbose_name_plural = "Paradas"
        ordering = ['horario_transporte', 'ordem']
        unique_together = ('horario_transporte', 'ordem')

    def __str__(self):
        return f"{self.ponto} às {self.horario} - {self.passageiros_estimados} passageiros"


class Viagem(models.Model):
    """Model representing trips."""
    
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]

    horario_transporte = models.ForeignKey(
        HorarioTransporte,
        on_delete=models.PROTECT,
        related_name="viagens",
        verbose_name="Horário de Transporte"
    )
    motorista = models.ForeignKey(
        Motorista_MoveMuz,
        on_delete=models.PROTECT,
        related_name="viagens",
        verbose_name="Motorista"
    )
    data_viagem = models.DateField(
        verbose_name="Data da Viagem"
    )
    horario_saida_real = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Horário de Saída Real"
    )
    horario_chegada_real = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Horário de Chegada Real"
    )
    passageiros_transportados = models.PositiveIntegerField(
        default=0,
        verbose_name="Passageiros Transportados"
    )
    quilometragem_inicial = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Quilometragem Inicial"
    )
    quilometragem_final = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Quilometragem Final"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='agendada',
        verbose_name="Status"
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )

    class Meta:
        verbose_name = "Viagem"
        verbose_name_plural = "Viagens"
        ordering = ['-data_viagem', '-horario_transporte__horario_partida']
        unique_together = ('horario_transporte', 'data_viagem')

    def __str__(self):
        return f"{self.horario_transporte.nome} - {self.data_viagem} ({self.motorista.nome})"

    @property
    def quilometragem_percorrida(self):
        """Calculate distance traveled."""
        if self.quilometragem_inicial and self.quilometragem_final:
            return self.quilometragem_final - self.quilometragem_inicial
        return None


class Passageiro(models.Model):
    """Model representing passengers."""
    
    viagem = models.ForeignKey(
        Viagem,
        on_delete=models.CASCADE,
        related_name='passageiros',
        verbose_name="Viagem"
    )
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Passageiro"
    )
    documento = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Documento de Identificação",
        help_text="CPF, RG ou outro documento"
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
    ponto_embarque = models.ForeignKey(
        Ponto,
        on_delete=models.PROTECT,
        related_name="embarques",
        verbose_name="Ponto de Embarque"
    )
    ponto_desembarque = models.ForeignKey(
        Ponto,
        on_delete=models.PROTECT,
        related_name="desembarques",
        verbose_name="Ponto de Desembarque"
    )
    observacao = models.TextField(
        blank=True,
        verbose_name="Observação"
    )

    class Meta:
        verbose_name = "Passageiro"
        verbose_name_plural = "Passageiros"
        ordering = ['viagem', 'nome']

    def __str__(self):
        return f"{self.nome} ({self.viagem.data_viagem})"


class EscalaVeiculo(models.Model):
    """Model representing vehicle schedules."""
    
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        related_name="escalas",
        verbose_name="Veículo"
    )
    motorista = models.ForeignKey(
        Motorista_MoveMuz,
        on_delete=models.PROTECT,
        related_name="escalas",
        verbose_name="Motorista"
    )
    data_inicio = models.DateField(
        verbose_name="Data de Início"
    )
    data_fim = models.DateField(
        verbose_name="Data de Fim"
    )
    turno = models.CharField(
        max_length=10,
        choices=[
            ('manha', 'Manhã'),
            ('tarde', 'Tarde'),
            ('noite', 'Noite'),
            ('integral', 'Integral'),
        ],
        verbose_name="Turno"
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações"
    )

    class Meta:
        verbose_name = "Escala do Veículo"
        verbose_name_plural = "Escalas dos Veículos"
        ordering = ['-data_inicio']

    def __str__(self):
        return f"{self.veiculo} - {self.motorista} ({self.data_inicio} a {self.data_fim})"

    def clean(self):
        """Validate schedule dates."""
        if self.data_inicio and self.data_fim:
            if self.data_inicio > self.data_fim:
                raise ValidationError(
                    'Data de início deve ser anterior à data de fim.'
                )


class OcupacaoVeiculo(models.Model):
    """Model representing vehicle occupancy."""
    
    viagem = models.OneToOneField(
        Viagem,
        on_delete=models.CASCADE,
        related_name="ocupacao",
        verbose_name="Viagem"
    )
    passageiros_confirmados = models.PositiveIntegerField(
        default=0,
        verbose_name="Passageiros Confirmados"
    )
    passageiros_em_espera = models.PositiveIntegerField(
        default=0,
        verbose_name="Passageiros em Lista de Espera"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Ocupação do Veículo"
        verbose_name_plural = "Ocupações dos Veículos"
        ordering = ['-atualizado_em']

    def __str__(self):
        return f"{self.viagem} - {self.passageiros_confirmados}/{self.viagem.horario_transporte.veiculo.capacidade} passageiros"

    @property
    def taxa_ocupacao(self):
        """Calculate occupancy rate."""
        capacidade = self.viagem.horario_transporte.veiculo.capacidade
        if capacidade > 0:
            return round((self.passageiros_confirmados / capacidade) * 100, 1)
        return 0

    @property
    def vagas_disponiveis(self):
        """Calculate available seats."""
        capacidade = self.viagem.horario_transporte.veiculo.capacidade
        return max(0, capacidade - self.passageiros_confirmados)