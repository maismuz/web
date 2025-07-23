from django import forms
from .models import Denuncia

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        # Campos que o usuário irá preencher (sem o eh_anonima)
        fields = [
            'titulo', 'descricao', 'tipo', 'data_ocorrencia', 
            'logradouro_ocorrencia', 'bairro_ocorrencia', 
            'ponto_referencia', 'anexo'
        ]
        
        # Widgets para estilização com Bootstrap 5
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': ' ', 'rows': 4}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'data_ocorrencia': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'logradouro_ocorrencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'bairro_ocorrencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'ponto_referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'anexo': forms.FileInput(attrs={'class': 'form-control'}),
        }