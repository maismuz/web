from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Denuncia

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
