from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from django.forms import inlineformset_factory
from .forms import *


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
class DetalheItemAcervoView(View):
    def get(self, request, pk):
        item = ItemAcervo.objects.filter(pk=pk).first()
        imagens = []
        if item:
            imagens = ImagemItemAcervo.objects.filter(item_acervo=item)
        return render(
            request,
            'detalhe_item_acervo.html',
            {
                'item': item,  # Corrigido para 'item'
                'imagens': imagens
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
    
    
class FormDocumentoHistoricoView(View):
    
    def get(self, request):
        return render(request, 'formulario_docshistorico.html')
# Create your views here.


class PatrimonioCreateView(View):
    def get(self, request):
        patrimonio_form = PatrimonioForm()
        ImagemFormSet = inlineformset_factory(
            Patrimonio, ImagemPatrimonio, form=ImagemPatrimonioForm, extra=3, can_delete=False
        )
        formset = ImagemFormSet()
        return render(request, 'formulario_patrimonio.html', {
            'patrimonio_form': patrimonio_form,
            'formset': formset
        })

    def post(self, request):
        ImagemFormSet = inlineformset_factory(
            Patrimonio, ImagemPatrimonio, form=ImagemPatrimonioForm, extra=3, can_delete=False
        )
        patrimonio_form = PatrimonioForm(request.POST)
        formset = ImagemFormSet(request.POST, request.FILES)
        if patrimonio_form.is_valid() and formset.is_valid():
            patrimonio = patrimonio_form.save(commit=False)
            patrimonio.usuario_adicionado = request.user
            patrimonio.save()
            imagens = formset.save(commit=False)
            for imagem in imagens:
                imagem.patrimonio = patrimonio
                imagem.save()
            return redirect('patrimonio', pk=patrimonio.pk)
        return render(request, 'formulario_patrimonio.html', {
            'patrimonio_form': patrimonio_form,
            'formset': formset
        })

class ItemAcervoCreateView(View):
    def get(self, request):
        item_form = ItemAcervoForm()
        ImagemFormSet = inlineformset_factory(
            ItemAcervo, ImagemItemAcervo, form=ImagemItemAcervoForm, extra=3, can_delete=False
        )
        formset = ImagemFormSet()
        return render(request, 'formulario_itens.html', {
            'item_form': item_form,
            'formset': formset
        })

    def post(self, request):
        ImagemFormSet = inlineformset_factory(
            ItemAcervo, ImagemItemAcervo, form=ImagemItemAcervoForm, extra=3, can_delete=False
        )
        item_form = ItemAcervoForm(request.POST)
        formset = ImagemFormSet(request.POST, request.FILES)
        if item_form.is_valid() and formset.is_valid():
            item = item_form.save(commit=False)
            item.usuario_adicionado = request.user
            item.save()
            imagens = formset.save(commit=False)
            for imagem in imagens:
                imagem.item_acervo = item
                imagem.save()
            return redirect('detalhe_item_acervo', pk=item.pk)
        return render(request, 'formulario_itens.html', {
            'item_form': item_form,
            'formset': formset
        })