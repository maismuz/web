from django.db import models
from import_export import resources
from .models import Raca



class RacaResource(resources.ModelResource):
    class Meta:
        model = Raca
        skip_unchanged = True
        report_skipped = True
        fields = ('raca', 'caracteristica')


@admin.register(Raca)

class RacaAdmin(ImportExportModelAdmin):
    resource_class = RacaResource
    list_display = ('Raca','Caracteristicas')
    list_filter = ('porte')
