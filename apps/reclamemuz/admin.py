from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Denuncia, Comentario


class DenunciaResource(resources.ModelResource):
    class Meta:
        model = Denuncia
        fields = (
            'id_denuncia', 'titulo', 'descricao', 'categoria',
            'endereco', 'latitude', 'longitude', 'data_ocorrencia',
            'status', 'id_usuario__username'
        )

@admin.register(Denuncia)
class DenunciaAdmin(ImportExportModelAdmin):
    resource_class = DenunciaResource
    list_display = ('id_denuncia', 'titulo', 'categoria', 'status', 'data_ocorrencia', 'id_usuario')
    list_filter = ('categoria', 'status', 'data_ocorrencia')
    search_fields = ('titulo', 'descricao', 'endereco', 'id_usuario__username')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_usuario', 'id_denuncia', 'data_hora', 'resumo_texto')
    list_filter = ('data_hora', 'id_usuario', 'id_denuncia')
    search_fields = ('texto', 'id_usuario__username', 'id_denuncia__id')
    date_hierarchy = 'data_hora'
    ordering = ('-data_hora',)

    def resumo_texto(self, obj):
        return (obj.texto[:50] + '...') if len(obj.texto) > 50 else obj.texto
    resumo_texto.short_description = 'Texto (resumo)'