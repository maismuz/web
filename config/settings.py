"""
Configurações Django para o projeto.

Este arquivo contém todas as configurações necessárias para o funcionamento do projeto.
Para mais informações, consulte: 
https://docs.djangoproject.com/en/4.2/topics/settings/
"""

import os
from datetime import timedelta
from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages
from import_export.formats.base_formats import CSV, XLSX
from django.utils.translation import gettext_lazy as _

# Construir caminhos dentro do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# AVISO: mantenha a chave secreta em segredo!
# Variáveis de ambiente carregadas do .env
SECRET_KEY = config('SECRET_KEY')

# Credenciais de banco de dados a partir de variáveis de ambiente
DB_CREDENTIALS = {
    'NAME': config('DB_NAME'),
    'USER': config('DB_USER'),
    'PASSWORD': config('DB_PASSWORD'),
    'HOST': config('DB_HOST'),
    'PORT': config('DB_PORT'),
}

# AVISO: Não use DEBUG = True em produção!
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos e origens CSRF confiáveis
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'vps58279.publiccloud.com.br',
]

CSRF_TRUSTED_ORIGINS = [
    'https://*',
    'http://*'
]

# Configurações de banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_CREDENTIALS['NAME'],
        'USER': DB_CREDENTIALS['USER'],
        'PASSWORD': DB_CREDENTIALS['PASSWORD'],
        'HOST': DB_CREDENTIALS['HOST'],
        'PORT': DB_CREDENTIALS['PORT'],
    }
}

# Definições da aplicação
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'apps.adotamuz',
    'apps.contratamuz',
    'apps.core',
    'apps.covamuz',
    'apps.doamuz',
    'apps.escambuz',
    'apps.esportemuz',
    'apps.eventuz',
    'apps.movemuz',
    'apps.muzsaude',
    'apps.muzeu',
    'apps.reclamemuz',
    'apps.teste',
    'apps.turismuz',
]

THIRD_PARTY_APPS = [
    'nested_admin',
    'crispy_forms',
    'crispy_bootstrap5',
    'import_export',
    'django_filters',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

# Crispy Forms settings
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
NPM_STATIC_FILES_PREFIX = 'node_modules'

# Configuração de middlewares
DJANGO_MIDDLEWARES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PROJECT_MIDDLEWARES = [
    # '',
]

THIRD_PARTY_MIDDLEWARES = [
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
]

MIDDLEWARE = DJANGO_MIDDLEWARES + PROJECT_MIDDLEWARES + THIRD_PARTY_MIDDLEWARES

# Configuração de URL
ROOT_URLCONF = 'config.urls'

# Configuração de templates
TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, f"apps/{app}/templates/")
    for app in [
        'adotamuz', 'contratamuz', 'core', 'covamuz', 'doamuz',
        'escambuz', 'esportemuz', 'eventuz', 'movemuz', 'muzeu',
        'muzsaude', 'reclamemuz', 'teste', 'turismuz',
    ]
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"

# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Configuração de arquivos estáticos (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Diretórios de arquivos estáticos adicionais
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, f"apps/{app}/static/")
    for app in [
        'adotamuz', 'contratamuz', 'core', 'covamuz', 'doamuz',
        'escambuz', 'esportemuz', 'eventuz', 'movemuz', 'muzeu',
        'muzsaude', 'reclamemuz', 'teste', 'turismuz',
    ]
]

# Configurações de Import / Export
IMPORT_FORMATS = [CSV, XLSX]
EXPORT_FORMATS = [CSV, XLSX]

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Configuração de arquivos de mídia
# SITE_URL = ''
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Padrão para chave primária automática
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL de login
# LOGIN_URL = '/'
# URL de logout
# LOGOUT_URL = '/logout/'