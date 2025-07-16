from django import forms
from .models import Motorista_MoveMuz, Combustivel, TipoVeiculo, Veiculo, Local, EscalaVeiculo, HorarioTransporte, Viagem, Passageiro, Ponto, Parada, OcupacaoVeiculo

class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista_MoveMuz
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
        }

class CombustivelForm(forms.ModelForm):
    class Meta:
        model = Combustivel
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Gasolina'}),
        }

class TipoVeiculoForm(forms.ModelForm):
    class Meta:
        model = TipoVeiculo
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Carro, Ônibus'}),
        }

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'
        widgets = {
            'ano_fabricacao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ano'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABC1234'}),
            'capacidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'condicao_manutencao': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'combustivel': forms.Select(attrs={'class': 'form-select'}),
            'cor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Azul'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Onix'}),
        }

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = '__all__'
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class EscalaVeiculoForm(forms.ModelForm):
    class Meta:
        model = EscalaVeiculo
        fields = '__all__'
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'origem': forms.Select(attrs={'class': 'form-select'}),
            'destino': forms.Select(attrs={'class': 'form-select'}),
            'horario_saida': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'horario_chegada': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class HorarioTransporteForm(forms.ModelForm):
    class Meta:
        model = HorarioTransporte
        fields = '__all__'
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'origem': forms.Select(attrs={'class': 'form-select'}),
            'destino': forms.Select(attrs={'class': 'form-select'}),
            'horario_partida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = '__all__'
        widgets = {
            'motorista': forms.Select(attrs={'class': 'form-select'}),
            'origem': forms.Select(attrs={'class': 'form-select'}),
            'destino': forms.Select(attrs={'class': 'form-select'}),
            'data_saida': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'data_chegada': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class PassageiroForm(forms.ModelForm):
    class Meta:
        model = Passageiro
        fields = '__all__'
        widgets = {
            'viagem': forms.Select(attrs={'class': 'form-select'}),
        }

class PontoForm(forms.ModelForm):
    class Meta:
        model = Ponto
        fields = '__all__'

class ParadaForm(forms.ModelForm):
    class Meta:
        model = Parada
        fields = '__all__'
        widgets = {
            'horario_transporte': forms.Select(attrs={'class': 'form-select'}),
            'ponto': forms.Select(attrs={'class': 'form-select'}),
            'horario': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class OcupacaoVeiculoForm(forms.ModelForm):
    class Meta:
        model = OcupacaoVeiculo
        fields = '__all__'
        widgets = {
            'horario_transporte': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }