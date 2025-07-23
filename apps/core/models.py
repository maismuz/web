from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
import re
from datetime import date

def validate_cpf(value):
    """Validador personalizado para CPF"""
    cpf = re.sub(r'[^0-9]', '', value)
    
    if len(cpf) != 11:
        raise ValidationError(_('CPF deve conter 11 dígitos.'))
    
    if cpf == cpf[0] * 11:
        raise ValidationError(_('CPF inválido.'))
    
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if digito1 != int(cpf[9]):
        raise ValidationError(_('CPF inválido.'))
    
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if digito2 != int(cpf[10]):
        raise ValidationError(_('CPF inválido.'))

def validate_date_of_birth(value):
    """Validador para data de nascimento"""
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    
    if age < 16:
        raise ValidationError(_('A idade mínima permitida é 16 anos.'))
    
    if age > 120:
        raise ValidationError(_('Data de nascimento inválida.'))

ESTADOS_CHOICES = [
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
    ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
]

# Validators personalizados
telefone_validator = RegexValidator(
    regex=r'^\(\d{2}\) \d{5}-\d{4}$',
    message=_('Formato de telefone inválido. Use o formato: (XX) XXXXX-XXXX.')
)

cep_validator = RegexValidator(
    regex=r'^\d{5}-\d{3}$',
    message=_('Formato de CEP inválido. Use o formato: XXXXX-XXX.')
)

class Endereco(models.Model):
    logradouro = models.CharField(
        max_length=255,
        verbose_name=_('Logradouro'),
        help_text=_('Nome da rua, avenida, etc.')
    )
    numero = models.CharField(
        max_length=20,
        verbose_name=_('Número'),
        help_text=_('Número do endereço')
    )
    complemento = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Complemento'),
        help_text=_('Complemento do endereço.')
    )
    bairro = models.CharField(
        max_length=100,
        verbose_name=_('Bairro'),
        help_text=_('Bairro do endereço.')
    )
    cidade = models.CharField(
        max_length=100,
        verbose_name=_('Cidade'),
        help_text=_('Cidade do endereço.')
    )
    estado = models.CharField(
        max_length=2,
        choices=ESTADOS_CHOICES,
        verbose_name=_('Estado'),
        help_text=_('Estado do endereço.')
    )
    cep = models.CharField(
        max_length=10,
        validators=[cep_validator],
        verbose_name=_('CEP'),
        help_text=_('CEP no formato XXXXX-XXX.')
    )
    perfil = models.ForeignKey(
        'Perfil',
        on_delete=models.CASCADE,
        related_name='enderecos',
        verbose_name=_('Perfil'),
        help_text=_('Perfil associado a este endereço.')
    )

    def clean(self):
        if self.cep:
            cep_numeros = re.sub(r'[^0-9]', '', self.cep)
            if len(cep_numeros) == 8:
                self.cep = f"{cep_numeros[:5]}-{cep_numeros[5:]}"

    class Meta:
        verbose_name = _('Endereço')
        verbose_name_plural = _('Endereços')

class Perfil(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name=_('Usuário')
    )
    foto = models.ImageField(
        upload_to='perfis/',
        blank=True,
        null=True,
        verbose_name=_('Foto de Perfil')
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[telefone_validator],
        verbose_name=_('Telefone')
    )
    data_nascimento = models.DateField(
        blank=True,
        null=True,
        validators=[validate_date_of_birth],
        verbose_name=_('Data de Nascimento')
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[validate_cpf],
        verbose_name=_('CPF')
    )
    rg = models.CharField(
        max_length=20,
        verbose_name=_('RG')
    )
    genero = models.CharField(
        max_length=1,
        choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro'), ('N', 'Prefiro não informar')],
        verbose_name=_('Gênero')
    )
    linkedin = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('LinkedIn'),
        help_text=_('URL do perfil no LinkedIn.')
    )
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Website'),
        help_text=_('URL do website pessoal ou profissional.')
    )
    profissao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Profissão'),
        help_text=_('Profissão atual.')
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Biografia'),
        help_text=_('Breve descrição profissional.')
    )
    data_atualizacao = models.DateTimeField(auto_now=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username
    
    def get_idade(self):
        """Calcula a idade do usuário baseado na data de nascimento."""
        if not self.data_nascimento:
            return None
        
        today = date.today()
        return today.year - self.data_nascimento.year - (
            (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
    
    def clean(self):
        """Valida e normaliza os dados antes de salvar."""
        super().clean()
        
        if self.cpf:
            cpf_numeros = re.sub(r'[^0-9]', '', self.cpf)
            if len(cpf_numeros) == 11:
                self.cpf = f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
        
        if self.telefone:
            telefone_numeros = re.sub(r'[^0-9]', '', self.telefone)
            if len(telefone_numeros) == 11:
                self.telefone = f"({telefone_numeros[:2]}) {telefone_numeros[2:7]}-{telefone_numeros[7:]}"
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('Perfil')
        verbose_name_plural = _('Perfis')
        ordering = ['usuario__username']  
        indexes = [
            models.Index(fields=['cpf']),  
            models.Index(fields=['usuario']),  
        ]

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Cria automaticamente um perfil para cada usuário criado.
    """
    if created:
        Perfil.objects.create(usuario=instance)



