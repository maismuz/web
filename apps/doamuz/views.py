from django.shortcuts import render
from django.shortcuts import *
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *


def homeDoa(request):
    return render(request, 'homeDoa.html')
