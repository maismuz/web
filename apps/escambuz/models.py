from django.db import models

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
    
    class Objeto(models.Model):
        TIPO_CHOICES = (('venda', 'Venda'), ('troca', 'Troca'), ('doacao', 'Doação'), )
        nome = models.CharField(max_length=255)
        descricao = models.TextField()
        preco = models.DecimalField(max_digits=10, decimal_places=2)
        tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
        categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
        usuario = models.ForeignKey(User, on_delete=models.CASCADE)
        estado = models.CharField(max_length=100)
        data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome
