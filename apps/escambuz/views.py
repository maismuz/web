from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Categoria, Objeto, Mensagem, FotoObjeto
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required 

def categoria_objeto(request):
    categorias = Categoria.objects.all()
    objetos = Objeto.objects.select_related('categoria', 'usuario').all()
    return render(request, 'categoria_objeto.html', {
        'categorias': categorias,
        'objetos': objetos,
    })

@login_required 
def iniciar_conversa(request, destinatario_id):
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

    return render(request, 'conversa.html', {
        'destinatario': destinatario,
        'conversas': conversas
    })

@login_required 
def adicionar_objeto(request):
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

        return redirect('categoria_objeto') 
    
    categorias = Categoria.objects.all()
    objetos = Objeto.objects.select_related('categoria', 'usuario').all()
    return render(request, 'categoria_objeto.html', {
        'categorias': categorias,
        'objetos': objetos,
    })

def home_view(request):
    return render(request, 'home.html')