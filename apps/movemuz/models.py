from django.db import models

class Motorista(models.Model):
    nome = models.CharField("Nome completo", max_length=100)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    telefone = models.CharField("Telefone", max_length=15, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)
    cnh_numero = models.CharField("Número da CNH", max_length=20, unique=True)
    data_nascimento = models.DateField("Data de nascimento")
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Motorista"
        verbose_name_plural = "Motoristas"
        ordering = ['nome']

    def __str__(self):
        return self.nome
