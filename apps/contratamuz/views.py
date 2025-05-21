from django.shortcuts import render
from apps.contratamuz.models import *

def inicial(request):
    return render(request, 'contratamuz/index.html')

def listar_vagas(request):
    vagas = VagaEmprego.objects.filter(ativa=True).order_by('-criado_em')
    return render(request, 'contratamuz/listar_vagas.html', {'vagas': vagas})

def listar_servicos(request):
    servicos = Servico.objects.all().order_by('-criado_em')
    return render(request, 'contratamuz/listar_servicos.html', {'servicos': servicos})

