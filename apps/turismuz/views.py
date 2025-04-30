from django.shortcuts import *
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *



def hometur(request):
    return render(request, 'hometur.html')

def guia(request):
    return render(request, 'guia.html')

def estabelecimentos(request):
    return render(request, 'estabelecimentos.html')

def guias(request):
    return render(request, 'guias.html')

def publicacoes(request):
    publicacoes = Publicacao.objects.all().order_by('-data_de_publicacao')
    return render(request, 'publicacoes.html', {'publicacoes': publicacoes})

def publicacao_detail(request, pk):
    from .models import Publicacao
    publicacao = Publicacao.objects.get(pk=pk)
    return render(request, 'publicacao_detail.html', {'publicacao': publicacao})