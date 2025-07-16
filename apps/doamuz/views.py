from django.shortcuts import render
from .models import Solicitacao, Categoria

def homedoa(request):
    return render(request, 'homedoa.html') 
def instrucoes(request):
    return render(request, 'instrucoes.html')  
def doacao(request):
    return render(request, 'doacao.html') 
def login(request):
    return render(request, 'login.html') 
def ongs(request):
    return render(request, 'ongs.html') 
def doador(request):
    categoria_id = request.GET.get('categoria')
    categorias = Categoria.objects.all()
    if categoria_id:
        solicitacoes = Solicitacao.objects.filter(categoria_id=categoria_id)
    else:
        solicitacoes = Solicitacao.objects.all()
    return render(request, 'doador.html', {
        'solicitacoes': solicitacoes,
        'categorias': categorias,
        'categoria_selecionada': categoria_id
    })