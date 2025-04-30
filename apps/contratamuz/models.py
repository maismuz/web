from django.db import models
from django.contrib.auth.models import User

# Criação de modelos de contratos e curriculos para serviços autonomos ou contratação de empreasas;

class Usuario(models.Model):
    eh_empresa = models.BooleanField(default=False)
    eh_prestador = models.BooleanField(default=False)
    telefone = models.CharField(max_length=15, blank=True)
    biografia = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
class Servico(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    link_contato = models.URLField(blank=True)

    def __str__(self):
        return self.titulo