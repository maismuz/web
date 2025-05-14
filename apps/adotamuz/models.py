from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validar_nome(value):
    if not value.replace(' ', '').isalpha():
        raise ValidationError('O nome deve conter apenas letras e espaços.')
    

class Raca(models.Model):
    
    PORTE_CHOICES = [('pequeno', 'Pequeno'), ('medio', 'Médio'), ('grande', 'Grande')]
    ESPECIE_CHOICES = [('cachorro', 'Cachorro'), ('gato', 'Gato')]

    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    porte = models.CharField(max_length=10, choices=PORTE_CHOICES, default='medio', verbose_name='Porte')
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES, default='cachorro', verbose_name='Espécie')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

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
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do animal',
        help_text='Nome ou apelido do animal.'
    )
    porte = models.CharField(
        max_length=15,
        verbose_name='Porte',
        help_text='Porte físico do animal (pequeno, médio, grande)'
    )
    raca = models.CharField(
        max_length=50, 
        verbose_name='Raça',
        help_text='Raça do animal (opcional).',
        blank=True,
        null=True
    )
    cor = models.CharField(
        max_length=30,
        verbose_name='Cor',
        help_text='Cor predominante do animal'
    )
    localizacao = models.CharField(
        max_length=150,
        verbose_name='Localização',
        help_text='Local onde o animal se encontra.'
    )
    foto = models.ImageField(
        upload_to='animais/fotos',
        verbose_name='Foto do Animal',
        help_text='Foto principal do animal'
    )
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição detalhada do animal',
        blank=True
    )

    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animais'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.porte})"

    def save(self, *args, **kwargs):
        self.nome = self.nome.capitalize()
        self.full_clean()
        super().save(*args, **kwargs)


class Adocao(models.Model):
    nome_animal = models.CharField(
        max_length=100,
        verbose_name='Nome do Animal',
        help_text='Nome ou apelido do animal.'
    )
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Informações sobre o animal, comportamento, cuidados, etc.'
    )
    foto = models.ImageField(
        upload_to='adocoes/fotos/',
        verbose_name='Foto do Animal',
        help_text='Imagem do animal disponível para adoção.'
    )
    contato = models.CharField(
        max_length=20,
        verbose_name='Telefone ou WhatsApp',
        help_text='Número para contato com quem está doando.',
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
        help_text='Marque como falso quando o animal for adotado.'
    )

    class Meta:
        verbose_name = 'Anúncio de Adoção'
        verbose_name_plural = 'Anúncios de Adoção'
        ordering = ['-data_cadastro']

    def __str__(self):
        return f"{self.nome_animal} - {'Disponível' if self.disponivel else 'Adotado'}"

class TipoProcedimento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    animal = models.ForeignKey('adotamuz.Animal', on_delete=models.CASCADE, related_name='tipos_de_procedimentos')
    instituicao_responsavel = models.CharField(max_length=150)
    data = models.DateField()
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Tipo de Procedimento"
        verbose_name_plural = "Tipos de Procedimentos"

    def __str__(self):
        return f"{self.nome} - {self.animal.nome} - {self.data}"

class Procedimento(models.Model):
    tipo = models.ForeignKey(TipoProcedimento, on_delete=models.CASCADE, related_name='procedimentos')

    class Meta:
        verbose_name = "Procedimento"
        verbose_name_plural = "Procedimentos"

    def __str__(self):
        return f"{self.tipo.nome} ({self.tipo.animal.nome})"


class TipoDenuncia(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text='Coloque o tipo de denúncia exemplo: abandono, violência, etc')

    class Meta:
        verbose_name = "Tipo de Denúncia"
        verbose_name_plural = "Tipos de Denúncia"

    def __str__(self):
        return self.nome

class Denuncia(models.Model):
    tipo = models.ForeignKey(TipoDenuncia, on_delete=models.CASCADE, related_name='denuncias')
    data = models.DateField()
    localizacao = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='denuncias_fotos/', blank=True, null=True)
    descricao = models.TextField()

    class Meta:
        verbose_name = "Denúncia"
        verbose_name_plural = "Denúncias"

    def __str__(self):
        return f"{self.tipo.nome} - {self.data}"
