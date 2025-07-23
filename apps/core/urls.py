from apps.core.views import *
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", homepage, name="index"),
    
    path("forms/", base_forms, name="base_forms"),
    path("tabela/", base_tabela, name="base_tabela"),
    path("pagina/", base_pagina, name="base_pagina"),

    path("adotamuz/", include("apps.adotamuz.urls")),
    path("contratamuz/", include("apps.contratamuz.urls")),
    path("covamuz/", include("apps.covamuz.urls")),
    path("doamuz/", include("apps.doamuz.urls")),
    path("escambuz/", include("apps.escambuz.urls")),
    path("esportemuz/", include("apps.esportemuz.urls")),
    path("eventuz/", include("apps.eventuz.urls")),
    path("movemuz/", include("apps.movemuz.urls")),
    path("muzeu/", include("apps.muzeu.urls")),
    path("muzsaude/", include("apps.muzsaude.urls")),
    path("reclamemuz/", include("apps.reclamemuz.urls")),
    path("turismuz/", include("apps.turismuz.urls")),
]
