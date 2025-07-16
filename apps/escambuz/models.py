from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Objeto(models.Model):
    TIPO_CHOICES = [
        ('venda', 'Venda'),
        ('doacao', 'Doação'),
        ('troca', 'Troca')
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='objetos_imgs/', blank=True, null=True) 
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(choices=TIPO_CHOICES, max_length=10)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class FotoObjeto(models.Model):
    objeto = models.ForeignKey(Objeto, related_name='fotos', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='objetos/', blank=True, null=True)
    def __str__(self):
        return f"Foto de {self.objeto.nome}"

    class Meta:
        verbose_name = 'Foto do Objeto'
        verbose_name_plural = 'Fotos dos Objetos'


class Transacao(models.Model):
    TIPO_CHOICES = [
        ('venda', 'Venda'),
        ('troca', 'Troca'),
        ('doacao', 'Doação'),
        ('outro', 'Outro'),
    ]

    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='outro')
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='transacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transacoes')
    estado = models.CharField(max_length=100)
    data_transacao = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.nome} ({self.tipo})'

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

class HistoricoTransacao(models.Model):
    objeto_oferecido = models.ForeignKey(Objeto, on_delete=models.SET_NULL, null=True, related_name='ofertas')
    objeto_recebido = models.ForeignKey(Objeto, on_delete=models.SET_NULL, null=True, related_name='recebidos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.usuario.username} - {self.status} em {self.data}"

class Mensagem(models.Model):
    STATUS_CHOICES = [
        ('nao_lida', 'Não Lida'),
        ('lida', 'Lida'),
        ('arquivada', 'Arquivada'),
    ]

    remetente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mensagens_enviadas'
    )
    destinatario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mensagens_recebidas'
    )
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='nao_lida'
    )

    def clean(self):
        if self.remetente == self.destinatario:
            raise ValidationError("Remetente e destinatário não podem ser o mesmo usuário.")

    def __str__(self):
        return f"De {self.remetente.username} para {self.destinatario.username} em {self.data_envio.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ['data_envio'] 
        db_table = 'mensagens_usuarios'

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