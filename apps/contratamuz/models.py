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
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='servicos')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    link_contato = models.URLField(blank=True)

    def __str__(self):
        return self.titulo
    
class VagaEmprego(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='vagas')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    localizacao = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo