from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Animal

class AnimalResource(resources.ModelResource):
    class Meta:
        model = Animal
        skip_unchanged = True
        report_skipped = True
        fields = ('nome', 'porte', 'raca', 'cor', 'localizacao', 'foto', 'descricao')

@admin.register(Animal)
class AnimalAdmin(ImportExportModelAdmin):
    resource_class = AnimalResource
    list_display = ('nome', 'porte', 'cor', 'localizacao')
    list_filter = ('porte', 'cor', 'localizacao')
    search_fields = ('nome', 'raca', 'descricao', 'localizacao') 
    fieldsets = (
        ('Informações do Animal', {
            'fields': ('nome', 'foto', 'cor', 'porte', 'raca', 'localizacao', 'descricao')
        }),
    )