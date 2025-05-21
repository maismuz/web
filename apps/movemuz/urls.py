from apps.movemuz import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
]