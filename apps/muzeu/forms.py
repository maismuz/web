from django import forms
from .models import Patrimonio, ItemAcervo, ImagemPatrimonio, ImagemItemAcervo

class PatrimonioForm(forms.ModelForm):
    class Meta:
        model = Patrimonio
        fields = [
            'nome',
            'descricao',
            'tipo',
            'data_origem',
            'localizacao',
            'coordenadas',
            'status',
            'importancia_historica',
            # 'data_adicao',  # auto_now_add, não incluir no form
            # 'usuario_adicionado',  # geralmente preenchido automaticamente
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Patrimônio'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'style': 'height: 100px'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'data_origem': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data de Origem', 'type': 'date'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Localização'}),
            'coordenadas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Coordenadas'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'importancia_historica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Importância Histórica'}),
        }

class ItemAcervoForm(forms.ModelForm):
    class Meta:
        model = ItemAcervo
        fields = [
            'nome',
            'categoria',
            'descricao',
            'origem',
            'data_origem',
            'numero_registro',
            'estado_conservacao',
            'status',
            'localizacao_fisica',
            'valor_estimado',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Item'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'style': 'height: 100px'}),
            'origem': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'data_origem': forms.DateInput(attrs={'class': 'form-control', 'placeholder': ' ', 'type': 'date'}),
            'numero_registro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'estado_conservacao': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'localizacao_fisica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'valor_estimado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
        }

class ImagemPatrimonioForm(forms.ModelForm):
    class Meta:
        model = ImagemPatrimonio
        fields = ['patrimonio', 'imagem', 'legenda', 'eh_principal']
        widgets = {
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'legenda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Legenda'}),
            'eh_principal': forms.Select(attrs={'class': 'form-select'}),
            'patrimonio': forms.HiddenInput(),  # geralmente oculto no formset
        }

class ImagemItemAcervoForm(forms.ModelForm):
    class Meta:
        model = ImagemItemAcervo
        fields = ['item_acervo', 'imagem', 'legenda', 'eh_principal']
        widgets = {
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'legenda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Legenda'}),
            'eh_principal': forms.Select(attrs={'class': 'form-select'}),
            'item_acervo': forms.HiddenInput(),  # geralmente oculto no formset
        }