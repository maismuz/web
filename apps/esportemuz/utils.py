from apps.esportemuz.models import *
from django.utils.timezone import now
from hashlib import sha256
import os

# Create your functions here.
def gerar_nome_arquivo(instance, folder, filename):
    """
    Gera um nome de arquivo único para o upload de imagens, baseado no timestamp atual e no nome original do arquivo.
    """
    ext = os.path.splitext(filename)[1]
    hashed_filename = sha256(f'{filename}{now().timestamp()}'.encode('utf-8')).hexdigest()

    return os.path.join(folder, f'{hashed_filename}{ext}')

def formatar_nome_legivel(text):
    """
    Formata um nome para ser mais legível, substituindo underscores por espaços e capitalizando as palavras.
    """
    return text if not isinstance(text, str) else ' '.join(word.title() for word in text.split('_'))