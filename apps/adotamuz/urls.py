
from apps.adotamuz import views
from django.urls import path

urlpatterns = [
    path('', views.lista_racas, name='lista_racas'),
]
