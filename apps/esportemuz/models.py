from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from uuid import uuid4

from .utils import gerar_nome_arquivo


class Modalidade(models.Model):
    """Model representing a sports discipline or category."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name='ID'
    )
    nome = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nome da Modalidade',
        help_text='Nome da modalidade esportiva'
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name='Ativa',
        help_text='Indica se a modalidade está ativa'
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )

    class Meta:
        verbose_name = 'Modalidade'
        verbose_name_plural = 'Modalidades'
        ordering = ['nome']

    def __str__(self):
        return self.nome.replace('_', ' ').title()

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = '_'.join(self.nome.strip().lower().split())
        super().save(*args, **kwargs)


class Equipe(models.Model):
    """Model representing a team that participates in championships."""
    
    def get_path_escudo(instance, filename):
        """Generate file path for team shield."""
        return gerar_nome_arquivo(instance, 'esportemuz/equipes/escudos', filename)

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name='ID'
    )
    nome = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nome da Equipe'
    )
    escudo = models.ImageField(
        upload_to=get_path_escudo,
        blank=True,
        null=True,
        verbose_name='Escudo da Equipe'
    )
    cidade = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Cidade',
        help_text='Cidade da equipe'
    )
    data_fundacao = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Fundação'
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name='Ativa',
        help_text='Indica se a equipe está ativa'
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )

    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'
        ordering = ['nome']

    def __str__(self):
        return self.nome.replace('_', ' ').title()

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = '_'.join(self.nome.strip().lower().split())
        super().save(*args, **kwargs)


class TipoCampeonato(models.Model):
    """Model representing a championship type (e.g., round-robin, knockout)."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name='ID'
    )
    nome = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nome do Tipo',
        help_text='Tipo de campeonato (ex: pontos corridos, mata-mata)'
    )
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Descrição do tipo de campeonato'
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Indica se o tipo está ativo'
    )

    class Meta:
        verbose_name = 'Tipo de Campeonato'
        verbose_name_plural = 'Tipos de Campeonato'
        ordering = ['nome']

    def __str__(self):
        return self.nome.replace('_', ' ').title()

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = '_'.join(self.nome.strip().lower().split())
        super().save(*args, **kwargs)


class LocalPartida(models.Model):
    """Model representing a match venue."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name='ID'
    )
    nome = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nome do Local'
    )
    endereco = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Endereço',
        help_text='Endereço completo do local'
    )
    capacidade = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Capacidade',
        help_text='Capacidade máxima de público'
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Indica se o local está ativo'
    )

    class Meta:
        verbose_name = 'Local da Partida'
        verbose_name_plural = 'Locais das Partidas'
        ordering = ['nome']

    def __str__(self):
        return self.nome.replace('_', ' ').title()

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = '_'.join(self.nome.strip().lower().split())
        super().save(*args, **kwargs)


class Campeonato(models.Model):
    """Model representing a specific championship."""
    
    STATUS_CHOICES = [
        ('nao_iniciado', 'Não Iniciado'),
        ('em_andamento', 'Em Andamento'),
        ('encerrado', 'Encerrado'),
        ('cancelado', 'Cancelado'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name='ID'
    )
    nome = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nome do Campeonato'
    )
    modalidade = models.ForeignKey(
        Modalidade,
        on_delete=models.PROTECT,
        related_name='campeonatos',
        verbose_name='Modalidade'
    )
    tipo_campeonato = models.ForeignKey(
        TipoCampeonato,
        on_delete=models.PROTECT,
        related_name='campeonatos',
        verbose_name='Tipo de Campeonato'
    )
    data_inicio = models.DateField(
        verbose_name='Data de Início'
    )
    data_fim = models.DateField(
        verbose_name='Data de Fim'
    )
    equipes = models.ManyToManyField(
        Equipe,
        through='Classificacao',
        verbose_name='Equipes Participantes'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='nao_iniciado',
        verbose_name='Status'
    )
    premiacao = models.TextField(
        blank=True,
        verbose_name='Premiação',
        help_text='Descrição da premiação do campeonato'
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )

    class Meta:
        verbose_name = 'Campeonato'
        verbose_name_plural = 'Campeonatos'
        ordering = ['-data_inicio']

    def __str__(self):
        return self.nome.replace('_', ' ').title()

    def clean(self):
        """Validate championship dates."""
        if self.data_inicio and self.data_fim:
            if self.data_inicio >= self.data_fim:
                raise ValidationError(
                    'Data de início deve ser anterior à data de fim.'
                )

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = '_'.join(self.nome.strip().lower().split())
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def encerrado(self):
        """Backward compatibility property."""
        return self.status == 'encerrado'

    @property
    def total_equipes(self):
        """Get total number of participating teams."""
        return self.equipes.count()

    @property
    def total_partidas(self):
        """Get total number of matches."""
        return self.partidas.count()


class Partida(models.Model):
    """Model representing a match between two teams in a championship."""
    
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('em_andamento', 'Em Andamento'),
        ('encerrada', 'Encerrada'),
        ('adiada', 'Adiada'),
        ('cancelada', 'Cancelada'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name='ID'
    )
    campeonato = models.ForeignKey(
        Campeonato,
        on_delete=models.CASCADE,
        related_name='partidas',
        verbose_name='Campeonato'
    )
    equipe_mandante = models.ForeignKey(
        Equipe,
        on_delete=models.PROTECT,
        related_name='partidas_mandante',
        verbose_name='Equipe Mandante'
    )
    equipe_visitante = models.ForeignKey(
        Equipe,
        on_delete=models.PROTECT,
        related_name='partidas_visitante',
        verbose_name='Equipe Visitante'
    )
    data_hora = models.DateTimeField(
        verbose_name='Data e Hora da Partida'
    )
    local = models.ForeignKey(
        LocalPartida,
        on_delete=models.PROTECT,
        related_name='partidas',
        verbose_name='Local da Partida'
    )
    gols_mandante = models.PositiveIntegerField(
        default=0,
        verbose_name='Gols da Equipe Mandante'
    )
    gols_visitante = models.PositiveIntegerField(
        default=0,
        verbose_name='Gols da Equipe Visitante'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='agendada',
        verbose_name='Status da Partida'
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações',
        help_text='Observações sobre a partida'
    )

    class Meta:
        verbose_name = 'Partida'
        verbose_name_plural = 'Partidas'
        ordering = ['-data_hora']

    def __str__(self):
        data_str = self.data_hora.strftime('%d/%m/%Y %H:%M') if self.data_hora else 'Data não definida'
        local_str = str(self.local) if self.local else 'Local não definido'
        return f'{self.equipe_mandante} vs {self.equipe_visitante} - {data_str} ({local_str})'

    def clean(self):
        """Validate match business rules."""
        if self.equipe_mandante == self.equipe_visitante:
            raise ValidationError(
                'Uma equipe não pode jogar contra si mesma.'
            )
        
        if self.data_hora and self.data_hora < timezone.now():
            if self.status == 'agendada':
                raise ValidationError(
                    'Partidas agendadas não podem ter data no passado.'
                )

    @property
    def encerrada(self):
        """Backward compatibility property."""
        return self.status == 'encerrada'

    @property
    def resultado(self):
        """Get match result."""
        if self.status != 'encerrada':
            return 'Partida não encerrada'
        
        if self.gols_mandante > self.gols_visitante:
            return f'Vitória {self.equipe_mandante}'
        elif self.gols_visitante > self.gols_mandante:
            return f'Vitória {self.equipe_visitante}'
        else:
            return 'Empate'


class Classificacao(models.Model):
    """Model representing a team's classification in a championship."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        verbose_name='ID'
    )
    campeonato = models.ForeignKey(
        Campeonato,
        on_delete=models.CASCADE,
        related_name='classificacoes',
        verbose_name='Campeonato'
    )
    equipe = models.ForeignKey(
        Equipe,
        on_delete=models.CASCADE,
        related_name='classificacoes',
        verbose_name='Equipe'
    )
    pontos = models.PositiveIntegerField(
        default=0,
        verbose_name='Pontos'
    )
    partidas_jogadas = models.PositiveIntegerField(
        default=0,
        verbose_name='Partidas Jogadas'
    )
    vitorias = models.PositiveIntegerField(
        default=0,
        verbose_name='Vitórias'
    )
    empates = models.PositiveIntegerField(
        default=0,
        verbose_name='Empates'
    )
    derrotas = models.PositiveIntegerField(
        default=0,
        verbose_name='Derrotas'
    )
    gols_pro = models.PositiveIntegerField(
        default=0,
        verbose_name='Gols Pró'
    )
    gols_contra = models.PositiveIntegerField(
        default=0,
        verbose_name='Gols Contra'
    )
    saldo_gols = models.IntegerField(
        default=0,
        verbose_name='Saldo de Gols'
    )

    class Meta:
        verbose_name = 'Classificação'
        verbose_name_plural = 'Classificações'
        ordering = ['-pontos', '-vitorias', '-saldo_gols', '-gols_pro']
        unique_together = ('campeonato', 'equipe')

    def __str__(self):
        return f'{self.equipe} - {self.pontos} pontos ({self.campeonato})'

    def save(self, *args, **kwargs):
        self.saldo_gols = self.gols_pro - self.gols_contra
        super().save(*args, **kwargs)

    def clean(self):
        """Validate classification consistency."""
        if self.partidas_jogadas != (self.vitorias + self.empates + self.derrotas):
            raise ValidationError(
                'Total de partidas deve ser igual à soma de vitórias, empates e derrotas.'
            )

    @property
    def aproveitamento(self):
        """Calculate team performance percentage."""
        if self.partidas_jogadas == 0:
            return 0
        pontos_possiveis = self.partidas_jogadas * 3
        return round((self.pontos / pontos_possiveis) * 100, 1)