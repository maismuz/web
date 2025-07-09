from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from apps.covamuz.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('inicio/', InicioView.as_view(), name='inicio'),
    path('horarios/', HorariosView.as_view(), name='horarios'),
    path('areas/',AreasView.as_view(), name= 'areas'),
]