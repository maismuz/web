from django.db import models

# Create your models here.
class categoria(models.Model):
        cidade = models.CharField(max_length=100, verbose_name="Cidade")
        tipo_doação = models.CharField(max_length=100, verbose_name="Tipo de Doação")
        def __str__(self):
            return f"{self.nome}"
        class Meta:
            verbose_name = "Categoria"
            verbose_name_plural = "Categorias"
