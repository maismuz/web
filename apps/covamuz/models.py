from django.db import models

class Cemiterio(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do cemitério")
    
    def __str__(self):
        return f"{self.nome}, {self.uf}"
    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
