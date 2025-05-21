from apps.movemuz import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]