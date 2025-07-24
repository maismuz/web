import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from apps.contratamuz.views import listar_servicos
from apps.contratamuz.models import Servico

# Criar factory para request
factory = RequestFactory()
User = get_user_model()

print("=== TESTE DE DEBUG PARA SERVIÇOS ===")

# 1. Verificar quantos serviços existem
total_servicos = Servico.objects.count()
print(f"Total de serviços no banco: {total_servicos}")

if total_servicos > 0:
    print("\nPrimeiros 5 serviços:")
    for servico in Servico.objects.all()[:5]:
        print(f"- ID: {servico.id}, Título: {servico.titulo}, Usuário: {servico.usuario}")

# 2. Testar a view
print("\n=== TESTANDO A VIEW ===")
try:
    request = factory.get('/contratamuz/servicos/')
    response = listar_servicos(request)
    print(f"Status da resposta: {response.status_code}")
    
    if hasattr(response, 'context_data'):
        context = response.context_data
        print(f"Contexto disponível: {list(context.keys())}")
        
        if 'page_obj' in context:
            page_obj = context['page_obj']
            print(f"Página atual: {page_obj.number}")
            print(f"Total de páginas: {page_obj.paginator.num_pages}")
            print(f"Itens na página atual: {len(page_obj.object_list)}")
        
        if 'total_servicos' in context:
            print(f"Total serviços no contexto: {context['total_servicos']}")
            
except Exception as e:
    print(f"Erro ao testar view: {e}")
    import traceback
    traceback.print_exc()

print("\n=== TESTE CONCLUÍDO ===")
