# apps/reclamemuz/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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

def detalhe_denuncia(request, denuncia_id):
    # Busca a denúncia pelo ID. Se não encontrar, exibe um erro 404 (Página não encontrada).
    denuncia = get_object_or_404(Denuncia, pk=denuncia_id)
    
    # Se o formulário de status for enviado (método POST)
    if request.method == 'POST':
        # ATENÇÃO: Em um projeto real, aqui você deve verificar se o usuário tem permissão para mudar o status!
        # Ex: if not request.user.is_staff: return redirect('home')

        novo_status = request.POST.get('novo_status')
        
        # Validação para garantir que o status enviado é válido
        status_validos = [s[0] for s in Denuncia.STATUS_CHOICES]
        if novo_status in status_validos:
            denuncia.status = novo_status
            denuncia.save()
            messages.success(request, 'Status da denúncia alterado com sucesso!')
            # Redireciona para a mesma página para evitar reenvio do formulário
            return redirect('reclamemuz:detalhe_denuncia', denuncia_id=denuncia.id)
        else:
            messages.error(request, 'Ocorreu um erro: Status inválido.')

    # Se for uma requisição GET (apenas para visualizar a página)
    contexto = {
        'denuncia': denuncia,
        'status_choices': Denuncia.STATUS_CHOICES, # Envia as opções de status para o template
    }
    
    return render(request, 'detalhe_denuncia.html', contexto)