from django.views import View
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import date
from .forms import EventoForm
from .models import Evento


class IndexView(View):
    def get(self, request):
        return render(request, 'eventuz/index.html')


class EventosView(View):
    def get(self, request):
        eventos = Evento.objects.filter(aprovado=True, data_hora__gte=date.today()).order_by('data_hora')
        return render(request, 'eventuz/eventos.html', {'eventos': eventos})


class CadastrarEventosView(View):
    def get(self, request):
        form = EventoForm()
        return render(request, 'eventuz/cadastrar_eventos.html', {'form': form})

    def post(self, request):
        form = EventoForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('eventuz:eventos')
        return render(request, 'eventuz/cadastrar_eventos.html', {'form': form})


class HistoricoView(View):
    def get(self, request):
        eventos_passados = Evento.objects.filter(aprovado=True, data_hora__lt=timezone.now()).order_by('-data_hora')
        return render(request, 'eventuz/historico.html', {'eventos_passados': eventos_passados})

class DetalhesEventoView(View):
    def get(self, request, pk):
        evento = Evento.objects.get(pk=pk)
        return render(request, 'eventuz/detalhes_evento.html', {'evento': evento})
