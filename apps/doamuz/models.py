from django.db import models
from django.core.validators import RegexValidator


class Estado(models.Model):
    """Model representing Brazilian states."""
    
    ESTADOS_CHOICES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]
    
    sigla = models.CharField(
        max_length=2,
        choices=ESTADOS_CHOICES,
        unique=True,
        verbose_name="Estado"
    )

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ['sigla']

    def __str__(self):
        return self.get_sigla_display()


class Cidade(models.Model):
    """Model representing cities."""
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da Cidade"
    )
    estado = models.ForeignKey(
        Estado,
        on_delete=models.PROTECT,
        related_name="cidades",
        verbose_name="Estado"
    )

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
        ordering = ['estado__sigla', 'nome']
        unique_together = ('nome', 'estado')

    def __str__(self):
        return f"{self.nome} - {self.estado.sigla}"


class Categoria(models.Model):
    """Model representing donation categories."""
    
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Tipo de Doação"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição da categoria de doação"
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


class Doacao(models.Model):
    """Model representing donation requests."""
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('atendido', 'Atendido'),
        ('cancelado', 'Cancelado'),
    ]
    
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título da Doação"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descreva o que está sendo solicitado"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="doacoes",
        verbose_name="Categoria"
    )
    quantidade_necessaria = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Quantidade Necessária",
        help_text="Quantidade de itens necessários (opcional)"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    data_limite = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data Limite",
        help_text="Data limite para receber as doações"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status"
    )
    contato = models.CharField(
        max_length=20,
        verbose_name="Contato",
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
                message='Digite um número de telefone válido'
            )
        ]
    )

    class Meta:
        verbose_name = "Doação"
        verbose_name_plural = "Doações"
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo

    @property
    def foi_atendido(self):
        """Backward compatibility property."""
        return self.status == 'atendido'


class Ongs(models.Model):
    """Model representing NGOs."""
    
    nome_organizacao = models.CharField(
        max_length=200,
        verbose_name="Nome da Organização"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição da organização e suas atividades"
    )
    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.PROTECT,
        related_name="ongs",
        verbose_name="Cidade"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ongs",
        verbose_name="Categoria Principal"
    )
    contato = models.CharField(
        max_length=20,
        verbose_name="Telefone de Contato",
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
                message='Digite um número de telefone válido'
            )
        ]
    )
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail"
    )
    horario_funcionamento = models.CharField(
        max_length=100,
        verbose_name="Horário de Funcionamento",
        help_text="Ex: Segunda a Sexta, 8h às 17h"
    )
    endereco = models.CharField(
        max_length=200,
        verbose_name="Endereço"
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
        ]
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name="Ativa",
        help_text="Indica se a ONG está ativa"
    )

    class Meta:
        verbose_name = "ONG"
        verbose_name_plural = "ONGs"
        ordering = ['nome_organizacao']

    def __str__(self):
        return self.nome_organizacao


class Solicitacao(models.Model):
    """Model representing donation requests from individuals or organizations."""
    
    TIPO_SOLICITANTE_CHOICES = [
        ('pessoa', 'Pessoa Física'),
        ('ong', 'ONG'),
    ]
    
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título da Solicitação"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição completa da necessidade"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="solicitacoes",
        verbose_name="Categoria"
    )
    tipo_solicitante = models.CharField(
        max_length=10,
        choices=TIPO_SOLICITANTE_CHOICES,
        verbose_name="Tipo de Solicitante"
    )
    nome_solicitante = models.CharField(
        max_length=200,
        verbose_name="Nome do Solicitante"
    )
    prazo = models.DateField(
        null=True,
        blank=True,
        verbose_name="Prazo",
        help_text="Data limite para receber a doação"
    )
    contato = models.CharField(
        max_length=20,
        verbose_name="Telefone de Contato",
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
                message='Digite um número de telefone válido'
            )
        ]
    )
    imagem = models.ImageField(
        upload_to='solicitacoes/',
        null=True,
        blank=True,
        verbose_name="Imagem",
        help_text="Imagem relacionada à solicitação"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    atendida = models.BooleanField(
        default=False,
        verbose_name="Atendida",
        help_text="Marcar quando a solicitação for atendida"
    )

    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo


class Pessoa(models.Model):
    """Model representing individual donors or recipients."""
    
    nome = models.CharField(
        max_length=200,
        verbose_name="Nome Completo"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pessoas",
        verbose_name="Categoria de Interesse"
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título da necessidade ou oferta"
    )
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada"
    )
    prazo = models.DateField(
        null=True,
        blank=True,
        verbose_name="Prazo",
        help_text="Data limite (se aplicável)"
    )
    imagem = models.ImageField(
        upload_to='pessoas/',
        null=True,
        blank=True,
        verbose_name="Imagem"
    )
    contato = models.CharField(
        max_length=20,
        verbose_name="Telefone de Contato",
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
                message='Digite um número de telefone válido'
            )
        ]
    )
    mostrar_nome = models.BooleanField(
        default=True,
        verbose_name="Mostrar Nome",
        help_text="Marcar para mostrar o nome publicamente"
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ['-data_cadastro']

    def __str__(self):
        if self.mostrar_nome:
            return self.nome
        return "Anônimo"


class Feedback(models.Model):
    """Model representing feedback about donations."""
    
    AVALIACAO_CHOICES = [
        (1, 'Muito Ruim'),
        (2, 'Ruim'),
        (3, 'Regular'),
        (4, 'Bom'),
        (5, 'Excelente'),
    ]
    
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="feedbacks",
        verbose_name="Categoria da Doação"
    )
    mensagem = models.TextField(
        verbose_name="Mensagem",
        help_text="Descreva sua experiência"
    )
    avaliacao = models.IntegerField(
        choices=AVALIACAO_CHOICES,
        verbose_name="Avaliação",
        help_text="Avalie de 1 a 5 estrelas"
    )
    data_comentario = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data do Comentário"
    )
    email_contato = models.EmailField(
        blank=True,
        verbose_name="E-mail para Contato",
        help_text="E-mail para contato (opcional)"
    )

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ['-data_comentario']

    def __str__(self):
        return f"Feedback - {self.categoria.nome} ({self.avaliacao}★)"

    @property
    def tipo_doacao(self):
        """Backward compatibility property."""
        return self.categoria.nome