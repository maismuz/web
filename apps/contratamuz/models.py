from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Usuario(models.Model):
    """Model representing users who can be companies or service providers."""
    
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome',
        help_text='Nome completo do usuário ou razão social da empresa'
    )
    eh_empresa = models.BooleanField(
        default=False,
        verbose_name='É Empresa',
        help_text='Marcar se o usuário é uma empresa'
    )
    eh_prestador = models.BooleanField(
        default=False,
        verbose_name='É Prestador de Serviço',
        help_text='Marcar se o usuário é um prestador de serviços'
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Telefone',
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
                message='Digite um número de telefone válido'
            )
        ]
    )
    biografia = models.TextField(
        blank=True,
        verbose_name='Biografia',
        help_text='Descrição sobre o usuário ou empresa'
    )
    imagem = models.ImageField(
        upload_to='usuarios/',
        blank=True,
        null=True,
        verbose_name='Imagem de Perfil'
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['nome']

    def __str__(self):
        tipo = []
        if self.eh_empresa:
            tipo.append('Empresa')
        if self.eh_prestador:
            tipo.append('Prestador')
        tipo_str = f" ({', '.join(tipo)})" if tipo else ""
        return f"{self.nome}{tipo_str}"

    def clean(self):
        """Validate that user is at least company or service provider."""
        if not self.eh_empresa and not self.eh_prestador:
            raise ValidationError(
                'Usuário deve ser pelo menos uma empresa ou prestador de serviços.'
            )


class Servico(models.Model):
    """Model representing services offered by users."""
    
    CATEGORIA_CHOICES = [
        ('tecnologia', 'Tecnologia'),
        ('saude', 'Saúde'),
        ('educacao', 'Educação'),
        ('beleza', 'Beleza e Estética'),
        ('domesticos', 'Serviços Domésticos'),
        ('construcao', 'Construção e Reforma'),
        ('transporte', 'Transporte'),
        ('consultoria', 'Consultoria'),
        ('design', 'Design e Arte'),
        ('outros', 'Outros'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='servicos',
        verbose_name='Usuário'
    )
    titulo = models.CharField(
        max_length=100,
        verbose_name='Título do Serviço'
    )
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição detalhada do serviço oferecido'
    )
    categoria = models.CharField(
        max_length=100,
        choices=CATEGORIA_CHOICES,
        verbose_name='Categoria'
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )
    contato = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Contato',
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
                message='Digite um número de telefone válido'
            )
        ]
    )
    imagem = models.ImageField(
        upload_to='servicos/',
        blank=True,
        null=True,
        verbose_name='Imagem do Serviço'
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Marcar como inativo para ocultar o serviço'
    )

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.titulo} - {self.usuario.nome}"

    @property
    def nota_media(self):
        """Calculate average rating for the service."""
        avaliacoes = self.avaliacoes.all()
        if avaliacoes.exists():
            return round(sum(a.nota for a in avaliacoes) / avaliacoes.count(), 1)
        return None


class VagaEmprego(models.Model):
    """Model representing job vacancies."""
    
    CATEGORIA_CHOICES = [
        ('tecnologia', 'Tecnologia'),
        ('saude', 'Saúde'),
        ('educacao', 'Educação'),
        ('administracao', 'Administração'),
        ('vendas', 'Vendas'),
        ('marketing', 'Marketing'),
        ('recursos_humanos', 'Recursos Humanos'),
        ('financeiro', 'Financeiro'),
        ('operacional', 'Operacional'),
        ('outros', 'Outros'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='vagas',
        verbose_name='Empresa'
    )
    titulo = models.CharField(
        max_length=100,
        verbose_name='Título da Vaga'
    )
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição detalhada da vaga e requisitos'
    )
    salario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Salário',
        validators=[MinValueValidator(0)],
        help_text='Salário oferecido (opcional)'
    )
    localizacao = models.CharField(
        max_length=100,
        verbose_name='Localização'
    )
    categoria = models.CharField(
        max_length=100,
        choices=CATEGORIA_CHOICES,
        verbose_name='Categoria'
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name='Vaga Ativa',
        help_text='Marcar como inativa quando a vaga for preenchida'
    )

    class Meta:
        verbose_name = 'Vaga de Emprego'
        verbose_name_plural = 'Vagas de Emprego'
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.titulo} - {self.usuario.nome}"

    def clean(self):
        """Validate that only companies can post job vacancies."""
        if self.usuario and not self.usuario.eh_empresa:
            raise ValidationError(
                'Apenas empresas podem publicar vagas de emprego.'
            )


class Candidatura(models.Model):
    """Model representing job applications."""
    
    STATUS_CANDIDATURA = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('aceita', 'Aceita'),
        ('rejeitada', 'Rejeitada'),
    ]

    candidato = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='candidaturas',
        verbose_name='Candidato'
    )
    vaga = models.ForeignKey(
        VagaEmprego,
        on_delete=models.CASCADE,
        related_name='candidaturas',
        verbose_name='Vaga'
    )
    mensagem = models.TextField(
        blank=True,
        verbose_name='Mensagem',
        help_text='Mensagem do candidato (opcional)'
    )
    data_candidatura = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data da Candidatura'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CANDIDATURA,
        default='pendente',
        verbose_name='Status'
    )

    class Meta:
        verbose_name = 'Candidatura'
        verbose_name_plural = 'Candidaturas'
        ordering = ['-data_candidatura']
        unique_together = ('candidato', 'vaga')

    def __str__(self):
        return f"{self.candidato.nome} -> {self.vaga.titulo}"

    def clean(self):
        """Validate candidature business rules."""
        if self.candidato and self.candidato.eh_empresa:
            raise ValidationError(
                'Empresas não podem se candidatar a vagas.'
            )
        if self.vaga and not self.vaga.ativa:
            raise ValidationError(
                'Não é possível se candidatar a uma vaga inativa.'
            )


class Avaliacao(models.Model):
    """Model representing service evaluations."""
    
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        verbose_name='Serviço'
    )
    avaliador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='avaliacoes_feitas',
        verbose_name='Avaliador'
    )
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Nota',
        help_text='Nota de 1 a 5 estrelas'
    )
    comentario = models.TextField(
        blank=True,
        verbose_name='Comentário',
        help_text='Comentário sobre o serviço (opcional)'
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data da Avaliação'
    )

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-criado_em']
        unique_together = ('servico', 'avaliador')

    def __str__(self):
        return f"Avaliação de {self.avaliador.nome} para {self.servico.titulo} ({self.nota}★)"

    def clean(self):
        """Validate that user cannot evaluate their own service."""
        if self.servico and self.avaliador and self.servico.usuario == self.avaliador:
            raise ValidationError(
                'Usuário não pode avaliar seu próprio serviço.'
            )