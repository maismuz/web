from django.shortcuts import render, redirect
from .models import *
from django.views import View
from .forms import *

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class RegiCemiView(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CemiterioForm(request.POST)
            formset = AreaCemiterioFormSet(request.POST)
            if form.is_valid() and formset.is_valid():
                cemiterio = form.save()
                formset.instance = cemiterio
                formset.save()
                return redirect('')
        else:
            form = CemiterioForm()
            formset = AreaCemiterioFormSet()

        return render(request, 'registrocemi.html', {'form': form, 'formset': formset})
    
class RegiAreaView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registroarea.html')