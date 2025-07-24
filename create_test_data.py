import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.contratamuz.models import Usuario, Servico

User = get_user_model()

print("=== CRIANDO DADOS DE TESTE ===")

# Verificar se já há dados
total_servicos = Servico.objects.count()
print(f"Serviços existentes: {total_servicos}")

if total_servicos == 0:
    print("Criando dados de teste...")
    
    # Criar usuário de teste se não existir
    try:
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Usuário',
                'last_name': 'Teste'
            }
        )
        if created:
            user.set_password('123456')
            user.save()
            
        # Criar perfil de usuário
        usuario, created = Usuario.objects.get_or_create(
            user=user,
            defaults={
                'nome': 'Usuário Teste',
                'telefone': '(11) 99999-9999',
                'cidade': 'São Paulo',
                'estado': 'SP',
                'eh_prestador': True
            }
        )
        
        # Criar alguns serviços de teste
        servicos_teste = [
            {
                'titulo': 'Aulas de Violão',
                'descricao': 'Aulas particulares de violão para iniciantes e intermediários. Método exclusivo desenvolvido ao longo de 10 anos de experiência.',
                'categoria': 'musica',
                'preco': 80.00
            },
            {
                'titulo': 'Mixagem e Masterização',
                'descricao': 'Serviços profissionais de mixagem e masterização para artistas independentes. Qualidade de estúdio.',
                'categoria': 'audio',
                'preco': 150.00
            },
            {
                'titulo': 'Produção Musical',
                'descricao': 'Produção completa de suas músicas, desde a criação até a finalização. Diversos estilos musicais.',
                'categoria': 'producao',
                'preco': 300.00
            }
        ]
        
        for servico_data in servicos_teste:
            servico, created = Servico.objects.get_or_create(
                titulo=servico_data['titulo'],
                defaults={
                    'usuario': usuario,
                    'descricao': servico_data['descricao'],
                    'categoria': servico_data['categoria'],
                    'preco': servico_data['preco']
                }
            )
            if created:
                print(f"Criado: {servico.titulo}")
        
        print(f"Total de serviços após criação: {Servico.objects.count()}")
        
    except Exception as e:
        print(f"Erro ao criar dados: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Dados já existem, não é necessário criar novos.")

print("=== CONCLUÍDO ===")
