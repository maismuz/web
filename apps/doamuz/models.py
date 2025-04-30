from django.db import models

# Create your models here.
class Categoria(models.Model):
        cidade = models.CharField(max_length=100, verbose_name="Cidade")
        tipo_doação = models.CharField(max_length=100, verbose_name="Tipo de Doação")
        def __str__(self):
            return f"{self.nome}"
        class Meta:
            verbose_name = "Categoria"
            verbose_name_plural = "Categorias"

class Doacao(models.Model):
        titulo = models.CharField(max_length=200)
        descricao = models.TextField(help_text="Descreva o que está sendo solicitado")
        categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
        quantidade_necessaria = models.PositiveIntegerField(null=True, blank=True)
        data_criacao = models.DateTimeField(auto_now_add=True)
        foi_atendido = models.BooleanField(default=False)
        def __str__(self):
            return f"{self.nome}"
        class Meta:
            verbose_name = "Doação"
            verbose_name_plural = "Doações"
