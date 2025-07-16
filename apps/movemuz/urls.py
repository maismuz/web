# config/urls.py (assuming this is your main project urls file)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('forms/', include('apps.movemuz.urls_forms')), # Corrected path
    path('tabela/', include('apps.movemuz.urls_table')), # Corrected path
    path('pagina/', include('apps.movemuz.urls_page')), # Corrected path
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Use STATIC_ROOT for staticfiles_dirs setup
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# apps/movemuz/urls.py
from django.urls import path
from . import views

app_name = 'movemuz'

urlpatterns += [
    # Homepage and main views
    path('', views.homepage_view, name='homepage'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Demo and base pages
    path('forms-demo/', views.forms_demo_view, name='forms_demo'),
    path('base-page/', views.base_page_view, name='base_page'),
    
    # Table views (CRUD operations)
    path('motoristas/', views.MotoristaTableView.as_view(), name='motoristas_table'),
    path('combustiveis/', views.CombustivelTableView.as_view(), name='combustiveis_table'),
    path('tipos-veiculo/', views.TipoVeiculoTableView.as_view(), name='tipos_veiculo_table'),
    path('veiculos/', views.VeiculoTableView.as_view(), name='veiculos_table'),
    path('locais/', views.LocalTableView.as_view(), name='locais_table'),
    path('escalas-veiculo/', views.EscalaVeiculoTableView.as_view(), name='escalas_veiculo_table'),
    path('horarios-transporte/', views.HorarioTransporteTableView.as_view(), name='horarios_transporte_table'),
    path('viagens/', views.ViagemTableView.as_view(), name='viagens_table'),
    path('passageiros/', views.PassageiroTableView.as_view(), name='passageiros_table'),
    path('pontos/', views.PontoTableView.as_view(), name='pontos_table'),
    path('paradas/', views.ParadaTableView.as_view(), name='paradas_table'),
    path('ocupacao-veiculos/', views.OcupacaoVeiculoTableView.as_view(), name='ocupacao_veiculos_table'),
    
    # Detail views
    path('motoristas/<uuid:pk>/', views.motorista_detail_view, name='motorista_detail'),
    path('veiculos/<uuid:pk>/', views.veiculo_detail_view, name='veiculo_detail'),
    path('viagens/<uuid:pk>/', views.viagem_detail_view, name='viagem_detail'),
    
    # API endpoints for AJAX requests
    path('api/motoristas-disponiveis/', views.api_motoristas_disponiveis, name='api_motoristas_disponiveis'),
    path('api/veiculos-disponiveis/', views.api_veiculos_disponiveis, name='api_veiculos_disponiveis'),
]
