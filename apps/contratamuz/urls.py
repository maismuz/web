from django.contrib import admin
from django.urls import path
from contratamuz import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicial, name='inicial'),
    path('vagas/', views.listar_vagas, name='listar_vagas'),
    # adicione outras rotas conforme necessário
]
