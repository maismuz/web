from django.db import models

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField(max_length=200)
    data_hora = models.DateTimeField()
    local = models.CharField(max_length=200)
    descricao = models.TextField()
    organizador = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    contato = models.CharField(max_length=100)
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT, related_name='eventos')
    aprovado = models.BooleanField(default=False)
    rede_social = models.CharField(max_length=100, blank=True, null=True)  # novo campo

    def __str__(self):
        return self.nome

    def link_rede_social(self):
        if self.rede_social:
            if self.rede_social.startswith("http"):
                return self.rede_social
            else:
                # Gera link do Instagram por padrão (você pode mudar isso para Facebook, etc.)
                return f"https://instagram.com/{self.rede_social.lstrip('@')}"
        return None

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