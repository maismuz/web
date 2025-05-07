from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
