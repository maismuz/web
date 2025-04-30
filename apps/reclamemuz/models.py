from django.db import models
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    """
    Categorias de denúncias urbanas.
    """
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome

class Denuncia(models.Model):
    """
    Denúncia realizada por um cidadão.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('resolvido', 'Resolvido'),
        ('ignorado', 'Ignorado'),
    ]

    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    endereco = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    data_ocorrencia = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    # usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='denuncias')
    data_publicacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Denúncia"
        verbose_name_plural = "Denúncias"
        ordering = ['-data_publicacao']

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    """
    Comentário em uma denúncia.
    """
    texto = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)
    # usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, related_name='comentarios')

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"

    def __str__(self):
        return f"Comentário em {self.denuncia.titulo}"

class Notificacao(models.Model):
    """
    Notificações sobre denúncias seguidas.
    """
    mensagem = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)
    # usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

    def __str__(self):
        return f"Notificação para denúncia {self.denuncia.titulo}"

class Midia(models.Model):
    """
    Mídia anexada à denúncia.
    """
    TIPO_CHOICES = [
        ('imagem', 'Imagem'),
        ('video', 'Vídeo'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    url_arquivo = models.URLField()
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, related_name='midias')

    class Meta:
        verbose_name = "Mídia"
        verbose_name_plural = "Mídias"

    def __str__(self):
        return f"Mídia de {self.denuncia.titulo}"
