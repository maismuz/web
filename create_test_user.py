#!/usr/bin/env python
"""Script para criar um usuário de teste"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.contratamuz.models import Usuario

def create_test_user():
    # Criar usuário Django
    username = 'teste'
    email = 'teste@teste.com'
    password = '123456'
    
    # Verificar se já existe
    if User.objects.filter(username=username).exists():
        print(f'Usuário {username} já existe')
        return
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='Usuário',
        last_name='Teste'
    )
    
    # Criar perfil
    usuario = Usuario.objects.create(
        user=user,
        nome='Usuário Teste',
        cidade='São Paulo',
        telefone='(11) 99999-9999',
        biografia='Usuário de teste',
        eh_empresa=False,
        eh_prestador=True
    )
    
    print(f'Usuário criado com sucesso!')
    print(f'Username: {username}')
    print(f'Password: {password}')
    print(f'Email: {email}')

if __name__ == '__main__':
    create_test_user()
