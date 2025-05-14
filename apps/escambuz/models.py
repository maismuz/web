from django.db import models
from django.contrib.auth.models import User  
from django.utils import timezone

class AvaliacaoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=3, decimal_places=1)
    comentario = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação para {self.usuario.username} - Nota: {self.nota}"

class Oferta(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateField(default=timezone.now)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"


class DenunciaIrregular(models.Model):
    MOTIVO_CHOICES = [
        ('preco_irregular', 'Preço Irregular'),
        ('produto_nao_existente', 'Produto Não Existente'),
        ('informacao_incorreta', 'Informação Incorreta'),
        ('outro', 'Outro'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('resolvida', 'Resolvida'),
        ('rejeitada', 'Rejeitada'),
    ]

    oferta = models.ForeignKey(Oferta, related_name='denuncias_irregulares', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name='denuncias_irregulares', on_delete=models.CASCADE)
    motivo_da_denuncia = models.CharField(max_length=50, choices=MOTIVO_CHOICES, default='outro')
    descricao = models.TextField(blank=True, null=True, default='Nenhuma descrição fornecida.')
    data_denuncia = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        usuario = getattr(self.usuario, 'username', 'Usuário desconhecido')
        oferta = getattr(self.oferta, 'titulo', 'Oferta desconhecida')
        return f'Denúncia por {usuario} sobre {oferta}'

    class Meta:
        verbose_name = "Denúncia Irregular"
        verbose_name_plural = "Denúncias Irregulares"
    
    def marcar_como_resolvida(self):
        """Método para marcar a denúncia como resolvida."""
        self.status = 'resolvida'
        self.save()

    def marcar_como_rejeitada(self):
        """Método para marcar a denúncia como rejeitada."""
        self.status = 'rejeitada'
        self.save()
