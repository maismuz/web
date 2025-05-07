from django.db import models
from django.core.exceptions import ValidationError


def validar_nome(value):
    if not value.replace(' ', '').isalpha():
        raise ValidationError('O nome deve conter apenas letras e espaços.')


class Raca(models.Model):
    
    PORTE_CHOICES = [('pequeno', 'Pequeno'), ('medio', 'Médio'), ('grande', 'Grande')]
    ESPECIE_CHOICES = [('cachorro', 'Cachorro'), ('gato', 'Gato')]

    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    porte = models.CharField(max_length=10, choices=PORTE_CHOICES, default='medio', verbose_name='Porte')
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES, default='cachorro', verbose_name='Espécie')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        verbose_name = 'Raça'
        verbose_name_plural = 'Raças'
        ordering = ['nome']
        unique_together = ('nome', 'especie')

    def __str__(self):
        return f'{self.nome} ({self.especie})'

    def clean(self):
        if not self.nome:
            raise ValidationError({'nome': 'O nome é obrigatório.'})
        validar_nome(self.nome)

    def save(self, *args, **kwargs):
        self.nome = self.nome.strip().capitalize()
        self.full_clean()
        super().save(*args, **kwargs)
        
