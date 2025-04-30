from django.db import models
from uuid import uuid5

# Create your models here.
class Modalidade(models.Model):
    """
    Representa uma disciplina ou categoria esportiva específica.
    """

    class Meta:
        verbose_name = 'Modalidade'
        verbose_name_plural = 'Modalidades'

    id = models.UUIDField(primary_key=True, default=uuid5, editable=False, verbose_name='ID')
    nome = models.CharField(max_length=255, verbose_name='Nome')

    def __str__(self):
        return self.nome
    
class TipoCampeonato(models.Model):
    """
    Representa um tipo de campeonato, como pontos corridos, mata-mata, etc.
    """

    class Meta:
        verbose_name = 'Tipo de Campeonato'
        verbose_name_plural = 'Tipos de Campeonato'

    id = models.UUIDField(primary_key=True, default=uuid5, editable=False, verbose_name='ID')
    nome = models.CharField(max_length=255, verbose_name='Nome')

    def __str__(self):
        return self.nome
    
class Campeonato(models.Model):
    """
    Representa um campeonato específico, que pode ter várias modalidades e tipos.
    """

    class Meta:
        verbose_name = 'Campeonato'
        verbose_name_plural = 'Campeonatos'

    id = models.UUIDField(primary_key=True, default=uuid5, editable=False, verbose_name='ID')
    nome = models.CharField(max_length=255, verbose_name='Nome')
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE, verbose_name='Modalidade')
    tipo_campeonato = models.ForeignKey(TipoCampeonato, on_delete=models.CASCADE, verbose_name='Tipo de Campeonato')
    data_inicio = models.DateField(verbose_name='Data de Início')
    data_fim = models.DateField(verbose_name='Data de Fim')

    def __str__(self):
        return self.nome