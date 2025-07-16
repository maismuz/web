# apps/movemuz/forms.py
from django import forms
from .models import (
    Motorista_MoveMuz, Combustivel, TipoVeiculo, Veiculo, Local,
    EscalaVeiculo, HorarioTransporte, Viagem, Passageiro, Ponto,
    Parada, OcupacaoVeiculo, ESTADOS_BRASIL # Importe ESTADOS_BRASIL para choices, se for usar
)

class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista_MoveMuz
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do motorista'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'cnh_numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000000000'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # Checkbox
        }

class CombustivelForm(forms.ModelForm):
    class Meta:
        model = Combustivel
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Gasolina, Diesel, Etanol'}),
        }

class TipoVeiculoForm(forms.ModelForm):
    class Meta:
        model = TipoVeiculo
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Carro, Ônibus, Caminhão'}),
        }

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'
        widgets = {
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Onix, FH 540, Marcopolo'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABC1234'}),
            'cor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Azul, Branco, Prata'}),
            'ano_fabricacao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2023'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}), # Para ImageField/FileField
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'combustivel': forms.Select(attrs={'class': 'form-select'}),
            'capacidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de passageiros ou carga'}),
            'condicao_manutencao': forms.Select(attrs={'class': 'form-select'}),
        }

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do local (ex: Terminal Rodoviário)'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço completo'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Guaxupé'}),
            'estado': forms.Select(attrs={'class': 'form-select', 'choices': ESTADOS_BRASIL}), # Usando ESTADOS_BRASIL aqui
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
            'dias_semana': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Segunda a sexta, Fins de semana'}),
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
            'finalidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Entrega de materiais, Viagem de serviço'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detalhes adicionais da viagem...'}),
        }

class PassageiroForm(forms.ModelForm):
    class Meta:
        model = Passageiro
        fields = '__all__'
        widgets = {
            'viagem': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do passageiro'}),
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número do RG/CPF/Passaporte'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações sobre o passageiro (restrições, necessidades especiais)...'}),
        }

class PontoForm(forms.ModelForm):
    class Meta:
        model = Ponto
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Ponto de Ônibus Central'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço ou descrição do ponto de embarque/desembarque'}),
        }

class ParadaForm(forms.ModelForm):
    class Meta:
        model = Parada
        fields = '__all__'
        widgets = {
            'horario_transporte': forms.Select(attrs={'class': 'form-select'}),
            'ponto': forms.Select(attrs={'class': 'form-select'}),
            'horario': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'passageiros_estimados': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número estimado de passageiros nesta parada'}),
        }

class OcupacaoVeiculoForm(forms.ModelForm):
    class Meta:
        model = OcupacaoVeiculo
        fields = '__all__'
        widgets = {
            'horario_transporte': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'passageiros_a_bordo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de passageiros que embarcaram'}),
        }