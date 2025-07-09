from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'data_hora', 'local', 'descricao', 'organizador', 'cnpj', 'contato', 'categoria']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Data e hora do evento', 
                'type': 'datetime-local'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Descrição do evento', 
                'style': 'height: 100px;'
            }),
        }
