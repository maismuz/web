#!/usr/bin/env python
import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from apps.contratamuz.models import Usuario, VagaEmprego

def criar_vagas_teste():
    """Cria algumas vagas de teste"""
    
    # Criar um usuário empresa se não existir
    empresa, created = Usuario.objects.get_or_create(
        nome='Estúdio Musical ABC',
        defaults={
            'cidade': 'São Paulo',
            'telefone': '(11) 98765-4321',
            'biografia': 'Estúdio de gravação e produção musical',
            'eh_empresa': True,
            'eh_prestador': False,
        }
    )
    
    if created:
        print(f"Empresa criada: {empresa.nome}")
    else:
        print(f"Empresa já existe: {empresa.nome}")
    
    # Verificar vagas existentes
    vagas_existentes = VagaEmprego.objects.count()
    print(f"Vagas existentes: {vagas_existentes}")
    
    # Criar vagas de teste se não existirem
    if vagas_existentes == 0:
        vagas_teste = [
            {
                'titulo': 'Músico Freelancer',
                'descricao': 'Procuramos músico experiente para projetos diversos.',
                'categoria': 'musica',
                'localizacao': 'São Paulo, SP',
                'salario': 2500.00,
                'ativa': True,
            },
            {
                'titulo': 'Técnico de Som',
                'descricao': 'Vaga para técnico de som em estúdio de gravação.',
                'categoria': 'audio',
                'localizacao': 'Rio de Janeiro, RJ',
                'salario': 3000.00,
                'ativa': True,
            },
            {
                'titulo': 'Professor de Violão',
                'descricao': 'Professor de violão para escola de música.',
                'categoria': 'ensino',
                'localizacao': 'Belo Horizonte, MG',
                'salario': 2000.00,
                'ativa': True,
            },
        ]
        
        for vaga_data in vagas_teste:
            vaga = VagaEmprego.objects.create(
                usuario=empresa,
                **vaga_data
            )
            print(f"Vaga criada: {vaga.titulo}")
    
    # Verificar total final
    total_vagas = VagaEmprego.objects.count()
    vagas_ativas = VagaEmprego.objects.filter(ativa=True).count()
    
    print(f"\nResumo:")
    print(f"Total de vagas: {total_vagas}")
    print(f"Vagas ativas: {vagas_ativas}")
    
    # Listar todas as vagas
    print(f"\nListando vagas:")
    for vaga in VagaEmprego.objects.all():
        print(f"- {vaga.titulo} ({vaga.categoria}) - Ativa: {vaga.ativa}")

if __name__ == '__main__':
    criar_vagas_teste()
