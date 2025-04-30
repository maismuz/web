from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class Mensagem(models.Model):
    STATUS_CHOICES = [
        ('lida', 'Lida'),
        ('nao_lida', 'Não Lida'),
        ('arquivada', 'Arquivada'),
    ]

    remetente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_lida')

    def __str__(self):
        return f"De {self.remetente} para {self.destinatario} em {self.data.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
