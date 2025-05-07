from django.contrib import admin
from esportemuz.models import *

# Register your models here.
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_per_page = 10