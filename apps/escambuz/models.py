from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Categoria1(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Transacao(models.Model):
    TIPO_CHOICES = [
        ('venda', 'Venda'),
        ('troca', 'Troca'),
        ('doacao', 'Doação'),
        ('outro', 'Outro'),
    ]

    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='outro')
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categoria = models.ForeignKey(Categoria1, on_delete=models.SET_NULL, null=True, blank=True, related_name='transacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transacoes')
    estado = models.CharField(max_length=100)
    data_transacao = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.nome} ({self.tipo})'

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
