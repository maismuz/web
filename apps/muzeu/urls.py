from apps.muzeu.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('item-acervo/', ItemAcervoView.as_view(), name='item_acervo'),
    path('patrimonio/', PatrimonioView.as_view(), name='patrimonio'),
    path('documento-historico/', DocumentoHistoricoView.as_view(), name='documento_historico'),
    path('form-itens-acervo/', FormItensAcervoView.as_view(), name='form_itens_acervo'),
    path('form-patrimonio/', FormPatrimonioView.as_view(), name='form_patrimonio'),
    path('form-documento-historico/', FormDocumentoHistoricoView.as_view(), name='form_documento_historico'),
    path('lista-item/', FormDocumentoHistoricoView.as_view(), name='lista_item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)