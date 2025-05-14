from django.shortcuts import *
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
from django.shortcuts import render, get_object_or_404

def hometur(request):
    return render(request, 'hometur.html')

def guia(request):
    return render(request, 'guia.html')

def estabelecimentos(request):
    estabelecimentos = Estabelecimento.objects.all()
    return render(request, 'estabelecimentos.html', {'estabelecimentos': estabelecimentos})

def guias(request):
    guias = GuiaTuristico.objects.all()
    return render(request, 'guias.html', {'guias': guias})

def publicacoes(request):
    publicacoes = Publicacao.objects.all().order_by('-data_de_publicacao')
    return render(request, 'publicacoes.html', {'publicacoes': publicacoes})

def publicacao_detail(request, pk):
    from .models import Publicacao
    publicacao = Publicacao.objects.get(pk=pk)
    return render(request, 'publicacao_detail.html', {'publicacao': publicacao})

def guia_detail(request, pk):
    guia = get_object_or_404(GuiaTuristico, pk=pk)
    return render(request, 'guia_detail.html', {'guia': guia})

def estabelecimento_detail(request, pk):
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    return render(request, 'estabelecimento_detail.html', {'estabelecimento': estabelecimento})
