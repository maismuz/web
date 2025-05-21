from django.views import View
from django.shortcuts import render

class IndexView(View):
    def get(self, request):
        return render(request, 'eventuz/index.html')

class EventosView(View):
    def get(self, request):
        return render(request, 'eventuz/eventos.html')

class CadastrarEventosView(View):
    def get(self, request):
        return render(request, 'eventuz/cadastrar_eventos.html')
