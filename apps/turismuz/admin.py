from django.contrib import admin
from .models import *
admin.site.register(Categorias) 
admin.site.register(Estabelecimento)
admin.site.register(GuiaTuristico)
admin.site.register(Publicacao)
admin.site.register(ImagemPublicacao)
admin.site.register(Avaliacao)
admin.site.register(Permissao)

