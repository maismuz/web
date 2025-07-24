import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.template.loader import get_template
from django.template import Context
from apps.contratamuz.models import Servico

try:
    # Testar se o template carrega
    template = get_template('contratamuz/servicos.html')
    print("✅ Template carregado com sucesso!")
    
    # Testar se há serviços no banco
    servicos = Servico.objects.all()
    print(f"✅ Serviços no banco: {servicos.count()}")
    
    # Testar renderização básica
    from django.http import HttpRequest
    from django.contrib.auth.models import AnonymousUser
    
    request = HttpRequest()
    request.user = AnonymousUser()
    request.GET = {}
    
    from apps.contratamuz.views import listar_servicos
    response = listar_servicos(request)
    print(f"✅ View respondeu com status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Página de serviços funcionando corretamente!")
    else:
        print(f"❌ Erro na resposta: {response.status_code}")
        
except Exception as e:
    print(f"❌ Erro encontrado: {str(e)}")
    import traceback
    traceback.print_exc()
