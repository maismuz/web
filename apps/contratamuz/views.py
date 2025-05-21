from django.shortcuts import render
from apps.contratamuz.models import *

def inicial(request):
    return render(request, 'inicial.html')

def listar_vagas(request):
    vagas = VagaEmprego.objects.filter(ativa=True).order_by('-criado_em')
    return render(request, 'listar_vagas.html', {'vagas': vagas})

