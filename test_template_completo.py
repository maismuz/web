import os
import sys
import django
from django.template.loader import get_template
from django.template import Context
from django.http import HttpRequest

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contratamuz.models import Servico, Usuario
from apps.contratamuz.views import listar_servicos
from django.test import RequestFactory

print("=== TESTE COMPLETO DO TEMPLATE ===")

# 1. Verificar se há serviços
total_servicos = Servico.objects.count()
print(f"Total serviços no banco: {total_servicos}")

# 2. Testar a view
factory = RequestFactory()
request = factory.get('/contratamuz/servicos/')

try:
    response = listar_servicos(request)
    print(f"Status code: {response.status_code}")
    
    # 3. Verificar se o template pode ser carregado
    try:
        template = get_template('contratamuz/servicos.html')
        print("Template carregado com sucesso")
        
        # Testar renderização básica
        content = response.content.decode('utf-8')
        print(f"Tamanho do conteúdo renderizado: {len(content)} caracteres")
        
        # Verificar se há conteúdo básico
        if "Serviços Disponíveis" in content:
            print("✓ Título encontrado no template")
        else:
            print("✗ Título não encontrado")
            
        if "Total de serviços:" in content:
            print("✓ Total de serviços encontrado")
        else:
            print("✗ Total de serviços não encontrado")
            
        # Mostrar uma amostra do conteúdo
        print("\n--- AMOSTRA DO CONTEÚDO RENDERIZADO ---")
        lines = content.split('\n')
        for i, line in enumerate(lines[:20]):  # Primeiras 20 linhas
            if line.strip():
                print(f"{i+1:2d}: {line.strip()}")
                
    except Exception as e:
        print(f"Erro ao carregar template: {e}")
        
except Exception as e:
    print(f"Erro na view: {e}")
    import traceback
    traceback.print_exc()

print("\n=== TESTE CONCLUÍDO ===")
