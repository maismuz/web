from django.db import models
from django.contrib.auth.models import User  

class AvaliacaoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=3, decimal_places=1)
    comentario = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação para {self.usuario.username} - Nota: {self.nota}"
