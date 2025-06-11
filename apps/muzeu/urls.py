from apps.muzeu.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('item-acervo/', ItemAcervoView.as_view(), name='item_acervo'),
    path('patrimonio/', PatrimonioView.as_view(), name='patrimonio'),
    path('documento-historico/', DocumentoHistoricoView.as_view(), name='documento_historico')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)