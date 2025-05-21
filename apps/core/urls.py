from apps.core.views import *
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Rota para o painel administrativo
    path("admin/", admin.site.urls),

    # Rotas do core
    path("", homepage, name="index"),
    path("forms/", base_forms, name="base_forms"),
    path("tabela/", base_tabela, name="base_tabela"),

    # Rota para as demais aplicações
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
