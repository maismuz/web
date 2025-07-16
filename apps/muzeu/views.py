from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *

class IndexView(View):
    def get(self, request):
        patrimonios = Patrimonio.objects.all()
        imagens_patrimonio = ImagemPatrimonio.objects.select_related('patrimonio').all()
        return render(
            request,
            'index_muzeu.html',
            {
                'patrimonios': patrimonios,
                'imagens_patrimonio': imagens_patrimonio
            }
        )
    
class ItemAcervoView(View):
    def get(self, request):
        itens_acervo = ItemAcervo.objects.all().order_by('nome')
        imagens_itens_acervo = ImagemItemAcervo.objects.select_related('item_acervo').all()
        return render(
            request,
            'item_acervo.html',
            {
                'itens_acervo': itens_acervo,
                'imagens_itens_acervo': imagens_itens_acervo
            }
        )

class PatrimonioView(View):
    def get(self, request, pk=None):
        patrimonio = None
        imagens = []
        if pk:
            patrimonio = Patrimonio.objects.filter(pk=pk).first()
            if patrimonio:
                imagens = ImagemPatrimonio.objects.filter(patrimonio=patrimonio)
        return render(
            request,
            'patrimonio.html',
            {
                'patrimonio': patrimonio,
                'imagens': imagens
            }
        )
    
class ListaItemView(View):
    def get(self, request):
        imagens_patrimonio = ImagemPatrimonio.objects.select_related('patrimonio').order_by('patrimonio__nome')
        patrimonios = Patrimonio.objects.all().order_by('nome')
        return render(
            request,
            'lista_item.html',
            {
                'patrimonios': patrimonios,
                'imagens_patrimonio': imagens_patrimonio
            }
        )
class DocumentoHistoricoView(View):
    def get(self, request):
        return render(request, 'documento_historico.html')
    
class FormItensAcervoView(View):
    
    def get(self, request):
        return render(request, 'formulario_itens.html')
    
class FormPatrimonioView(View):
    
    def get(self, request):
        return render(request, 'formulario_patrimonio.html')
    
class FormDocumentoHistoricoView(View):
    
    def get(self, request):
        return render(request, 'formulario_docshistorico.html')
# Create your views here.

