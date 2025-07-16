from django.db import models
from django.core.validators import RegexValidator, URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Categoria(models.Model):
    """Model representing event categories."""
    
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome da Categoria",
        help_text="Nome da categoria do evento"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição da categoria (opcional)"
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name="Ativa",
        help_text="Indica se a categoria está ativa"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Evento(models.Model):
    """Model representing events."""
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente Aprovação'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('cancelado', 'Cancelado'),
    ]

    nome = models.CharField(
        max_length=200,
        verbose_name="Nome do Evento",
        help_text="Nome ou título do evento"
    )
    data_hora = models.DateTimeField(
        verbose_name="Data e Hora",
        help_text="Data e horário de início do evento"
    )
    data_fim = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data e Hora de Fim",
        help_text="Data e horário de fim do evento (opcional)"
    )
    local = models.CharField(
        max_length=200,
        verbose_name="Local do Evento",
        help_text="Endereço ou nome do local onde será realizado"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada do evento"
    )
    organizador = models.CharField(
        max_length=100,
        verbose_name="Organizador",
        help_text="Nome da pessoa ou empresa organizadora"
    )
    cnpj = models.CharField(
        max_length=18,
        blank=True,
        verbose_name="CNPJ",
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message='CNPJ deve estar no formato 00.000.000/0000-00'
            )
        ],
        help_text="CNPJ da empresa organizadora (opcional)"
    )
    contato = models.CharField(
        max_length=100,
        verbose_name="Contato",
        help_text="Telefone, email ou forma de contato"
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefone",
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
                message='Digite um número de telefone válido'
            )
        ],
        help_text="Número de telefone para contato (opcional)"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail",
        help_text="E-mail para contato (opcional)"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='eventos',
        verbose_name="Categoria"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status"
    )
    rede_social = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Rede Social",
        help_text="Link ou usuário da rede social (Instagram, Facebook, etc.)"
    )
    site = models.URLField(
        blank=True,
        verbose_name="Site",
        help_text="Site oficial do evento (opcional)"
    )
    valor_ingresso = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valor do Ingresso",
        help_text="Valor do ingresso (deixe em branco se for gratuito)"
    )
    capacidade = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Capacidade",
        help_text="Número máximo de participantes (opcional)"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.nome} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    def clean(self):
        """Validate event business rules."""
        if self.data_hora and self.data_fim:
            if self.data_hora >= self.data_fim:
                raise ValidationError(
                    'Data de início deve ser anterior à data de fim.'
                )
        
        if self.data_hora and self.data_hora < timezone.now():
            if self.status == 'pendente':
                raise ValidationError(
                    'Não é possível criar eventos com data no passado.'
                )

    @property
    def aprovado(self):
        """Backward compatibility property."""
        return self.status == 'aprovado'

    @property
    def eh_gratuito(self):
        """Check if event is free."""
        return self.valor_ingresso is None or self.valor_ingresso == 0

    def link_rede_social(self):
        """Generate social media link."""
        if not self.rede_social:
            return None
            
        rede_social = self.rede_social.strip()
        
        # Se já é um link completo
        if rede_social.startswith(('http://', 'https://')):
            return rede_social
            
        # Remove @ se presente
        usuario = rede_social.lstrip('@')
        
        # Detecta tipo de rede social e gera link apropriado
        if 'instagram' in rede_social.lower() or not any(char in rede_social for char in ['.', '/']):
            return f"https://instagram.com/{usuario}"
        elif 'facebook' in rede_social.lower():
            return f"https://facebook.com/{usuario}"
        elif 'twitter' in rede_social.lower():
            return f"https://twitter.com/{usuario}"
        else:
            # Tenta como URL genérica
            try:
                URLValidator()(f"https://{rede_social}")
                return f"https://{rede_social}"
            except ValidationError:
                return f"https://instagram.com/{usuario}"

    @property
    def duracao_horas(self):
        """Calculate event duration in hours."""
        if self.data_fim and self.data_hora:
            delta = self.data_fim - self.data_hora
            return round(delta.total_seconds() / 3600, 1)
        return None


class Midia(models.Model):
    """Model representing event media (photos and videos)."""
    
    TIPOS_MIDIA = [
        ('foto', 'Foto'),
        ('video', 'Vídeo'),
    ]

    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='midias',
        verbose_name="Evento"
    )
    tipo = models.CharField(
        max_length=5,
        choices=TIPOS_MIDIA,
        verbose_name="Tipo de Mídia"
    )
    titulo = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Título",
        help_text="Título ou descrição da mídia (opcional)"
    )
    arquivo = models.FileField(
        upload_to='midias_eventos/',
        blank=True,
        null=True,
        verbose_name="Arquivo",
        help_text="Arquivo de imagem ou vídeo"
    )
    url_video = models.URLField(
        blank=True,
        verbose_name="URL do Vídeo",
        help_text="Link do YouTube, Vimeo ou outro serviço (para vídeos)"
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem",
        help_text="Ordem de exibição da mídia"
    )
    data_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Upload"
    )

    class Meta:
        verbose_name = "Mídia"
        verbose_name_plural = "Mídias"
        ordering = ['evento', 'ordem', 'id']

    def __str__(self):
        titulo = self.titulo or f"{self.get_tipo_display()}"
        return f"{titulo} - {self.evento.nome}"

    def clean(self):
        """Validate media business rules."""
        if self.tipo == 'video':
            if not self.arquivo and not self.url_video:
                raise ValidationError(
                    'Para vídeos, é necessário enviar um arquivo ou informar uma URL.'
                )
        elif self.tipo == 'foto':
            if not self.arquivo:
                raise ValidationError(
                    'Para fotos, é necessário enviar um arquivo.'
                )

    def is_foto(self):
        """Check if media is a photo."""
        return self.tipo == 'foto'

    def is_video(self):
        """Check if media is a video."""
        return self.tipo == 'video'

    @property
    def url_exibicao(self):
        """Get display URL for media."""
        if self.arquivo:
            return self.arquivo.url
        elif self.url_video:
            return self.url_video
        return None