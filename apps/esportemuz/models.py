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