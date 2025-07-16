from django.http import HttpResponse
from django.shortcuts import render

def lista_racas(request):
   return render(request, 'index.html')
