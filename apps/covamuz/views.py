from django.shortcuts import render, redirect
from .models import *
from django.views import View

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class RegistroView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registro.html')