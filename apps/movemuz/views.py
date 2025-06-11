from django.shortcuts import render, redirect
from .forms import VeiculoForm
from .models import TipoVeiculo, Combustivel
from datetime import datetime

def cadastrar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sucesso_cadastro_veiculo')
    else:
        form = VeiculoForm()

    tipos_veiculo = TipoVeiculo.objects.all()
    combustiveis = Combustivel.objects.all()
    current_year = datetime.now().year

    context = {
        'form': form,
        'tipos_veiculo': tipos_veiculo,
        'combustiveis': combustiveis,
        'current_year': current_year,
    }
    return render(request, 'cadastro_veiculo.html', context)