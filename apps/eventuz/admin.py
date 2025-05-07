from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

class MidiaInline(admin.TabularInline):
    model = Midia
    extra = 1

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    inlines = [MidiaInline]
    list_display = ['nome', 'data', 'local']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
