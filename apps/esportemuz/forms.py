from django import forms
from apps.esportemuz.models import *

class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = '__all__'