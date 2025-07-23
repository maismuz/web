from django import forms
from django.forms import inlineformset_factory
from .models import *

class CemiterioForm(forms.ModelForm):
    class Meta:
        model = Cemiterio
        fields = ['nome', 'cidade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do cemitério', 'id': 'inputCemiterio'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade', 'id': 'inputCidade'}),
        }

AreaCemiterioFormSet = inlineformset_factory(
    Cemiterio, AreaCemiterio,
    fields=['nome'],
    extra=1,
    can_delete=True,
    widgets={
        'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da área'}),
    }
)
