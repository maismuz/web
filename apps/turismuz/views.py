from django.shortcuts import *
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

def hometur(request):
    publicacoes = Publicacao.objects.all().order_by('-data_de_publicacao')
    categorias = Categorias.objects.all()
    return render(request, 'hometur.html', {
        'publicacoes': publicacoes, 
        'categorias': categorias,
        'page_type': 'hometur'
    })

def guia(request):
    return render(request, 'guia.html')

def estabelecimentos(request):
    estabelecimentos = Estabelecimento.objects.all()
    categorias = Categorias.objects.all()
    return render(request, 'estabelecimentos.html', {
        'estabelecimentos': estabelecimentos, 
        'categorias': categorias,
        'page_type': 'estabelecimentos'
    })

def guias(request):
    guias = list(GuiaTuristico.objects.all())
    grupos = [guias[i:i+3] for i in range(0, len(guias), 3)]
    categorias = Categorias.objects.all()
    return render(request, 'guias.html', {
        'grupos': grupos,
        'guias': guias,
        'categorias': categorias,
        'page_type': 'guias'
    })

def publicacoes(request):
    publicacoes = Publicacao.objects.all().order_by('-data_de_publicacao')
    categorias = Categorias.objects.all()
    return render(request, 'publicacoes.html', {
        'publicacoes': publicacoes, 
        'categorias': categorias,
        'page_type': 'publicacoes'
    })

def publicacao_detail(request, pk):
    publicacao = Publicacao.objects.get(pk=pk)
    categorias = Categorias.objects.all()
    return render(request, 'publicacao_detail.html', {
        'publicacao': publicacao, 
        'categorias': categorias,
        'page_type': 'publicacoes'
    })

def guia_detail(request, pk):
    guia = get_object_or_404(GuiaTuristico, pk=pk)
    categorias = Categorias.objects.all()
    return render(request, 'guia_detail.html', {
        'guia': guia, 
        'categorias': categorias,
        'page_type': 'guias'
    })

def estabelecimento_detail(request, pk):
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    categorias = Categorias.objects.all()
    return render(request, 'estabelecimento_detail.html', {
        'estabelecimento': estabelecimento, 
        'categorias': categorias,
        'page_type': 'estabelecimentos'
    })

def add_publicacao(request):
    if request.method == 'POST':
        try:
            titulo = request.POST.get('titulo')
            texto_da_noticia = request.POST.get('texto_da_noticia')
            categoria_id = request.POST.get('categoria')
            legenda = request.POST.get('legenda')
            imagem = request.FILES.get('imagem')
            
            # Criar a publicação
            publicacao = Publicacao.objects.create(
                titulo=titulo,
                texto_da_noticia=texto_da_noticia,
                legenda=legenda,
                imagem=imagem,
            )
            
            # Adicionar categoria se fornecida
            if categoria_id:
                categoria = Categorias.objects.get(id=categoria_id)
                publicacao.categoria = categoria
                publicacao.save()
            
            messages.success(request, 'Publicação criada com sucesso!')
            return redirect('hometur')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar publicação: {str(e)}')
            return redirect('hometur')
    
    return redirect('hometur')

def add_estabelecimento(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            descricao = request.POST.get('descricao')
            endereco = request.POST.get('endereco')
            contato = request.POST.get('contato')
            categoria_id = request.POST.get('categoria')
            imagem = request.FILES.get('imagem')
            
            # Preparar dados para criação
            dados_estabelecimento = {
                'nome': nome,
                'descricao': descricao,
                'endereco': endereco,
                'contato': contato,
                'imagem': imagem,
            }
            
            # Adicionar categoria se fornecida
            if categoria_id and categoria_id != '':
                try:
                    categoria = Categorias.objects.get(id=categoria_id)
                    dados_estabelecimento['categoria'] = categoria
                except Categorias.DoesNotExist:
                    pass  # Ignora se a categoria não existir
            
            # Criar o estabelecimento
            estabelecimento = Estabelecimento.objects.create(**dados_estabelecimento)
            
            messages.success(request, 'Estabelecimento criado com sucesso!')
            return redirect('estabelecimentos')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar estabelecimento: {str(e)}')
            return redirect('estabelecimentos')
    
    return redirect('estabelecimentos')

def add_guia(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            descricao = request.POST.get('descricao')
            duracao_horas = request.POST.get('duracao')
            nivel_dificuldade = request.POST.get('nivel_dificuldade')
            valor = request.POST.get('valor')
            entidade_responsavel = request.POST.get('entidade_responsavel')
            contato = request.POST.get('contato')
            imagem = request.FILES.get('imagem')
            
            # Converter duração para formato timedelta se fornecida
            duracao = None
            if duracao_horas:
                from datetime import timedelta
                duracao = timedelta(hours=float(duracao_horas))
            
            # Criar o guia
            guia = GuiaTuristico.objects.create(
                nome=nome,
                descricao=descricao,
                duracao=duracao,
                nivel_dificuldade=nivel_dificuldade,
                valor=valor if valor else None,
                entidade_responsavel=entidade_responsavel,
                contato=contato,
                imagem=imagem,
            )
            
            messages.success(request, 'Guia turístico criado com sucesso!')
            return redirect('guias')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar guia: {str(e)}')
            return redirect('guias')
    
    return redirect('guias')
