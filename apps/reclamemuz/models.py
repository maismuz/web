from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Categoria(models.Model):
    """Model representing complaint categories."""
    
    nome = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nome da Categoria"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição da categoria"
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name="Ativa",
        help_text="Indica se a categoria está ativa"
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Denuncia(models.Model):
    """Model representing urban complaints."""
    
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
        ('transporte', 'Transporte público'),
        ('saude', 'Saúde pública'),
        ('educacao', 'Educação'),
        ('outro', 'Outro'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    titulo = models.CharField(
        max_length=200,
        verbose_name="Título da Denúncia"
    )
    descricao = models.TextField(
        verbose_name="Descrição Detalhada",
        help_text="Descreva detalhadamente o problema"
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='outro',
        verbose_name="Tipo de Denúncia"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="denuncias",
        verbose_name="Categoria"
    )
    prioridade = models.CharField(
        max_length=10,
        choices=PRIORIDADE_CHOICES,
        default='normal',
        verbose_name="Prioridade"
    )
    data_ocorrencia = models.DateTimeField(
        verbose_name="Data e Hora da Ocorrência"
    )
    logradouro_ocorrencia = models.CharField(
        max_length=255,
        verbose_name="Rua/Avenida da Ocorrência"
    )
    bairro_ocorrencia = models.CharField(
        max_length=100,
        verbose_name="Bairro da Ocorrência",
        default="Centro"
    )
    ponto_referencia = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Ponto de Referência",
        help_text="Ponto de referência próximo (opcional)"
    )
    anexo = models.FileField(
        upload_to='denuncias/',
        blank=True,
        null=True,
        verbose_name="Anexar Foto ou Vídeo",
        help_text="Arquivo de imagem ou vídeo (opcional)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status"
    )
    observacoes_internas = models.TextField(
        blank=True,
        verbose_name="Observações Internas",
        help_text="Observações para uso interno da administração"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Denúncia"
        verbose_name_plural = "Denúncias"
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"

    def clean(self):
        """Validate complaint data."""
        if self.data_ocorrencia and self.data_ocorrencia > timezone.now():
            raise ValidationError(
                'Data de ocorrência não pode ser no futuro.'
            )

    @property
    def dias_pendente(self):
        """Calculate days since complaint was created."""
        return (timezone.now().date() - self.data_criacao.date()).days


class Comentario(models.Model):
    """Model representing comments on complaints."""
    
    texto = models.TextField(
        verbose_name="Texto do Comentário"
    )
    data_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data e Hora"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comentarios_denuncias",
        verbose_name="Usuário"
    )
    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name="comentarios",
        verbose_name="Denúncia"
    )
    eh_publico = models.BooleanField(
        default=True,
        verbose_name="Comentário Público",
        help_text="Se marcado, o comentário será visível publicamente"
    )

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-data_hora']

    def __str__(self):
        return f"Comentário de {self.usuario.username} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"


class Midia(models.Model):
    """Model representing media files attached to complaints."""
    
    TIPO_CHOICES = [
        ('imagem', 'Imagem'),
        ('video', 'Vídeo'),
        ('documento', 'Documento'),
    ]

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Mídia"
    )
    arquivo = models.FileField(
        upload_to='denuncias/midias/',
        verbose_name="Arquivo",
        help_text="Arquivo de mídia"
    )
    url_arquivo = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL do Arquivo",
        help_text="URL externa do arquivo (opcional)"
    )
    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name="midias",
        verbose_name="Denúncia"
    )
    descricao = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição da mídia (opcional)"
    )
    data_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Upload"
    )

    class Meta:
        verbose_name = "Mídia"
        verbose_name_plural = "Mídias"
        ordering = ['-data_upload']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.denuncia.titulo}"

    def clean(self):
        """Validate that either file or URL is provided."""
        if not self.arquivo and not self.url_arquivo:
            raise ValidationError(
                'É necessário fornecer um arquivo ou uma URL.'
            )


class Notificacao(models.Model):
    """Model representing notifications sent to users."""
    
    TIPO_CHOICES = [
        ('status_mudou', 'Status da Denúncia Alterado'),
        ('novo_comentario', 'Novo Comentário'),
        ('denuncia_resolvida', 'Denúncia Resolvida'),
        ('lembrete', 'Lembrete'),
        ('outro', 'Outro'),
    ]

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='outro',
        verbose_name="Tipo de Notificação"
    )
    mensagem = models.TextField(
        verbose_name="Mensagem"
    )
    data_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data e Hora"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notificacoes",
        verbose_name="Usuário"
    )
    denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name="notificacoes",
        verbose_name="Denúncia"
    )
    lida = models.BooleanField(
        default=False,
        verbose_name="Lida",
        help_text="Indica se a notificação foi lida"
    )

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ['-data_hora']

    def __str__(self):
        return f"Notificação para {self.usuario.username} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"


class BuscaDenuncia(models.Model):
    """Model representing search queries performed by users."""
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="buscas_denuncias",
        verbose_name="Usuário"
    )
    termo = models.CharField(
        max_length=255,
        verbose_name="Termo de Busca"
    )
    categoria = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Categoria Filtrada",
        help_text="Categoria usada no filtro"
    )
    status = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Status Filtrado",
        help_text="Status usado no filtro"
    )
    tipo = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Tipo Filtrado",
        help_text="Tipo usado no filtro"
    )
    data_inicial = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data Inicial",
        help_text="Data inicial do período filtrado"
    )
    data_final = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data Final",
        help_text="Data final do período filtrado"
    )
    bairro = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Bairro Filtrado"
    )
    data_busca = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Momento da Busca"
    )
    total_resultados = models.PositiveIntegerField(
        default=0,
        verbose_name="Total de Resultados",
        help_text="Número de resultados encontrados"
    )

    class Meta:
        verbose_name = "Busca de Denúncia"
        verbose_name_plural = "Buscas de Denúncias"
        ordering = ['-data_busca']

    def __str__(self):
        return f"Busca por '{self.termo}' em {self.data_busca.strftime('%d/%m/%Y %H:%M')}"

    def clean(self):
        """Validate search date range."""
        if self.data_inicial and self.data_final:
            if self.data_inicial > self.data_final:
                raise ValidationError(
                    'Data inicial deve ser anterior à data final.'
                )
