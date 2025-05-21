from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


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
        ordering = ['-data_envio']
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
