from django import forms
from apps.esportemuz.models import *

class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = '__all__'

class CampeonatoForm(forms.ModelForm):
    class Meta:
        model = Campeonato
        fields = '__all__'
        exclude = ['encerrado']