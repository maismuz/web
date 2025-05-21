from django import forms
from .models import Evento


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'data', 'local', 'descricao', 'organizador', 'cnpj', 'contato', 'categoria']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data do evento'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do evento', 'style': 'height: 100px;'}),
        }
