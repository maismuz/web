#!/usr/bin/env python
"""
Script para popular o banco de dados com dados de exemplo
Execute: python populate_db.py
"""

import os
import sys

from config.settings import BASE_DIR
sys.path.append(os.path.join(BASE_DIR, 'apps'))
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.eventuz.models import *

def criar_categorias():
    """Cria categorias de exemplo"""
    categorias = [
        'Música',
        'Esporte',
        'Cultura',
        'Tecnologia',
        'Educação',
        'Gastronomia',
        'Arte',
        'Negócios',
        'Saúde',
        'Entretenimento'
    ]
    
    for nome in categorias:
        categoria, created = Categoria.objects.get_or_create(nome=nome)
        if created:
            print(f"Categoria criada: {nome}")
        else:
            print(f"Categoria já existe: {nome}")

def criar_eventos_exemplo():
    """Cria eventos de exemplo"""
    categorias = list(Categoria.objects.all())
    
    if not categorias:
        print("Erro: Nenhuma categoria encontrada. Execute criar_categorias() primeiro.")
        return
    
    eventos_exemplo = [
        {
            'nome': 'Festival de Música Eletrônica 2024',
            'data_hora': timezone.now() + timedelta(days=30),
            'local': 'Parque Villa-Lobos, São Paulo - SP',
            'descricao': 'O maior festival de música eletrônica do Brasil está de volta! Três dias de muita música com os melhores DJs nacionais e internacionais. Prepare-se para uma experiência única com shows inesquecíveis, food trucks e muito mais.',
            'organizador': 'EventMusic Produções',
            'cnpj': '12.345.678/0001-90',
            'contato': '(11) 99999-9999 | contato@eventmusic.com.br',
            'categoria': categorias[0],  # Música
            'aprovado': True
        },
        {
            'nome': 'Maratona de São Paulo 2024',
            'data_hora': timezone.now() + timedelta(days=45),
            'local': 'Ibirapuera, São Paulo - SP',
            'descricao': 'A tradicional Maratona de São Paulo está chegando! Participe desta corrida histórica que percorre os principais pontos turísticos da cidade. Inscrições abertas para 42km, 21km e 5km.',
            'organizador': 'Federação Paulista de Atletismo',
            'cnpj': '98.765.432/0001-10',
            'contato': '(11) 88888-8888 | inscricoes@maratonasp.com.br',
            'categoria': categorias[1],  # Esporte
            'aprovado': True
        },
        {
            'nome': 'Conferência de Tecnologia TechSP',
            'data_hora': timezone.now() + timedelta(days=15),
            'local': 'Centro de Convenções Frei Caneca, São Paulo - SP',
            'descricao': 'A maior conferência de tecnologia do estado de São Paulo. Palestras sobre IA, desenvolvimento web, mobile, DevOps e muito mais. Networking com profissionais da área e empresas de tecnologia.',
            'organizador': 'TechSP Eventos',
            'cnpj': '11.222.333/0001-44',
            'contato': '(11) 77777-7777 | info@techsp.com.br',
            'categoria': categorias[3],  # Tecnologia
            'aprovado': True
        },
        {
            'nome': 'Exposição de Arte Contemporânea',
            'data_hora': timezone.now() + timedelta(days=7),
            'local': 'Museu de Arte Moderna, São Paulo - SP',
            'descricao': 'Exposição inédita com obras de artistas contemporâneos brasileiros e internacionais. Uma jornada através das diferentes expressões artísticas do século XXI.',
            'organizador': 'Museu de Arte Moderna',
            'cnpj': '55.666.777/0001-88',
            'contato': '(11) 66666-6666 | exposicoes@mam.org.br',
            'categoria': categorias[6],  # Arte
            'aprovado': True
        },
        {
            'nome': 'Workshop de Culinária Italiana',
            'data_hora': timezone.now() + timedelta(days=20),
            'local': 'Instituto Culinário Italiano, São Paulo - SP',
            'descricao': 'Aprenda a preparar pratos tradicionais da culinária italiana com chefs especializados. Inclui degustação e certificado de participação.',
            'organizador': 'Instituto Culinário Italiano',
            'cnpj': '33.444.555/0001-66',
            'contato': '(11) 55555-5555 | cursos@culinariaitalia.com.br',
            'categoria': categorias[5],  # Gastronomia
            'aprovado': True
        },
        # Eventos passados (histórico)
        {
            'nome': 'Rock in Rio São Paulo 2023',
            'data_hora': timezone.now() - timedelta(days=60),
            'local': 'Cidade do Rock, São Paulo - SP',
            'descricao': 'O maior festival de rock do mundo aconteceu em São Paulo com shows inesquecíveis de bandas nacionais e internacionais.',
            'organizador': 'Rock World',
            'cnpj': '99.888.777/0001-55',
            'contato': '(11) 44444-4444 | info@rockinrio.com.br',
            'categoria': categorias[0],  # Música
            'aprovado': True
        },
        {
            'nome': 'Copa do Mundo de Futebol Feminino',
            'data_hora': timezone.now() - timedelta(days=90),
            'local': 'Estádio do Morumbi, São Paulo - SP',
            'descricao': 'Partida histórica da Copa do Mundo de Futebol Feminino realizada em São Paulo.',
            'organizador': 'FIFA Brasil',
            'cnpj': '77.666.555/0001-33',
            'contato': '(11) 33333-3333 | brasil@fifa.com',
            'categoria': categorias[1],  # Esporte
            'aprovado': True
        }
    ]
    
    for evento_data in eventos_exemplo:
        evento, created = Evento.objects.get_or_create(
            nome=evento_data['nome'],
            defaults=evento_data
        )
        if created:
            print(f"Evento criado: {evento.nome}")
        else:
            print(f"Evento já existe: {evento.nome}")

def main():
    """Função principal"""
    print("=== Populando banco de dados ===")
    print()
    
    print("1. Criando categorias...")
    criar_categorias()
    print()
    
    print("2. Criando eventos de exemplo...")
    criar_eventos_exemplo()
    print()
    
    print("=== Concluído! ===")
    print()
    print("Dados criados:")
    print(f"- Categorias: {Categoria.objects.count()}")
    print(f"- Eventos: {Evento.objects.count()}")
    print(f"- Eventos aprovados: {Evento.objects.aprovados().count()}")
    print(f"- Eventos ativos: {Evento.objects.ativos().count()}")
    print(f"- Eventos histórico: {Evento.objects.historico().count()}")

if __name__ == '__main__':
    main()

