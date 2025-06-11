from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class IndexView(View):
    def get(self, request):
        return render(request, 'index_muzeu.html')
    
class ItemAcervoView(View):
    def get(self, request):
        return render(request, 'item_acervo.html')

class PatrimonioView(View):
    def get(self, request):
        return render(request, 'patrimonio.html')
    
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

