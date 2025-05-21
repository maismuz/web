from django.views import View
from django.shortcuts import render, redirect
from .forms import EventoForm

class IndexView(View):
    def get(self, request):
        return render(request, 'eventuz/index.html')

class EventosView(View):
    def get(self, request):
        return render(request, 'eventuz/eventos.html')

class CadastrarEventosView(View):
    def get(self, request):
        return render(request, 'eventuz/cadastrar_eventos.html')

class CadastrarEventosView(View):
    def get(self, request):
        form = EventoForm()
        return render(request, 'eventuz/cadastrar_eventos.html', {'form': form})

    def post(self, request):
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('eventos')
        return render(request, 'eventuz/cadastrar_eventos.html', {'form': form})