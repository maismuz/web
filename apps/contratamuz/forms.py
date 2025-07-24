from django import forms
from .models import Usuario, Servico, VagaEmprego


class UsuarioForm(forms.ModelForm):
    """Formulário para criação e edição de usuários"""
    
    class Meta:
        model = Usuario
        fields = ['nome', 'cidade', 'telefone', 'biografia', 'imagem', 'eh_empresa', 'eh_prestador']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu nome completo'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua cidade'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Conte um pouco sobre você e seus serviços...'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'eh_empresa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'eh_prestador': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ServicoForm(forms.ModelForm):
    """Formulário para criação e edição de serviços"""
    
    class Meta:
        model = Servico
        fields = ['titulo', 'descricao', 'categoria', 'contato', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Aulas de Violão para Iniciantes'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descreva detalhadamente seu serviço, experiência e diferenciais...'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'contato': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes CSS e placeholder personalizados
        for field_name, field in self.fields.items():
            if field_name == 'categoria':
                field.empty_label = "Selecione uma categoria"



# Formulários de Autenticação

class LoginForm(forms.Form):
    """Formulário para login de usuários"""
    username = forms.CharField(
        label='Usuário',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome de usuário',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )


class RegisterForm(forms.Form):
    """Formulário para registro de novos usuários"""
    
    # Dados do usuário Django
    username = forms.CharField(
        label='Nome de usuário',
        max_length=150,
        help_text='Apenas letras, números e @/./+/-/_ são permitidos.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escolha um nome de usuário único'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com'
        })
    )
    first_name = forms.CharField(
        label='Primeiro nome',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu primeiro nome'
        })
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu sobrenome'
        })
    )
    password = forms.CharField(
        label='Senha',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 6 caracteres'
        })
    )
    password_confirm = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a senha novamente'
        })
    )
    
    # Dados do perfil
    nome = forms.CharField(
        label='Nome completo',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome completo'
        })
    )
    cidade = forms.CharField(
        label='Cidade',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sua cidade'
        })
    )
    telefone = forms.CharField(
        label='Telefone',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999'
        })
    )
    biografia = forms.CharField(
        label='Biografia',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Conte um pouco sobre você...'
        })
    )
    eh_empresa = forms.BooleanField(
        label='Sou uma empresa',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    eh_prestador = forms.BooleanField(
        label='Quero oferecer serviços',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('As senhas não coincidem.')
        
        return cleaned_data


class PerfilForm(forms.ModelForm):
    """Formulário para edição de perfil do usuário"""
    
    # Campos do User
    first_name = forms.CharField(
        label='Primeiro nome',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu primeiro nome'
        })
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu sobrenome'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com'
        })
    )
    
    class Meta:
        model = Usuario
        fields = ['nome', 'cidade', 'telefone', 'biografia', 'imagem', 'eh_empresa', 'eh_prestador']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome completo'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sua cidade'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Conte um pouco sobre você e seus serviços...'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'eh_empresa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'eh_prestador': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email


class VagaEmpregoForm(forms.ModelForm):
    """Formulário para criação e edição de vagas de emprego"""
    
    class Meta:
        model = VagaEmprego
        fields = ['titulo', 'descricao', 'categoria', 'localizacao', 'salario']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Produtor Musical, Professor de Piano, etc.'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Descreva as responsabilidades, requisitos e benefícios da vaga...'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'localizacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: São Paulo - SP, Remoto, etc.'
            }),
            'salario': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 3000.00 (opcional)',
                'step': '0.01'
            }),
        }
        labels = {
            'titulo': 'Título da Vaga',
            'descricao': 'Descrição',
            'categoria': 'Categoria',
            'localizacao': 'Localização',
            'salario': 'Salário (R$)',
        }
        help_texts = {
            'salario': 'Campo opcional. Informe o valor em reais.',
            'descricao': 'Inclua informações sobre responsabilidades, requisitos, benefícios e como se candidatar.',
        }

