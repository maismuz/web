from django.db import models
from uuid import uuid4

# Create your models here.
class Modalidade(models.Model):
    """
    Representa uma disciplina ou categoria esportiva específica.
    """

    class Meta:
        verbose_name = 'Modalidade'
        verbose_name_plural = 'Modalidades'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='ID')
    nome = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.nome
    
class TipoCampeonato(models.Model):
    """
    Representa um tipo de campeonato, como pontos corridos, mata-mata, etc.
    """

    class Meta:
        verbose_name = 'Tipo de Campeonato'
        verbose_name_plural = 'Tipos de Campeonato'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='ID')
    nome = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.nome
    
class Campeonato(models.Model):
    """
    Representa um campeonato específico, que pode ter várias modalidades e tipos.
    """

    class Meta:
        verbose_name = 'Campeonato'
        verbose_name_plural = 'Campeonatos'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='ID')
    nome = models.CharField(max_length=255, verbose_name='Nome')
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE, verbose_name='Modalidade')
    tipo_campeonato = models.ForeignKey(TipoCampeonato, on_delete=models.CASCADE, verbose_name='Tipo de Campeonato')
    data_inicio = models.DateField(verbose_name='Data de Início')
    data_fim = models.DateField(verbose_name='Data de Fim')

    def __str__(self):
        return self.nome
    
class Equipe(models.Model):
    """
    Representa uma equipe que participa de um campeonato.
    """

    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='ID')
    nome = models.CharField(max_length=255, verbose_name='Nome')
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name='equipes', verbose_name='Campeonato')

    def __str__(self):
        return self.nome
    
class Grupo(models.Model):
    """
    Representa um grupo dentro de um campeonato, onde as equipes competem entre si.
    """

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='ID')
    nome = models.CharField(max_length=255, verbose_name='Nome')
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name='grupos', verbose_name='Campeonato')
    equipes = models.ManyToManyField(Equipe, related_name='grupos', blank=True, verbose_name='Equipes')

    def __str__(self):
        return self.nome
    
class StatusPartida(models.Model):
    """
    Representa o status de uma partida, como agendada, em andamento ou finalizada.
    """

    class Meta:
        verbose_name = 'Status da Partida'
        verbose_name_plural = 'Status das Partidas'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='ID')
    nome = models.CharField(max_length=255, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.nome
    
class Partida(models.Model):
    """
    Representa uma partida entre duas equipes em um campeonato.
    """

    class Meta:
        verbose_name = 'Partida'
        verbose_name_plural = 'Partidas'

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='ID')
    campeonato = models.ForeignKey(Campeonato, on_delete=models.SET_NULL, related_name='partidas', null=True, blank=True, verbose_name='Campeonato')
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, related_name='partidas', null=True, blank=True, verbose_name='Grupo')
    equipe_mandante = models.ForeignKey(Equipe, on_delete=models.SET_NULL, related_name='partidas_mandante', null=True, blank=True, verbose_name='Equipe Mandante')
    equipe_visitante = models.ForeignKey(Equipe, on_delete=models.SET_NULL, related_name='partidas_visitante', null=True, blank=True, verbose_name='Equipe Visitante')
    data_hora = models.DateTimeField(verbose_name='Data e Hora')
    local = models.CharField(max_length=255, verbose_name='Local')
    gols_mandante = models.PositiveIntegerField(default=0, verbose_name='Gols Mandante')
    gols_visitante = models.PositiveIntegerField(default=0, verbose_name='Gols Visitante')
    status = models.ForeignKey(StatusPartida, on_delete=models.PROTECT, related_name='partidas', verbose_name='Status')

    def __str__(self):
        return f'{self.equipe_mandante} vs {self.equipe_visitante} - {self.data_hora.strftime("%d/%m/%Y %H:%M")}'
    
class Classificacao(models.Model):
    """
    Representa a classificação de uma equipe em um campeonato.
    """

    class Meta:
        verbose_name = 'Classificação'
        verbose_name_plural = 'Classificações'
        ordering = ['-pontos', '-vitorias', '-saldo_gols', '-gols_pro']
        unique_together = ('campeonato', 'equipe')

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='ID')
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name='classificacoes', verbose_name='Campeonato')
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='classificacoes', verbose_name='Equipe')
    pontos = models.PositiveIntegerField(default=0, verbose_name='Pontos')
    vitorias = models.PositiveIntegerField(default=0, verbose_name='Vitórias')
    empates = models.PositiveIntegerField(default=0, verbose_name='Empates')
    derrotas = models.PositiveIntegerField(default=0, verbose_name='Derrotas')
    gols_pro = models.PositiveIntegerField(default=0, verbose_name='Gols Pró')
    gols_contra = models.PositiveIntegerField(default=0, verbose_name='Gols Contra')
    saldo_gols = models.IntegerField(default=0, verbose_name='Saldo de Gols')

    def __str__(self):
        return f'{self.equipe} - {self.pontos} pontos'