from django.shortcuts import *
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
<<<<<<< HEAD



=======
from django.shortcuts import render, get_object_or_404

>>>>>>> origin/develop
def hometur(request):
    return render(request, 'hometur.html')

def guia(request):
    return render(request, 'guia.html')

def estabelecimentos(request):
<<<<<<< HEAD
    return render(request, 'estabelecimentos.html')

def guias(request):
    return render(request, 'guias.html')
=======
    estabelecimentos = Estabelecimento.objects.all()
    return render(request, 'estabelecimentos.html', {'estabelecimentos': estabelecimentos})

def guias(request):
    guias = list(GuiaTuristico.objects.all())
    grupos = [guias[i:i+3] for i in range(0, len(guias), 3)]
    return render(request, 'guias.html', {
        'grupos': grupos,
        'guias': guias,     # adiciona variável esperada no template
    })
>>>>>>> origin/develop

def publicacoes(request):
    publicacoes = Publicacao.objects.all().order_by('-data_de_publicacao')
    return render(request, 'publicacoes.html', {'publicacoes': publicacoes})

def publicacao_detail(request, pk):
    from .models import Publicacao
    publicacao = Publicacao.objects.get(pk=pk)
<<<<<<< HEAD
    return render(request, 'publicacao_detail.html', {'publicacao': publicacao})
=======
    return render(request, 'publicacao_detail.html', {'publicacao': publicacao})

def guia_detail(request, pk):
    guia = get_object_or_404(GuiaTuristico, pk=pk)
    return render(request, 'guia_detail.html', {'guia': guia})

def estabelecimento_detail(request, pk):
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    return render(request, 'estabelecimento_detail.html', {'estabelecimento': estabelecimento})
>>>>>>> origin/develop
