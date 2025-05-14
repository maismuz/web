from django.db import models
from django.contrib.auth.models import User
# models.py
# Criação de modelos de contratos e curriculos para serviços autonomos ou contratação de empreasas;


# models.py

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    data_nascimento = models.DateField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    
class Servico(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    contato = models.CharField(max_length=15, blank=True)
    imagem = models.ImageField(upload_to='servicos/', blank=True, null=True)

    def __str__(self):
        return self.titulo
    
    @property
    def nota_media(self):
        avaliacoes = self.avaliacoes.all()
        if avaliacoes.exists():
            return round(sum([a.nota for a in avaliacoes]) / avaliacoes.count(), 1)
        return None
    
    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
    
class VagaEmprego(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    localizacao = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Vaga de Emprego'
        verbose_name_plural = 'Vagas de Emprego'
    
class Candidatura(models.Model):

    STATUS_CANDIDATURA = [
        ('pendente', 'Pendente'),
        ('aceita', 'Aceita'),
        ('rejeitada', 'Rejeitada'),
    ]
    vaga = models.ForeignKey(VagaEmprego, on_delete=models.CASCADE, related_name='candidaturas')
    mensagem = models.TextField(blank=True)
    data_candidatura = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CANDIDATURA, default='pendente')

    def __str__(self):
        return f"{self.candidato.nome} -> {self.vaga.titulo}"
    
    class Meta:
        verbose_name = 'Candidatura'
        verbose_name_plural = 'Candidaturas'
        
    
class Avaliacao(models.Model):
    serviço = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField()
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.avaliador.nome} para {self.serviço.titulo}"
    
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'