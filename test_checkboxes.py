import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from apps.contratamuz.models import Usuario

print("=== TESTE DE SALVAMENTO DOS CHECKBOXES ===")

# Criar usuário de teste se não existir
username = 'teste_checkbox'
try:
    user = User.objects.get(username=username)
    print(f"Usando usuário existente: {user.username}")
except User.DoesNotExist:
    user = User.objects.create_user(
        username=username,
        email='teste@checkbox.com',
        password='123456',
        first_name='Teste',
        last_name='Checkbox'
    )
    print(f"Criado novo usuário: {user.username}")

# Criar ou obter perfil do usuário
try:
    usuario = user.usuario
    print(f"Usando perfil existente: {usuario.nome}")
except:
    usuario = Usuario.objects.create(
        user=user,
        nome='Teste Checkbox',
        cidade='São Paulo',
        telefone='(11) 99999-9999',
        biografia='Teste para checkboxes',
        eh_empresa=False,
        eh_prestador=False
    )
    print(f"Criado novo perfil: {usuario.nome}")

print(f"Estado inicial -> Empresa: {usuario.eh_empresa}, Prestador: {usuario.eh_prestador}")

# Criar cliente e fazer login
client = Client()
client.login(username=username, password='123456')

# Testar salvamento com checkboxes marcados
dados_perfil = {
    'first_name': 'Teste',
    'last_name': 'Checkbox Atualizado',
    'email': 'teste_atualizado@checkbox.com',
    'nome': 'Teste Checkbox Atualizado',
    'cidade': 'Rio de Janeiro',
    'telefone': '(21) 88888-8888',
    'biografia': 'Biografia atualizada para teste',
    'eh_empresa': 'on',  # Marcado
    'eh_prestador': 'on'  # Marcado
}

try:
    response = client.post('/contratamuz/perfil/', dados_perfil)
    print(f"Status da resposta: {response.status_code}")
    
    if response.status_code == 302:  # Redirect (sucesso)
        print("✓ Redirecionamento realizado (indica sucesso)")
        
        # Recarregar o usuário do banco
        usuario.refresh_from_db()
        print(f"Estado após POST -> Empresa: {usuario.eh_empresa}, Prestador: {usuario.eh_prestador}")
        
        if usuario.eh_empresa and usuario.eh_prestador:
            print("✅ SUCESSO: Checkboxes foram salvos corretamente!")
        else:
            print("❌ FALHA: Checkboxes não foram salvos")
            
        # Testar desmarcar os checkboxes
        dados_perfil2 = dados_perfil.copy()
        del dados_perfil2['eh_empresa']  # Desmarcado
        del dados_perfil2['eh_prestador']  # Desmarcado
        
        response2 = client.post('/contratamuz/perfil/', dados_perfil2)
        usuario.refresh_from_db()
        print(f"Estado após desmarcar -> Empresa: {usuario.eh_empresa}, Prestador: {usuario.eh_prestador}")
        
        if not usuario.eh_empresa and not usuario.eh_prestador:
            print("✅ SUCESSO: Desmarcação dos checkboxes funcionou!")
        else:
            print("❌ FALHA: Desmarcação não funcionou")
            
    else:
        print("❌ FALHA: Não houve redirecionamento")
        
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()

print("\n=== TESTE CONCLUÍDO ===")
