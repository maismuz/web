from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome da categoria", help_text="Nome da categoria do item")
    descricao = models.TextField(verbose_name="Descrição da categoria", help_text="Descrição da categoria do item")

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

class ItemAcervo(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do item", help_text="Nome do item do acervo")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name="Categoria do item", help_text="Categoria do item do acervo")
    descricao = models.TextField(verbose_name="Descrição do item", help_text="Descrição do item do acervo")
    origem = models.CharField(max_length=255, verbose_name="Origem do item", help_text="Origem do item do acervo")
    data_adicao = models.DateTimeField(default=timezone.now, verbose_name="Data de adição", help_text="Data em que o item foi adicionado ao acervo", blank=True, null=True)
    usuario_adicionado = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário que adicionou", help_text="Usuário que adicionou o item ao acervo")

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Item do Acervo"
        verbose_name_plural = "Itens do Acervo"
        ordering = ['nome']

class ImagemItemAcervo(models.Model):
    item_acervo = models.ForeignKey(ItemAcervo, on_delete=models.PROTECT, verbose_name="Item do acervo", help_text="Item do acervo relacionado à imagem")
    imagem = models.ImageField(upload_to='imagens_acervo/', verbose_name="Imagem do item", help_text="Imagem do item do acervo")

    def __str__(self):
        return f"Imagem de {self.item_acervo.nome}"
    class Meta:
        verbose_name = "Imagem do Item do Acervo"
        verbose_name_plural = "Imagens dos Itens do Acervo"
        ordering = ['item_acervo__nome']

class Patrimonio(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do patrimônio", help_text="Nome do patrimônio")
    descricao = models.TextField(verbose_name="Descrição do patrimônio", help_text="Descrição do patrimônio")
    data_origem = models.DateField(verbose_name="Data de origem", help_text="Data de origem do patrimônio", blank=True, null=True)
    localizacao = models.CharField(max_length=255, verbose_name="Localização do patrimônio", help_text="Localização do patrimônio")
    data_adicao = models.DateTimeField(default=timezone.now, verbose_name="Data de adição", help_text="Data em que o patrimônio foi adicionado ao acervo", blank=True, null=True)
    usuario_adicionado = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário que adicionou", help_text="Usuário que adicionou o patrimônio ao acervo")

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Patrimônio"
        verbose_name_plural = "Patrimônios"
        ordering = ['nome']
    
class ImagemPatrimonio(models.Model):
    patrimonio = models.ForeignKey(Patrimonio, on_delete=models.PROTECT, verbose_name="Patrimônio", help_text="Patrimônio relacionado à imagem")
    imagem = models.ImageField(upload_to='imagens_patrimonio/', verbose_name="Imagem do patrimônio", help_text="Imagem do patrimônio")

    def __str__(self):
        return f"Imagem de {self.patrimonio.nome}"
    class Meta:
        verbose_name = "Imagem do Patrimônio"
        verbose_name_plural = "Imagens dos Patrimônios"
        ordering = ['patrimonio__nome']
    
class DocumentoHistorico(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título do documento", help_text="Título do documento histórico")
    descricao = models.TextField(verbose_name="Descrição do documento", help_text="Descrição do documento histórico", blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name="Categoria do documento", help_text="Categoria do documento histórico")
    autor = models.CharField(max_length=255, verbose_name="Autor do documento", help_text="Autor do documento histórico", blank=True, null=True)
    data_origem = models.DateField(verbose_name="Data de origem", help_text="Data de origem do documento histórico", blank=True, null=True)
    documento = models.FileField(upload_to='documentos_historicos/', verbose_name="Documento", help_text="Arquivo do documento histórico")
    data_adicao = models.DateTimeField(default=timezone.now, verbose_name="Data de adição", help_text="Data em que o documento foi adicionado ao acervo", blank=True, null=True)
    usuario_adicionado = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário que adicionou", help_text="Usuário que adicionou o documento ao acervo")

    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = "Documento Histórico"
        verbose_name_plural = "Documentos Históricos"
        ordering = ['titulo']
    
