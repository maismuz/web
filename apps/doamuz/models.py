from django.db import models

# Create your models here.
class Categoria(models.Model):
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

class Feedback(models.Model):
        tipo_doação = models.CharField(max_length=100, verbose_name="Qual foi a categoria da doação?")
        mensagem = models.TextField()
        data_do_comentario = models.DateTimeField(auto_now_add=True)
        AVALIACAO_CHOICES = [(1, 'Positivo'),(2, 'Negativo'),]
        avaliacao = models.IntegerField(choices=AVALIACAO_CHOICES, default=2, verbose_name="Avaliação")

        def __str__(self):
            return f"{self.nome}"

        class Meta:
            verbose_name = "Feedback"
            verbose_name_plural = "Feedbacks"
class Cidade(models.Model):
        cidade = models.CharField(max_length=100, verbose_name="Cidade")
        def __str__(self):
            return f"{self.nome}"
        class Meta:
            verbose_name = "Cidade"
            verbose_name_plural = "Cidades"

class Estado(models.Model):
        cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)
        estado = models.CharField(max_length=100, verbose_name="Estado")
        def __str__(self):
            return f"{self.nome}"
        class Meta:
            verbose_name = "Estado"
            verbose_name_plural = "Estados"

