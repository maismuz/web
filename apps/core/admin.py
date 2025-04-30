from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from .models import Perfil, Endereco, InformacaoProfissional, RedeSocial

class EnderecoResource(resources.ModelResource):
    class Meta:
        model = Endereco
        fields = ('id', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep')

class InformacaoProfissionalResource(resources.ModelResource):
    class Meta:
        model = InformacaoProfissional
        fields = ('id', 'profissao', 'bio')

class RedeSocialResource(resources.ModelResource):
    class Meta:
        model = RedeSocial
        fields = ('id', 'linkedin', 'website')

class PerfilResource(resources.ModelResource):
    """
    Recurso para importação e exportação de dados do modelo Perfil.
    """
    nome_usuario = Field(attribute='usuario__username', column_name='nome_usuario')
    email = Field(attribute='usuario__email', column_name='email')
    nome_completo = Field(column_name='nome_completo')
    idade = Field(column_name='idade')

    def dehydrate_nome_completo(self, perfil):
        return perfil.usuario.get_full_name() if perfil.usuario.get_full_name() else perfil.usuario.username

    def dehydrate_idade(self, perfil):
        return perfil.get_idade() if hasattr(perfil, 'get_idade') and perfil.get_idade() else '-'

    class Meta:
        model = Perfil
        fields = ('id', 'nome_usuario', 'email', 'nome_completo', 'telefone', 'cpf', 
                  'data_nascimento', 'idade', 'endereco', 'informacao_profissional', 'rede_social')
        export_order = fields

@admin.register(Endereco)
class EnderecoAdmin(ImportExportModelAdmin):
    resource_class = EnderecoResource
    list_display = ('logradouro', 'numero', 'bairro', 'cidade', 'estado', 'cep')
    search_fields = ('logradouro', 'bairro', 'cidade', 'cep')
    list_filter = ('estado', 'cidade')

@admin.register(InformacaoProfissional)
class InformacaoProfissionalAdmin(ImportExportModelAdmin):
    resource_class = InformacaoProfissionalResource
    list_display = ('profissao',)
    search_fields = ('profissao', 'bio')

@admin.register(RedeSocial)
class RedeSocialAdmin(ImportExportModelAdmin):
    resource_class = RedeSocialResource
    list_display = ('linkedin', 'website')

class PerfilAdmin(ImportExportModelAdmin):
    """
    Configuração da interface administrativa para o modelo Perfil.
    """
    resource_class = PerfilResource
    
    # Campos exibidos na listagem
    list_display = ('foto_preview', 'nome_completo', 'email_usuario', 'telefone', 
                   'idade_usuario', 'get_cidade_estado', 'get_profissao')
    
    # Filtros laterais
    list_filter = ('genero', 'endereco__estado', 'data_criacao')
    
    # Campos de pesquisa
    search_fields = ('usuario__username', 'usuario__email', 'usuario__first_name', 
                    'usuario__last_name', 'cpf', 'telefone', 'endereco__cidade')
    
    # Agrupamento de campos em fieldsets
    fieldsets = (
        (_('Informações do Usuário'), {
            'fields': ('usuario', 'foto', 'foto_preview', 'genero')
        }),
        (_('Informações de Contato'), {
            'fields': ('telefone',)
        }),
        (_('Documentos'), {
            'fields': ('cpf', 'rg')
        }),
        (_('Relacionamentos'), {
            'fields': ('endereco', 'informacao_profissional', 'rede_social')
        }),
        (_('Datas'), {
            'fields': ('data_nascimento', 'data_criacao', 'data_atualizacao')
        }),
    )
    
    # Campos somente leitura
    readonly_fields = ('foto_preview', 'data_criacao', 'data_atualizacao')
    
    # Ordenações disponíveis
    ordering = ('-data_atualizacao',)
    
    # Número de itens por página
    list_per_page = 25
    
    def foto_preview(self, obj):
        """Exibe uma miniatura da foto do perfil na lista e em detalhes."""
        if obj.foto:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.foto.url)
        return format_html('<span style="color: #999;">Sem foto</span>')
    foto_preview.short_description = _('Foto')
    
    def nome_completo(self, obj):
        """Exibe o nome completo do usuário ou o nome de usuário se não houver nome completo."""
        nome = obj.usuario.get_full_name()
        if nome:
            return nome
        return obj.usuario.username
    nome_completo.short_description = _('Nome')
    nome_completo.admin_order_field = 'usuario__first_name'
    
    def email_usuario(self, obj):
        """Exibe o e-mail do usuário."""
        return obj.usuario.email
    email_usuario.short_description = _('E-mail')
    email_usuario.admin_order_field = 'usuario__email'
    
    def idade_usuario(self, obj):
        """Calcula e exibe a idade do usuário."""
        if hasattr(obj, 'get_idade') and obj.get_idade():
            return f"{obj.get_idade()} anos"
        return '-'
    idade_usuario.short_description = _('Idade')
    
    def get_cidade_estado(self, obj):
        """Exibe a cidade e o estado juntos."""
        if obj.endereco:
            return f"{obj.endereco.cidade}/{obj.endereco.estado}"
        return '-'
    get_cidade_estado.short_description = _('Localização')
    
    def get_profissao(self, obj):
        """Exibe a profissão do usuário."""
        if obj.informacao_profissional:
            return obj.informacao_profissional.profissao
        return '-'
    get_profissao.short_description = _('Profissão')

    def get_queryset(self, request):
        """Otimiza a consulta para reduzir o número de queries SQL."""
        queryset = super().get_queryset(request)
        return queryset.select_related('usuario', 'endereco', 'informacao_profissional', 'rede_social')

# Extendendo a visualização padrão do User para mostrar link para o Perfil
class CustomUserAdmin(UserAdmin):
    """Customização do admin padrão de usuários para mostrar link para o perfil."""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'ver_perfil')
    
    def ver_perfil(self, obj):
        """Adiciona um link para o perfil do usuário, se existir."""
        try:
            if hasattr(obj, 'perfil'):
                return format_html('<a href="{}">{}</a>', 
                                  f'/admin/core/perfil/{obj.perfil.id}/change/', 
                                  _('Ver perfil'))
            return _('Sem perfil')
        except Perfil.DoesNotExist:
            return _('Sem perfil')
    ver_perfil.short_description = _('Perfil')

# Registrando os modelos no admin
admin.site.register(Perfil, PerfilAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
