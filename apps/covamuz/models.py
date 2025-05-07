from django.db import models

class Cemiterio(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do cemitério")
    cidade = models.CharField(max_length=100, verbose_name="Cidade do cemitério")

    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Cemitério"
        verbose_name_plural = "Cemitérios"

class AreaCemiterio(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do área")
    Cemiterio = models.ForeignKey(Cemiterio)

    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Área do cemitério"
        verbose_name_plural = "Áreas do cemitério"