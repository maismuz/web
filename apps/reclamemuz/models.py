from django.db import models
from django.contrib.auth.models import User

#Gerenciar denúncias urbanas
# seu_app/models.py
# Importe o modelo User padrão
from django.utils.translation import gettext_lazy as _

# Se você não vai usar Perfil e Endereco em nenhuma outra parte,
# pode remover as classes e seus validadores.
# Se for usar em outro lugar, pode mantê-los.

class Denuncia(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('resolvido', 'Resolvido'),
        ('recusado', 'Recusado'),
    ]

    TIPO_CHOICES = [
        ('infraestrutura', 'Buracos, calçamento, iluminação'),
        ('seguranca', 'Segurança e ordem pública'),
        ('meio_ambiente', 'Lixo, poluição, desmatamento'),
        ('servicos', 'Problemas com serviços públicos'),
        ('outro', 'Outro'),
    ]
    
    # REMOVIDO: Campo de ForeignKey para o Perfil
    
    # Informações da denúncia
    titulo = models.CharField(max_length=200, verbose_name='Título da Denúncia')
    descricao = models.TextField(verbose_name='Descrição Detalhada')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='outro', verbose_name='Tipo de Denúncia')
    data_ocorrencia = models.DateTimeField(verbose_name='Data e Hora da Ocorrência')
    
    # Local da ocorrência
    logradouro_ocorrencia = models.CharField(max_length=255, verbose_name='Rua/Avenida da Ocorrência')
    bairro_ocorrencia = models.CharField(max_length=100, verbose_name='Bairro da Ocorrência', default='Centro')
    ponto_referencia = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ponto de Referência')

    # Anexos e Status
    anexo = models.FileField(upload_to='denuncias/', blank=True, null=True, verbose_name='Anexar Foto ou Vídeo')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    
    # REMOVIDO: Campo eh_anonima
    
    # Timestamps
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Denúncia'
        verbose_name_plural = 'Denúncias'
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"

#Gerenciar comentários nas denúncias
class Comentario(models.Model):
    texto = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comentário de {self.id_usuario.username} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
    
#Gerenciar Busca e filtros de denúncias
from django.db import models
from django.contrib.auth.models import User

class BuscaDenuncia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    termo = models.CharField("Termo de busca", max_length=255)
    categoria = models.CharField("Categoria filtrada", max_length=20, blank=True, null=True)
    status = models.CharField("Status filtrado", max_length=10, blank=True, null=True)
    data_inicial = models.DateField("Data inicial", blank=True, null=True)
    data_final = models.DateField("Data final", blank=True, null=True)
    bairro = models.CharField("Bairro filtrado", max_length=100, blank=True, null=True)
    data_busca = models.DateTimeField("Momento da busca", auto_now_add=True)

    def __str__(self):
        return f"Busca por '{self.termo}' em {self.data_busca.strftime('%d/%m/%Y %H:%M')}"
    
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Midia(models.Model):
    TIPO_CHOICES = [
        ('imagem', 'Imagem'),
        ('video', 'Vídeo'),
    ]

    id_midia = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    url_arquivo = models.URLField(max_length=500)
    id_denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo.title()} - {self.url_arquivo}"

class Notificacao(models.Model):
    id_notificacao = models.AutoField(primary_key=True)
    mensagem = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE)

    def __str__(self):
        return f"Notificação para {self.id_usuario.username} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
