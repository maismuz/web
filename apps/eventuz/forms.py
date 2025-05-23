from django import forms
from .models import Evento


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'data_hora', 'local', 'descricao', 'organizador', 'cnpj', 'contato', 'categoria']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Data e hora do evento', 'type': 'datetime-local'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do evento', 'style': 'height: 100px;'}),
        }
    # def __init__(self, *args, **kwargs):
    #     super(EventoForm, self).__init__(*args, **kwargs)
    #     self.fields['nome'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nome do evento'})
    #     self.fields['local'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Local do evento'})
    #     self.fields['organizador'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Organizador do evento'})
    #     self.fields['cnpj'].widget.attrs.update({'class': 'form-control', 'placeholder': 'CNPJ do organizador'})
    #     self.fields['contato'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contato do organizador'})
    #     self.fields['categoria'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Categoria do evento'})
    #     self.fields['categoria'].empty_label = "Selecione uma categoria"
