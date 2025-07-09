# apps/reclamemuz/views.py

from django.shortcuts import render, redirect
from .forms import DenunciaForm

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