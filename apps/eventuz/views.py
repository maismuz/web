from django.views import View
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import date
from .forms import EventoForm
from .models import *
from datetime import timedelta



class IndexView(View):
    def get(self, request):
        return render(request, 'eventuz/index.html')


class EventosView(View):
    def get(self, request):
        agora = timezone.now()
        eventos = Evento.objects.filter(
            aprovado=True,
            data_hora__gte=agora - timedelta(days=1)
        )

        nome = request.GET.get('nome')
        organizador = request.GET.get('organizador')
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        categoria_id = request.GET.get('categoria')
        local = request.GET.get('local')

        if nome:
            eventos = eventos.filter(nome__icontains=nome)
        if organizador:
            eventos = eventos.filter(organizador__icontains=organizador)
        if data_inicio:
            eventos = eventos.filter(data_hora__date__gte=parse_date(data_inicio))
        if data_fim:
            eventos = eventos.filter(data_hora__date__lte=parse_date(data_fim))
        if categoria_id:
            eventos = eventos.filter(categoria_id=categoria_id)
        if local:
            eventos = eventos.filter(local__icontains=local)

        eventos = eventos.order_by('data_hora')
        categorias = Categoria.objects.all()
        return render(request, 'eventuz/eventos.html', {'eventos': eventos, 'categorias': categorias})
    
class CadastrarEventosView(View):
    def get(self, request):
        form = EventoForm()
        return render(request, 'eventuz/cadastrar_eventos.html', {'form': form})

    def post(self, request):
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save()

            # Pega a lista de arquivos enviados
            arquivos = request.FILES.getlist('midia_arquivos')
            url_video = form.cleaned_data.get('midia_url')

            # Cria um Midia para cada arquivo enviado
            for arquivo in arquivos:
                # Detecta tipo pelo content_type ou pela extensão do arquivo para decidir foto ou vídeo
                if arquivo.content_type.startswith('image/'):
                    tipo = 'foto'
                elif arquivo.content_type.startswith('video/'):
                    tipo = 'video'
                else:
                    tipo = 'foto'  # padrão

                Midia.objects.create(evento=evento, tipo=tipo, arquivo=arquivo)

            # Se tiver URL de vídeo, cria a mídia de vídeo
            if url_video:
                Midia.objects.create(evento=evento, tipo='video', url_video=url_video)

            return redirect('eventuz:eventos')

        return render(request, 'eventuz/cadastrar_eventos.html', {'form': form})


class HistoricoView(View):
    def get(self, request):
        eventos_passados = Evento.objects.filter(
            aprovado=True,
            data_hora__lt=timezone.now()
        )

        nome = request.GET.get('nome')
        organizador = request.GET.get('organizador')
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        categoria_id = request.GET.get('categoria')
        local = request.GET.get('local')

        if nome:
            eventos_passados = eventos_passados.filter(nome__icontains=nome)
        if organizador:
            eventos_passados = eventos_passados.filter(organizador__icontains=organizador)
        if data_inicio:
            eventos_passados = eventos_passados.filter(data_hora__date__gte=parse_date(data_inicio))
        if data_fim:
            eventos_passados = eventos_passados.filter(data_hora__date__lte=parse_date(data_fim))
        if categoria_id:
            eventos_passados = eventos_passados.filter(categoria_id=categoria_id)
        if local:
            eventos_passados = eventos_passados.filter(local__icontains=local)

        eventos_passados = eventos_passados.order_by('-data_hora')
        categorias = Categoria.objects.all()
        return render(request, 'eventuz/historico.html', {
            'eventos': eventos_passados,
            'categorias': categorias
        })


class DetalhesEventoView(View):
    def get(self, request, pk):
        evento = Evento.objects.get(pk=pk)
        return render(request, 'eventuz/detalhes_evento.html', {'evento': evento})
