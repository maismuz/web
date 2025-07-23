from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validar_nome(value):
    """Validate that name contains only letters and spaces."""
    if not value.replace(' ', '').isalpha():
        raise ValidationError('O nome deve conter apenas letras e espaços.')


class Raca(models.Model):
    """Model representing animal breeds."""
    
    PORTE_CHOICES = [
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande')
    ]
    ESPECIE_CHOICES = [
        ('cachorro', 'Cachorro'),
        ('gato', 'Gato')
    ]

    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nome',
        validators=[validar_nome]
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    porte = models.CharField(
        max_length=10,
        choices=PORTE_CHOICES,
        default='medio',
        verbose_name='Porte'
    )
    especie = models.CharField(
        max_length=10,
        choices=ESPECIE_CHOICES,
        default='cachorro',
        verbose_name='Espécie'
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
    )

    class Meta:
        verbose_name = 'Raça'
        verbose_name_plural = 'Raças'
        ordering = ['nome']
        unique_together = ('nome', 'especie')

    def __str__(self):
        return f'{self.nome} ({self.especie})'

    def save(self, *args, **kwargs):
        self.nome = self.nome.strip().capitalize()
        self.full_clean()
        super().save(*args, **kwargs)


class Animal(models.Model):
    """Model representing animals."""
    
    PORTE_CHOICES = [
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande')
    ]

    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do animal',
        help_text='Nome ou apelido do animal (se houver)',
        validators=[validar_nome]
    )
    porte = models.CharField(
        max_length=15,
        choices=PORTE_CHOICES,
        verbose_name='Porte',
        help_text='Porte físico do animal'
    )
    raca = models.ForeignKey(
        Raca,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Raça',
        help_text='Raça do animal (opcional)'
    )
    cor = models.CharField(
        max_length=30,
        verbose_name='Cor',
        help_text='Cor predominante do animal'
    )
    localizacao = models.CharField(
        max_length=150,
        verbose_name='Localização',
        help_text='Local onde o animal se encontra'
    )
    foto = models.ImageField(
        upload_to='animais/fotos/',
        verbose_name='Foto do Animal',
        help_text='Foto principal do animal'
    )
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Descrição detalhada do animal'
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
    )

    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animais'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.porte})"

    def save(self, *args, **kwargs):
        self.nome = self.nome.strip().capitalize()
        self.full_clean()
        super().save(*args, **kwargs)


class Adocao(models.Model):
    """Model representing adoption announcements."""
    
    nome_animal = models.CharField(
        max_length=100,
        verbose_name='Nome do Animal',
        help_text='Nome ou apelido do animal',
        validators=[validar_nome]
    )
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Informações sobre o animal, comportamento, cuidados, etc.'
    )
    foto = models.ImageField(
        upload_to='adocoes/fotos/',
        verbose_name='Foto do Animal',
        help_text='Imagem do animal disponível para adoção'
    )
    contato = models.CharField(
        max_length=20,
        verbose_name='Telefone ou WhatsApp',
        help_text='Número para contato com quem está doando',
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
                message='Digite um número de telefone válido.'
            )
        ]
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Cadastro'
    )
    disponivel = models.BooleanField(
        default=True,
        verbose_name='Disponível para Adoção',
        help_text='Marque como falso quando o animal for adotado'
    )

    class Meta:
        verbose_name = 'Anúncio de Adoção'
        verbose_name_plural = 'Anúncios de Adoção'
        ordering = ['-data_cadastro']

    def __str__(self):
        status = 'Disponível' if self.disponivel else 'Adotado'
        return f"{self.nome_animal} - {status}"


class InstituicaoParceira(models.Model):
    """Model representing partner institutions."""
    
    nome = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Nome da Instituição'
    )
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message='CNPJ deve estar no formato 00.000.000/0000-00'
            )
        ],
        verbose_name='CNPJ'
    )
    endereco = models.CharField(
        max_length=255,
        verbose_name='Endereço'
    )
    servicos_ofertados = models.TextField(
        verbose_name='Serviços Ofertados'
    )
    telefone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
                message='Digite um número de telefone válido'
            )
        ],
        verbose_name='Telefone'
    )

    class Meta:
        verbose_name = "Instituição Parceira"
        verbose_name_plural = "Instituições Parceiras"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class TipoProcedimento(models.Model):
    """Model representing types of procedures."""
    
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nome do Procedimento'
    )
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='tipos_procedimentos',
        verbose_name='Animal'
    )
    instituicao_responsavel = models.ForeignKey(
        InstituicaoParceira,
        on_delete=models.CASCADE,
        verbose_name='Instituição Responsável'
    )
    data = models.DateField(verbose_name='Data')
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações'
    )

    class Meta:
        verbose_name = "Tipo de Procedimento"
        verbose_name_plural = "Tipos de Procedimentos"
        ordering = ['-data']

    def __str__(self):
        return f"{self.nome} - {self.animal.nome} - {self.data}"


class Procedimento(models.Model):
    """Model representing procedures."""
    
    tipo = models.ForeignKey(
        TipoProcedimento,
        on_delete=models.CASCADE,
        related_name='procedimentos',
        verbose_name='Tipo de Procedimento'
    )

    class Meta:
        verbose_name = "Procedimento"
        verbose_name_plural = "Procedimentos"

    def __str__(self):
        return f"{self.tipo.nome} ({self.tipo.animal.nome})"


class TipoDenuncia(models.Model):
    """Model representing types of complaints."""
    
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nome',
        help_text='Tipo de denúncia (ex: abandono, violência, etc.)'
    )

    class Meta:
        verbose_name = "Tipo de Denúncia"
        verbose_name_plural = "Tipos de Denúncia"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Denuncia(models.Model):
    """Model representing complaints."""
    
    tipo = models.ForeignKey(
        TipoDenuncia,
        on_delete=models.CASCADE,
        related_name='denuncias',
        verbose_name='Tipo'
    )
    data = models.DateField(verbose_name='Data')
    localizacao = models.CharField(
        max_length=255,
        verbose_name='Localização'
    )
    foto = models.ImageField(
        upload_to='denuncias/fotos/',
        blank=True,
        null=True,
        verbose_name='Foto'
    )
    descricao = models.TextField(verbose_name='Descrição')

    class Meta:
        verbose_name = "Denúncia"
        verbose_name_plural = "Denúncias"
        ordering = ['-data']

    def __str__(self):
        return f"{self.tipo.nome} - {self.data}"


class Evento(models.Model):
    """Model representing events."""
    
    nome = models.CharField(
        max_length=200,
        verbose_name="Nome do Evento"
    )
    data = models.DateField(verbose_name="Data do Evento")
    hora = models.TimeField(verbose_name="Hora do Evento")
    local = models.CharField(
        max_length=255,
        verbose_name="Local"
    )
    organizador = models.CharField(
        max_length=150,
        verbose_name="Organizador"
    )

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['data', 'hora']

    def __str__(self):
        return f"{self.nome} - {self.data.strftime('%d/%m/%Y')} às {self.hora.strftime('%H:%M')}"
