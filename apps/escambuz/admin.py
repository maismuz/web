from django.contrib import admin
from .models import AvaliacaoUsuario

class AvaliacaoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nota', 'comentario', 'data_avaliacao']
    search_fields = ['usuario__username', 'comentario']
    list_filter = ['nota', 'data_avaliacao']  
    ordering = ['-data_avaliacao']  

admin.site.register(AvaliacaoUsuario, AvaliacaoUsuarioAdmin)

