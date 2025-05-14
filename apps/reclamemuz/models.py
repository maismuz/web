from django.db import models
from django.contrib.auth.models import User

class Denuncia(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('resolvido', 'Resolvido'),
        ('ignorado', 'Ignorado'),
    ]

    CATEGORIA_CHOICES = [
        ('buraco', 'Buraco no Asfalto'),
        ('lixo', 'Lixo'),
        ('iluminacao', 'Iluminação'),
        # Adicione outras categorias conforme necessário
    ]

    id_denuncia = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    endereco = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    data_ocorrencia = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"
