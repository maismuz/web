
from apps.adotamuz import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.lista_racas, name='lista_racas'),
]
