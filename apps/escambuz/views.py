from django.shortcuts import render
from .models import Categoria, Objeto

def index(request):

    categorias = Categoria.objects.all()
    
    objetos_recentes = Objeto.objects.order_by('-data_cadastro')[:9]
    
    context = {
        'categorias': categorias,
        'objetos': objetos_recentes
    }
    

    return render(request, 'escambuz/index.html', context)