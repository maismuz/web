from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Categoria(models.Model):
    """Model representing item categories."""
    
    nome = models.CharField(
        max_length=100,
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


class Objeto(models.Model):
    """Model representing items for exchange, sale or donation."""
    
    TIPO_CHOICES = [
        ('venda', 'Venda'),
        ('doacao', 'Doação'),
        ('troca', 'Troca')
    ]
    
    ESTADO_CHOICES = [
        ('novo', 'Novo'),
        ('seminovo', 'Seminovo'),
        ('usado', 'Usado'),
        ('danificado', 'Danificado'),
    ]

    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Item"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada do item"
    )
    imagem = models.ImageField(
        upload_to='objetos/principais/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Preço",
        help_text="Preço do item (obrigatório para vendas)"
    )
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Transação"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="objetos",
        verbose_name="Categoria"
    )
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        verbose_name="Estado do Item"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="objetos",
        verbose_name="Usuário"
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Marcar como inativo quando vendido/doado"
    )

    class Meta:
        verbose_name = "Objeto"
        verbose_name_plural = "Objetos"
        ordering = ['-data_cadastro']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    def clean(self):
        """Validate business rules."""
        if self.tipo == 'venda' and not self.preco:
            raise ValidationError(
                'Preço é obrigatório para itens à venda.'
            )
        if self.tipo == 'doacao' and self.preco and self.preco > 0:
            raise ValidationError(
                'Itens para doação não devem ter preço.'
            )


class FotoObjeto(models.Model):
    """Model representing additional photos of objects."""
    
    objeto = models.ForeignKey(
        Objeto,
        on_delete=models.CASCADE,
        related_name='fotos_adicionais',
        verbose_name="Objeto"
    )
    imagem = models.ImageField(
        upload_to='objetos/adicionais/',
        verbose_name="Imagem Adicional"
    )
    descricao = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Descrição da Foto",
        help_text="Descrição opcional da foto"
    )

    class Meta:
        verbose_name = 'Foto do Objeto'
        verbose_name_plural = 'Fotos dos Objetos'
        ordering = ['objeto', 'id']

    def __str__(self):
        return f"Foto de {self.objeto.nome}"


class Transacao(models.Model):
    """Model representing completed transactions."""
    
    TIPO_CHOICES = [
        ('venda', 'Venda'),
        ('troca', 'Troca'),
        ('doacao', 'Doação'),
        ('outro', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]

    nome = models.CharField(
        max_length=255,
        verbose_name="Nome da Transação"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Detalhes da transação"
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Transação"
    )
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Valor da Transação"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transacoes',
        verbose_name="Categoria"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transacoes',
        verbose_name="Usuário"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status"
    )
    data_transacao = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data da Transação"
    )

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ['-data_transacao']

    def __str__(self):
        return f'{self.nome} ({self.get_tipo_display()})'


class HistoricoTransacao(models.Model):
    """Model representing transaction history."""
    
    STATUS_CHOICES = [
        ('proposta_enviada', 'Proposta Enviada'),
        ('proposta_aceita', 'Proposta Aceita'),
        ('proposta_rejeitada', 'Proposta Rejeitada'),
        ('transacao_concluida', 'Transação Concluída'),
        ('transacao_cancelada', 'Transação Cancelada'),
    ]

    objeto_oferecido = models.ForeignKey(
        Objeto,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ofertas',
        verbose_name="Objeto Oferecido"
    )
    objeto_recebido = models.ForeignKey(
        Objeto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recebidos',
        verbose_name="Objeto Recebido"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="historico_transacoes",
        verbose_name="Usuário"
    )
    data = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data"
    )
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        verbose_name="Status"
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações",
        help_text="Observações sobre a transação"
    )

    class Meta:
        verbose_name = "Histórico de Transação"
        verbose_name_plural = "Histórico de Transações"
        ordering = ['-data']

    def __str__(self):
        return f"{self.usuario.username} - {self.get_status_display()} em {self.data.strftime('%d/%m/%Y')}"


class Mensagem(models.Model):
    """Model representing messages between users."""
    
    STATUS_CHOICES = [
        ('nao_lida', 'Não Lida'),
        ('lida', 'Lida'),
        ('arquivada', 'Arquivada'),
    ]

    remetente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mensagens_enviadas',
        verbose_name="Remetente"
    )
    destinatario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mensagens_recebidas',
        verbose_name="Destinatário"
    )
    assunto = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Assunto",
        help_text="Assunto da mensagem (opcional)"
    )
    mensagem = models.TextField(
        verbose_name="Mensagem"
    )
    data_envio = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Envio"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='nao_lida',
        verbose_name="Status"
    )
    objeto_relacionado = models.ForeignKey(
        Objeto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mensagens",
        verbose_name="Objeto Relacionado",
        help_text="Objeto relacionado à mensagem (opcional)"
    )

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ['-data_envio']

    def __str__(self):
        assunto = self.assunto or "Sem assunto"
        return f"De {self.remetente.username} para {self.destinatario.username}: {assunto}"

    def clean(self):
        """Validate that sender and receiver are different."""
        if self.remetente == self.destinatario:
            raise ValidationError(
                "Remetente e destinatário não podem ser o mesmo usuário."
            )


class AvaliacaoUsuario(models.Model):
    """Model representing user evaluations."""
    
    usuario_avaliado = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="avaliacoes_recebidas",
        verbose_name="Usuário Avaliado"
    )
    usuario_avaliador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="avaliacoes_feitas",
        verbose_name="Usuário Avaliador"
    )
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Nota",
        help_text="Nota de 1 a 5 estrelas"
    )
    comentario = models.TextField(
        blank=True,
        verbose_name="Comentário",
        help_text="Comentário sobre a experiência (opcional)"
    )
    data_avaliacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Avaliação"
    )
    transacao = models.ForeignKey(
        Transacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="avaliacoes",
        verbose_name="Transação Relacionada"
    )

    class Meta:
        verbose_name = "Avaliação de Usuário"
        verbose_name_plural = "Avaliações de Usuários"
        ordering = ['-data_avaliacao']
        unique_together = ('usuario_avaliado', 'usuario_avaliador', 'transacao')

    def __str__(self):
        return f"Avaliação para {self.usuario_avaliado.username} - Nota: {self.nota}★"

    def clean(self):
        """Validate that user cannot evaluate themselves."""
        if self.usuario_avaliado == self.usuario_avaliador:
            raise ValidationError(
                "Usuário não pode avaliar a si mesmo."
            )


class Oferta(models.Model):
    """Model representing special offers."""
    
    titulo = models.CharField(
        max_length=255,
        verbose_name="Título da Oferta"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada da oferta"
    )
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Preço"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    data_validade = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Validade",
        help_text="Data limite da oferta (opcional)"
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name="Oferta Ativa",
        help_text="Marcar como inativa para ocultar a oferta"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="ofertas",
        verbose_name="Categoria"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ofertas",
        verbose_name="Usuário"
    )

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo

    @property
    def esta_valida(self):
        """Check if offer is still valid."""
        if not self.ativa:
            return False
        if self.data_validade:
            return timezone.now().date() <= self.data_validade
        return True