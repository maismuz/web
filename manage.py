import sys
import os

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. Tem certeza de que ele está instalado e "
            "disponível na sua variável de ambiente PYTHONPATH? Você "
            "esqueceu de ativar um ambiente virtual?"
        ) from exc

    # Adiciona o diretório 'apps' ao sys.path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(BASE_DIR, 'apps'))

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()