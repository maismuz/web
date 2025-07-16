from django.urls import path
from . import views

urlpatterns = [
    path('', views.full_forms_view, name='full_forms'),
]