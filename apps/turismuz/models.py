from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Permissao(models.Model):
    """Model representing user permissions."""
    
    TIPO_CHOICES = [
        ('admin', 'Administrador'),
        ('autor', 'Autor'),
        ('comum', 'Comum'),
    ]

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default='comum',
        verbose_name='Tipo de Permissão'
    )
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Descrição das permissões'
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name='Ativa',
        help_text='Indica se a permissão está ativa'
    )

    class Meta:
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'
        ordering = ['tipo']

    def __str__(self):
        return self.get_tipo_display()


class Categorias(models.Model):
    """Model representing categories for establishments and publications."""
    
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nome da Categoria',
        help_text='Nome da categoria'
    )
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Descrição da categoria'
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name='Ativa',
        help_text='Indica se a categoria está ativa'
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Estabelecimento(models.Model):
    """Model representing tourism establishments."""
    
    STATUS_CHOICES = [
        ('em_analise', 'Em Análise'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]

    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Estabelecimento',
        help_text='Nome do estabelecimento'
    )
    categoria = models.ForeignKey(
        Categorias,
        on_delete=models.PROTECT,
        related_name='estabelecimentos',
        verbose_name='Categoria',
        help_text='Categoria do estabelecimento'
    )
    endereco = models.CharField(
        max_length=200,
        verbose_name='Endereço',
        help_text='Endereço completo do estabelecimento'
    )
    contato = models.CharField(
        max_length=100,
        verbose_name='Contato',
        help_text='Telefone, e-mail ou outro contato',
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$|^[\w\.-]+@[\w\.-]+\.\w+$',
                message='Digite um telefone válido ou e-mail'
            )
        ]
    )
    horario_funcionamento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Horário de Funcionamento',
        help_text='Ex: Segunda a Sexta, 8h às 18h'
    )
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Descrição detalhada do estabelecimento'
    )
    imagem = models.ImageField(
        upload_to='estabelecimentos/',
        blank=True,
        null=True,
        verbose_name='Imagem Principal',
        help_text='Imagem principal do estabelecimento'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='em_analise',
        verbose_name='Status'
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Atualização'
    )

    class Meta:
        verbose_name = 'Estabelecimento'
        verbose_name_plural = 'Estabelecimentos'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.categoria.nome}"

    @property
    def aprovado(self):
        """Check if establishment is approved."""
        return self.status == 'aprovado'


class GuiaTuristico(models.Model):
    """Model representing tourism guides."""
    
    NIVEL_DIFICULDADE_CHOICES = [
        ('facil', 'Fácil'),
        ('moderado', 'Moderado'),
        ('dificil', 'Difícil'),
        ('extremo', 'Extremo'),
    ]

    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Guia',
        help_text='Nome do guia de turismo'
    )
    descricao = models.TextField(
        verbose_name='Descrição do Guia',
        help_text='Descrição detalhada do guia de turismo'
    )
    duracao = models.DurationField(
        verbose_name='Duração',
        help_text='Duração estimada do tour'
    )
    nivel_dificuldade = models.CharField(
        max_length=10,
        choices=NIVEL_DIFICULDADE_CHOICES,
        default='facil',
        verbose_name='Nível de Dificuldade'
    )
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Valor',
        help_text='Valor do tour em reais'
    )
    entidade_responsavel = models.CharField(
        max_length=200,
        verbose_name='Entidade Responsável',
        help_text='Empresa ou pessoa responsável pelo tour'
    )
    contato = models.CharField(
        max_length=200,
        verbose_name='Contato',
        help_text='Telefone, email ou outras informações de contato',
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$|^[\w\.-]+@[\w\.-]+\.\w+$',
                message='Digite um telefone válido ou e-mail'
            )
        ]
    )
    imagem = models.ImageField(
        upload_to='guias_turisticos/',
        blank=True,
        null=True,
        verbose_name='Imagem do Guia',
        help_text='Imagem representativa do guia'
    )
    pontos_parada = models.TextField(
        blank=True,
        verbose_name='Pontos de Parada',
        help_text='Lista dos principais pontos de parada do tour'
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Indica se o guia está disponível'
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
    )

    class Meta:
        verbose_name = 'Guia de Turismo'
        verbose_name_plural = 'Guias de Turismo'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - R$ {self.valor}"

    def clean(self):
        """Validate guide data."""
        if self.valor and self.valor < 0:
            raise ValidationError('O valor não pode ser negativo.')


class Publicacao(models.Model):
    """Model representing tourism publications/articles."""
    
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
        ('arquivado', 'Arquivado'),
    ]

    titulo = models.CharField(
        max_length=255,
        verbose_name='Título da Publicação',
        help_text='Título que aparecerá no card de sua publicação'
    )
    texto_noticia = models.TextField(
        verbose_name='Texto da Publicação',
        help_text='Texto completo da publicação'
    )
    resumo = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Resumo',
        help_text='Resumo da publicação para exibição em listas'
    )
    categoria = models.ForeignKey(
        Categorias,
        on_delete=models.PROTECT,
        related_name='publicacoes',
        verbose_name='Categoria',
        help_text='Categoria da publicação'
    )
    imagem_principal = models.ImageField(
        upload_to='publicacoes/',
        blank=True,
        null=True,
        verbose_name='Imagem Principal',
        help_text='Imagem principal da publicação'
    )
    legenda_imagem = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Legenda da Imagem',
        help_text='Legenda da imagem principal'
    )
    autor = models.CharField(
        max_length=100,
        verbose_name='Autor',
        help_text='Nome do autor da publicação'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='rascunho',
        verbose_name='Status'
    )
    data_publicacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Publicação'
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Atualização'
    )
    visualizacoes = models.PositiveIntegerField(
        default=0,
        verbose_name='Visualizações',
        help_text='Número de visualizações da publicação'
    )

    class Meta:
        verbose_name = 'Publicação'
        verbose_name_plural = 'Publicações'
        ordering = ['-data_publicacao']

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

    @property
    def publicado(self):
        """Check if publication is published."""
        return self.status == 'publicado'


class ImagemPublicacao(models.Model):
    """Model representing additional images for publications."""
    
    publicacao = models.ForeignKey(
        Publicacao,
        on_delete=models.CASCADE,
        related_name='imagens_adicionais',
        verbose_name='Publicação'
    )
    imagem = models.ImageField(
        upload_to='publicacoes/galeria/',
        verbose_name='Imagem'
    )
    legenda = models.CharField(
        max_length=255,
        verbose_name='Legenda da Imagem',
        help_text='Descrição da imagem para acessibilidade'
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem',
        help_text='Ordem de exibição da imagem'
    )

    class Meta:
        verbose_name = 'Imagem da Publicação'
        verbose_name_plural = 'Imagens das Publicações'
        ordering = ['publicacao', 'ordem']

    def __str__(self):
        return f"{self.publicacao.titulo} - {self.legenda}"


class Avaliacao(models.Model):
    """Model representing evaluations for establishments or guides."""
    
    TIPO_AVALIACAO_CHOICES = [
        ('estabelecimento', 'Estabelecimento'),
        ('guia_turistico', 'Guia Turístico'),
    ]

    tipo_avaliacao = models.CharField(
        max_length=20,
        choices=TIPO_AVALIACAO_CHOICES,
        verbose_name='Tipo de Avaliação'
    )
    estabelecimento = models.ForeignKey(
        Estabelecimento,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        null=True,
        blank=True,
        verbose_name='Estabelecimento'
    )
    guia_turistico = models.ForeignKey(
        GuiaTuristico,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        null=True,
        blank=True,
        verbose_name='Guia Turístico'
    )
    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Nota',
        help_text='Nota de 1 a 5 estrelas'
    )
    comentario = models.TextField(
        blank=True,
        verbose_name='Comentário',
        help_text='Comentário sobre a experiência'
    )
    usuario = models.CharField(
        max_length=100,
        verbose_name='Nome do Usuário',
        help_text='Nome de quem fez a avaliação'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='E-mail',
        help_text='E-mail do avaliador (opcional)'
    )
    data_avaliacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data da Avaliação'
    )
    aprovada = models.BooleanField(
        default=True,
        verbose_name='Aprovada',
        help_text='Indica se a avaliação foi aprovada para exibição'
    )

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-data_avaliacao']

    def __str__(self):
        objeto = self.estabelecimento or self.guia_turistico
        return f"{self.usuario} - {objeto} - {self.nota}★"

    def clean(self):
        """Validate evaluation data."""
        if self.tipo_avaliacao == 'estabelecimento' and not self.estabelecimento:
            raise ValidationError(
                'Estabelecimento é obrigatório para avaliação de estabelecimento.'
            )
        if self.tipo_avaliacao == 'guia_turistico' and not self.guia_turistico:
            raise ValidationError(
                'Guia turístico é obrigatório para avaliação de guia.'
            )
        if self.estabelecimento and self.guia_turistico:
            raise ValidationError(
                'Não é possível avaliar estabelecimento e guia na mesma avaliação.'
            )

