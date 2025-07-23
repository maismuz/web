# apps/reclamemuz/views.py

from django.shortcuts import render, redirect
from .forms import DenunciaForm
from .models import Denuncia
def index(request):
    return render(request, 'homereclamemuz.html')

def denuncias(request):
    if request.method == 'POST':
        form = DenunciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # CORRIGIDO AQUI: Adicionado o namespace 'reclamemuz:'
            return redirect('reclamemuz:denuncia_sucesso') 
    else:
        form = DenunciaForm()
        
    return render(request, 'forms_Denuncia.html', {'form': form})

def denuncia_sucesso(request):
    return render(request, 'denuncia_sucesso.html')

# def listar_denuncias(request):
#     return render(request, 'denuncias.html')

def listar_denuncias(request):
    # 1. Busca todas as denúncias no banco de dados, ordenando pelas mais recentes.
    lista_de_denuncias = Denuncia.objects.all().order_by('-data_criacao')
    
    # 2. Cria o "contexto", que é um dicionário para enviar os dados para o template.
    contexto = {
        'denuncias': lista_de_denuncias
    }
    
    # 3. Renderiza o template 'listar_denuncias.html' e envia os dados para ele.
    return render(request, 'listar_denuncias.html', contexto)
