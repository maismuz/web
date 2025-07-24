import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from apps.contratamuz.models import Usuario, VagaEmprego

# Verificar se já existem vagas
print("=== VERIFICAÇÃO INICIAL ===")
total_vagas = VagaEmprego.objects.count()
print(f"Total de vagas no banco: {total_vagas}")

# Verificar usuários empresa
empresas = Usuario.objects.filter(eh_empresa=True)
print(f"Total de empresas: {empresas.count()}")

if empresas.count() == 0:
    print("Criando empresa de teste...")
    empresa = Usuario.objects.create(
        nome='Estúdio Musical Teste',
        cidade='São Paulo',
        telefone='(11) 98765-4321',
        biografia='Estúdio de teste para vagas',
        eh_empresa=True,
        eh_prestador=False,
    )
    print(f"Empresa criada: {empresa.nome}")
else:
    empresa = empresas.first()
    print(f"Usando empresa existente: {empresa.nome}")

# Criar vagas de teste
print("\n=== CRIANDO VAGAS ===")
vagas_data = [
    {
        'titulo': 'Músico de Estúdio',
        'descricao': 'Procuramos músico experiente para gravações em estúdio.',
        'categoria': 'musica',
        'localizacao': 'São Paulo, SP',
        'salario': 2500.00,
        'ativa': True,
    },
    {
        'titulo': 'Técnico de Som',
        'descricao': 'Vaga para técnico de som com experiência em mixagem.',
        'categoria': 'audio',
        'localizacao': 'Rio de Janeiro, RJ',
        'salario': 3000.00,
        'ativa': True,
    },
    {
        'titulo': 'Professor de Piano',
        'descricao': 'Professor de piano para escola de música.',
        'categoria': 'ensino',
        'localizacao': 'Belo Horizonte, MG',
        'salario': 2000.00,
        'ativa': True,
    },
]

for vaga_info in vagas_data:
    vaga = VagaEmprego.objects.create(
        usuario=empresa,
        **vaga_info
    )
    print(f"Vaga criada: {vaga.titulo} (ID: {vaga.id})")

# Verificação final
print("\n=== VERIFICAÇÃO FINAL ===")
total_final = VagaEmprego.objects.count()
vagas_ativas = VagaEmprego.objects.filter(ativa=True).count()

print(f"Total de vagas: {total_final}")
print(f"Vagas ativas: {vagas_ativas}")

print("\n=== LISTAGEM DAS VAGAS ===")
for vaga in VagaEmprego.objects.all():
    print(f"ID: {vaga.id} | {vaga.titulo} | {vaga.categoria} | Ativa: {vaga.ativa}")

print("\n=== TESTE DA VIEW ===")
# Simular consulta da view
vagas_view = VagaEmprego.objects.filter(ativa=True).order_by('-criado_em')
print(f"Consulta da view retorna: {vagas_view.count()} vagas")

print("\nScript concluído com sucesso!")
