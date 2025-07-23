from apps.muzeu.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('item-acervo/', ItemAcervoView.as_view(), name='item-acervo'),
    path('patrimonio/<int:pk>', PatrimonioView.as_view(), name='patrimonio'),
    path('documento-historico/', DocumentoHistoricoView.as_view(), name='documento_historico'),
    path('form-itens-acervo/', ItemAcervoCreateView.as_view(), name='form_itens_acervo'),
    path('form-patrimonio/', PatrimonioCreateView.as_view(), name='form_patrimonio'),
    path('form-documento-historico/', FormDocumentoHistoricoView.as_view(), name='form_documento_historico'),
    path('lista_item/', ListaItemView.as_view(), name='lista_item'),
    path('detalhe-item-acervo/<int:pk>/', DetalheItemAcervoView.as_view(), name='detalhe_item_acervo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)