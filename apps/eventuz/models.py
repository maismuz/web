from django.db import models

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField(max_length=200)
    data = models.DateField()
    local = models.CharField(max_length=200)
    descricao = models.TextField()
    organizador = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, blank=True, null=True)
    contato = models.CharField(max_length=100)
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT, related_name='eventos')
    aprovado = models.BooleanField(default=False)  # <-- novo campo

    def __str__(self):
        return self.nome

class Midia(models.Model):
    TIPOS_MIDIA = (
        ('foto', 'Foto'),
        ('video', 'Vídeo'),
    )
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='midias')
    tipo = models.CharField(max_length=5, choices=TIPOS_MIDIA)
    arquivo = models.FileField(upload_to='midias_eventos/', blank=True, null=True)
    url_video = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} do evento: {self.evento.nome}"

    def is_foto(self):
        return self.tipo == 'foto'

    def is_video(self):
        return self.tipo == 'video'