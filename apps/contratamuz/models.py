from django.db import models
from django.contrib.auth.models import User

# Criação de modelos de contratos e curriculos para serviços autonomos ou contratação de empreasas;
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    eh_empresa = models.BooleanField(default=False)
    eh_prestador = models.BooleanField(default=False)
    telefone = models.CharField(max_length=15, blank=True)
    biografia = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='usuarios/', blank=True, null=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
class Servico(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='servicos')
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
    
    class Meta:
        verbose_name = 'Vaga de Emprego'
        verbose_name_plural = 'Vagas de Emprego'
    
class Candidatura(models.Model):

    STATUS_CANDIDATURA = [
        ('pendente', 'Pendente'),
        ('aceita', 'Aceita'),
        ('rejeitada', 'Rejeitada'),
    ]

    candidato = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='candidaturas')
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
    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes_feitas')
    nota = models.IntegerField()
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.avaliador.nome} para {self.serviço.titulo}"
    
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'