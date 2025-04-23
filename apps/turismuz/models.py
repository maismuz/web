from django.db import models


class Publicacao(models.Model){ 
    titulo = models.CharField(max_length=255, verbose_name='Título da Publicação', help_text='Título que aparecerá no card de sua publicação.')
    texto_da_noticia = models.TextField(verbose_name = 'Texto da Publicação', help_text = 'Texto que aparecerá no corpo de sua publicação')
    # imagens
    data_de_publicacao = models.DateTimeField(auto_now_add = True, verbose_name='Data de Publicação')

}