from django.shortcuts import render
from .models import *
from django.views import View

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class InicioView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'inicio.html')
    
class HorariosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'horarios.html')
    
class AreasView(View):
    def get (self, request, *args, **kwargs):
        return render (request, 'areas.html')