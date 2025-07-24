import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from apps.core.models import Perfil
from apps.contratamuz.models import Usuario

print("=== TESTE DA VIEW DE REGISTRO ===")

# Criar cliente de teste
client = Client()

# Dados do usuário de teste
dados_registro = {
    'username': 'usuarioteste456',
    'email': 'usuarioteste456@example.com',
    'password': '123456',
    'password_confirm': '123456',
    'first_name': 'Usuario',
    'last_name': 'Teste',
    'nome': 'Usuario Teste 456',
    'cidade': 'São Paulo',
    'telefone': '(11) 99999-9999',
    'biografia': 'Teste de registro',
    'eh_empresa': '',
    'eh_prestador': 'on'
}

# Limpar usuário se já existir
User.objects.filter(username='usuarioteste456').delete()

try:
    # Fazer requisição POST para a view de registro
    response = client.post('/contratamuz/register/', dados_registro)
    
    print(f"Status da resposta: {response.status_code}")
    
    if response.status_code == 302:  # Redirect (sucesso)
        print("✓ Registro realizado com sucesso (redirecionamento)")
        
        # Verificar se o usuário foi criado
        user = User.objects.get(username='usuarioteste456')
        print(f"✓ Usuário Django criado: {user.username}")
        
        # Verificar se o perfil do core foi criado
        try:
            perfil = user.perfil
            print(f"✓ Perfil core criado: ID {perfil.id}")
        except:
            print("✗ Perfil core não encontrado")
        
        # Verificar se o usuário do contratamuz foi criado
        try:
            usuario = user.usuario
            print(f"✓ Usuario contratamuz criado: {usuario.nome}")
        except:
            print("✗ Usuario contratamuz não encontrado")
            
    else:
        print("✗ Falha no registro")
        print(f"Conteúdo da resposta: {response.content.decode()[:500]}...")
        
except Exception as e:
    print(f"✗ Erro no teste: {e}")
    import traceback
    traceback.print_exc()

print("\n=== TESTE CONCLUÍDO ===")
