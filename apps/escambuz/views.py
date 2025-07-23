from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Categoria, Objeto, Mensagem, FotoObjeto
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def home_view(request):
    """
    View para a página inicial (index), que mostra o carrossel de categorias
    e os objetos adicionados recentemente.
    """
    categorias = Categoria.objects.all()
    objetos = Objeto.objects.select_related('categoria', 'usuario').order_by('-data_cadastro')[:6]
    
    # ALTERAÇÃO: Aponta para o novo nome do template 'index_escambuz.html'
    return render(request, 'escambuz/index_escambuz.html', {
        'categorias': categorias,
        'objetos': objetos,
    })

def categoria_objeto_view(request):
    """
    View para a página de gerenciamento, que mostra as tabelas de
    categorias e objetos.
    """
    categorias = Categoria.objects.all()
    objetos = Objeto.objects.select_related('categoria', 'usuario').all()
    
    # Aponta para o template da página de gerenciamento
    return render(request, 'escambuz/categoria_objeto.html', {
        'categorias': categorias,
        'objetos': objetos,
    })

@login_required
def adicionar_objeto(request):
    """
    View que processa o formulário para adicionar um novo objeto.
    """
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        tipo = request.POST.get('tipo')
        categoria_id = request.POST.get('categoria')
        estado = request.POST.get('estado')
        fotos = request.FILES.getlist('fotos')

        categoria = get_object_or_404(Categoria, id=categoria_id)

        objeto = Objeto.objects.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            tipo=tipo,
            categoria=categoria,
            estado=estado,
            usuario=request.user
        )
        for foto_file in fotos:
            FotoObjeto.objects.create(objeto=objeto, imagem=foto_file)

        # Redireciona de volta para a página de gerenciamento após salvar
        return redirect('categoria_objeto')
    
    # Se não for POST, apenas redireciona para a página de gerenciamento
    return redirect('categoria_objeto')

@login_required
def iniciar_conversa(request, destinatario_id):
    """
    View para o sistema de chat entre usuários.
    """
    destinatario = get_object_or_404(User, id=destinatario_id)

    if request.method == "POST":
        mensagem_texto = request.POST.get("mensagem")
        if mensagem_texto:
            mensagem = Mensagem(remetente=request.user, destinatario=destinatario, mensagem=mensagem_texto)
            mensagem.save()
            return HttpResponseRedirect(request.path)

    conversas = Mensagem.objects.filter(
        (Q(remetente=request.user) & Q(destinatario=destinatario)) |
        (Q(remetente=destinatario) & Q(destinatario=request.user))
    ).order_by('data_envio')

    return render(request, 'escambuz/conversa.html', { # Supondo que você tenha um template 'conversa.html'
        'destinatario': destinatario,
        'conversas': conversas
    })