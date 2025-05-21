from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from apps.covamuz.views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registro/', RegistroView.as_view(), name='registro'),
]
