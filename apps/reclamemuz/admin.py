from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Denuncia, Comentario, BuscaDenuncia, Midia, Notificacao, Categoria

#Gerenciar denúncias urbanas
class DenunciaResource(resources.ModelResource):
    class Meta:
        model = Denuncia
        fields = (
            'id', 
            'titulo', 
            'tipo', 
            'descricao', 
            'data_ocorrencia', 
            'logradouro_ocorrencia', 
            'bairro_ocorrencia',
            'status',
            'data_criacao',
        )
        export_order = fields

@admin.register(Denuncia)
class DenunciaAdmin(ImportExportModelAdmin):
    resource_class = DenunciaResource
    list_display = (
        'titulo',
        'tipo',
        'status',
        'bairro_ocorrencia',
        'data_ocorrencia',
        'data_criacao',
    )
    
    # Filtros que aparecerão na barra lateral direita
    list_filter = ('status', 'tipo', 'data_criacao')
    
    # Campo de busca
    search_fields = ('titulo', 'descricao', 'bairro_ocorrencia')

#Gerenciar comentários nas denúncias
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

    from .models import Denuncia, Comentario, BuscaDenuncia

#Gerenciar busca e filtros de denúncias
@admin.register(BuscaDenuncia)
class BuscaDenunciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'termo', 'categoria', 'status', 'bairro', 'data_inicial', 'data_final', 'data_busca')
    list_filter = ('categoria', 'status', 'bairro', 'data_busca')
    search_fields = ('termo', 'usuario__username', 'bairro')
    date_hierarchy = 'data_busca'
    ordering = ('-data_busca',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id_categoria', 'nome')
    search_fields = ('nome',)

@admin.register(Midia)
class MidiaAdmin(admin.ModelAdmin):
    list_display = ('id_midia', 'tipo', 'id_denuncia')
    list_filter = ('tipo',)
    search_fields = ('url_arquivo',)


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('id_notificacao', 'id_usuario', 'id_denuncia', 'data_hora')
    list_filter = ('data_hora', 'id_usuario')
    search_fields = ('mensagem', 'id_usuario__username', 'id_denuncia__id')
    date_hierarchy = 'data_hora'
