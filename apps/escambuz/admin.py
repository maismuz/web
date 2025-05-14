from django.contrib import admin
from .models import Oferta, DenunciaIrregular


@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'preco', 'data_criacao']
    search_fields = ['titulo']
    list_filter = ['data_criacao']


@admin.register(DenunciaIrregular)
class DenunciaIrregularAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'oferta', 'motivo_da_denuncia', 'status', 'data_denuncia']
    list_filter = ['status', 'motivo_da_denuncia', 'data_denuncia']
    search_fields = ['usuario__username', 'oferta__titulo']
    autocomplete_fields = ['usuario', 'oferta']
    ordering = ['-data_denuncia']
