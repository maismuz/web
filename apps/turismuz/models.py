from django.db import models


class Categorias(models.Model):
    """
    Modelo para controle de categorias.
    """
    nome = models.CharField(
        verbose_name='Nome',
        help_text='Nome da categoria',
        max_length=100
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Estabelecimentos(models.Model):
    """
    Modelo para controle de estabelecimentos.
    """
    nome = models.CharField(
        verbose_name='Nome',
        help_text='Nome do estabelecimento',
        max_length=100
    )
    categoria = models.ForeignKey(
        Categorias,
        verbose_name='Categoria',
        help_text='Categoria do estabelecimento',
        on_delete=models.CASCADE
    )
    endereco = models.CharField(
        verbose_name='Endereço',
        help_text='Endereço do estabelecimento',
        max_length=200,
        blank=True,
        null=True
    )
    contato = models.CharField(
        verbose_name='Contato',
        help_text='Telefone, e-mail ou outro contato',
        max_length=100,
        blank=True,
        null=True
    )
    horario_funcionamento = models.CharField(
        verbose_name='Horário de Funcionamento',
        help_text='Horário de funcionamento do estabelecimento',
        max_length=100,
        blank=True,
        null=True
    )
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição do estabelecimento',
        blank=True,
        null=True
    )
   

    class Meta:
        verbose_name = 'Estabelecimento'
        verbose_name_plural = 'Estabelecimentos'
        ordering = ['nome']

    def __str__(self):
        return self.nome

class GuiasTurismo(models.Model):
    """
    Modelo para controle de guias de turismo.
    """
    nome = models.CharField(
        verbose_name='Nome do Guia',
        help_text='Nome do guia de turismo',
        max_length=100
    )
    nome_tour = models.CharField(
        verbose_name='Nome do Tour',
        help_text='Nome do tour',
        max_length=150
    )
    descricao = models.TextField(
        verbose_name='Descrição do Guia',
        help_text='Descrição do guia de turismo',
        blank=True,
        null=True
    )
    descricao_tour = models.TextField(
        verbose_name='Descrição do Tour',
        help_text='Descrição do tour',
        blank=True,
        null=True
    )
    duracao = models.DurationField(
        verbose_name='Duração',
        help_text='Duração do tour (hh:mm:ss)',
        blank=True,
        null=True
    )
    pontos_parada = models.TextField(
        verbose_name='Pontos de Parada',
        help_text='Lista dos pontos de parada do tour (um por linha)',
        blank=True,
        null=True
    )
    nivel_dificuldade = models.CharField(
        verbose_name='Nível de Dificuldade',
        help_text='Nível de dificuldade do tour',
        max_length=50,
        blank=True,
        null=True
    )
    valor = models.DecimalField(
        verbose_name='Valor',
        help_text='Valor do tour',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    entidades_responsaveis = models.CharField(
        verbose_name='Entidades Responsáveis',
        help_text='Entidades responsáveis pelo tour',
        max_length=200,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Guia de Turismo'
        verbose_name_plural = 'Guias de Turismo'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.nome_tour}"

class Publicacao(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Título da Publicação', help_text='Título que aparecerá no card de sua publicação.')
    texto_da_noticia = models.TextField(verbose_name = 'Texto da Publicação', help_text = 'Texto que aparecerá no corpo de sua publicação')
    data_de_publicacao = models.DateTimeField(auto_now_add = True, verbose_name='Data de Publicação')
    imagem = models.ImageField(upload_to='imagens_publicacoes/', verbose_name='Imagem da Publicação', help_text='Imagem que aparecerá no card de sua publicação.')
class Avaliacao(models.Model):
    nota = models.PositiveSmallIntegerField(
        verbose_name='Nota',
        help_text='Nota da avaliação (1 a 5)'
    )
    comentario = models.TextField(
        verbose_name='Comentário',
        help_text='Comentário da avaliação',
        blank=True,
        null=True
    )
    data = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data da Avaliação'
    )
    usuario = models.CharField(
        max_length=100,
        verbose_name='Usuário',
        help_text='Nome do usuário que avaliou'
    )

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-data']

    def __str__(self):
        return f"{self.usuario} - Nota: {self.nota}"



