from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Categoria, Denuncia, Comentario, Notificacao, Midia

# ----------------------------
# Categoria
# ----------------------------
class CategoriaResource(resources.ModelResource):
    class Meta:
        model = Categoria
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'nome')

@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    resource_class = CategoriaResource
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    ordering = ['nome']
    fieldsets = (
        ('Categoria', {
            'fields': ('nome',),
        }),
    )

# ----------------------------
# Denuncia
# ----------------------------
class DenunciaResource(resources.ModelResource):
    class Meta:
        model = Denuncia
        skip_unchanged = True
        report_skipped = True
        fields = (
            'id', 'titulo', 'descricao', 'categoria', 'endereco',
            'latitude', 'longitude', 'data_ocorrencia', 'status',
            'data_publicacao'
        )

@admin.register(Denuncia)
class DenunciaAdmin(ImportExportModelAdmin):
    resource_class = DenunciaResource
    list_display = ('id', 'titulo', 'categoria', 'status', 'data_ocorrencia', 'data_publicacao')
    list_filter = ('status', 'categoria')
    search_fields = ('titulo', 'descricao', 'endereco')
    readonly_fields = ('data_publicacao',)
    ordering = ['-data_publicacao']
    date_hierarchy = 'data_ocorrencia'
    fieldsets = (
        ('Informações da Denúncia', {
            'fields': ('titulo', 'descricao', 'categoria', 'status')
        }),
        ('Localização', {
            'fields': ('endereco', 'latitude', 'longitude')
        }),
        ('Datas', {
            'fields': ('data_ocorrencia', 'data_publicacao')
        }),
    )

# ----------------------------
# Comentario
# ----------------------------
class ComentarioResource(resources.ModelResource):
    class Meta:
        model = Comentario
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'texto', 'data_hora', 'denuncia')

@admin.register(Comentario)
class ComentarioAdmin(ImportExportModelAdmin):
    resource_class = ComentarioResource
    list_display = ('id', 'denuncia', 'data_hora')
    search_fields = ('texto',)
    ordering = ['-data_hora']
    readonly_fields = ('data_hora',)
    fieldsets = (
        ('Comentário', {
            'fields': ('denuncia', 'texto', 'data_hora')
        }),
    )

# ----------------------------
# Notificacao
# ----------------------------
class NotificacaoResource(resources.ModelResource):
    class Meta:
        model = Notificacao
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'mensagem', 'data_hora', 'denuncia')

@admin.register(Notificacao)
class NotificacaoAdmin(ImportExportModelAdmin):
    resource_class = NotificacaoResource
    list_display = ('id', 'denuncia', 'data_hora')
    search_fields = ('mensagem',)
    ordering = ['-data_hora']
    readonly_fields = ('data_hora',)
    fieldsets = (
        ('Notificação', {
            'fields': ('denuncia', 'mensagem', 'data_hora')
        }),
    )

# ----------------------------
# Midia
# ----------------------------
class MidiaResource(resources.ModelResource):
    class Meta:
        model = Midia
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'tipo', 'url_arquivo', 'denuncia')

@admin.register(Midia)
class MidiaAdmin(ImportExportModelAdmin):
    resource_class = MidiaResource
    list_display = ('id', 'tipo', 'url_arquivo', 'denuncia')
    list_filter = ('tipo',)
    search_fields = ('url_arquivo',)
    ordering = ['denuncia']
    fieldsets = (
        ('Mídia', {
            'fields': ('tipo', 'url_arquivo', 'denuncia')
        }),
    )
