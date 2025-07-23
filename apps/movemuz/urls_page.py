from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_page_view, name='base_page'),
]