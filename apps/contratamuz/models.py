from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    """Modelo para representar usuários do sistema"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario', null=True, blank=True)
    nome = models.CharField(max_length=100, verbose_name="Nome")
    cidade = models.CharField(max_length=100, verbose_name="Cidade", blank=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone", blank=True)
    biografia = models.TextField(blank=True, verbose_name="Biografia")
    imagem = models.ImageField(
        upload_to='usuarios/', 
        blank=True, 
        null=True, 
        verbose_name="Foto de Perfil"
    )
    eh_empresa = models.BooleanField(default=False, verbose_name="É Empresa")
    eh_prestador = models.BooleanField(default=True, verbose_name="É Prestador")
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['-id']
    
    def __str__(self):
        return self.nome
    
    @property
    def imagem_url(self):
        """Retorna a URL da imagem ou uma imagem padrão"""
        if self.imagem and hasattr(self.imagem, 'url'):
            return self.imagem.url
        return '/static/img/default-user.svg'


class Servico(models.Model):
    """Modelo para representar serviços oferecidos"""
    
    CATEGORIAS_CHOICES = [
        ('musica', 'Música'),
        ('fotografia', 'Fotografia'),
        ('video', 'Vídeo'),
        ('design', 'Design'),
        ('eventos', 'Eventos'),
        ('educacao', 'Educação'),
        ('tecnologia', 'Tecnologia'),
        ('consultoria', 'Consultoria'),
        ('outros', 'Outros'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    categoria = models.CharField(
        max_length=100, 
        choices=CATEGORIAS_CHOICES, 
        default='outros',
        verbose_name="Categoria"
    )
    contato = models.CharField(max_length=20, verbose_name="Telefone de Contato", blank=True)
    telefone_contato = models.CharField(max_length=20, verbose_name="Telefone de Contato", blank=True)
    imagem = models.ImageField(
        upload_to='servicos/', 
        blank=True, 
        null=True, 
        verbose_name="Imagem do Serviço"
    )
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='servicos',
        verbose_name="Prestador"
    )
    
    criado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ['-id']
    
    def __str__(self):
        return self.titulo
    
    @property
    def imagem_url(self):
        """Retorna a URL da imagem ou uma imagem padrão"""
        if self.imagem and hasattr(self.imagem, 'url'):
            return self.imagem.url
        return '/static/img/default-service.svg'
    
    @property
    def descricao_curta(self):
        """Retorna uma versão curta da descrição para cards"""
        if len(self.descricao) > 100:
            return self.descricao[:100] + '...'
        return self.descricao
    
    def get_categoria_display_icon(self):
        """Retorna o ícone correspondente à categoria"""
        icons = {
            'musica': 'music',
            'fotografia': 'camera',
            'video': 'video',
            'design': 'palette',
            'eventos': 'calendar',
            'educacao': 'book',
            'tecnologia': 'laptop',
            'consultoria': 'briefcase',
            'outros': 'more-horizontal',
        }
        return icons.get(self.categoria, 'more-horizontal')

    @property
    def nota_media(self):
        avaliacoes = self.avaliacoes.all()
        if avaliacoes.exists():
            return round(sum([a.nota for a in avaliacoes]) / avaliacoes.count(), 1)
        return None


class VagaEmprego(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='vagas')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    localizacao = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Vaga de Emprego'
        verbose_name_plural = 'Vagas de Emprego'
    

class Candidatura(models.Model):
    STATUS_CANDIDATURA = [
        ('pendente', 'Pendente'),
        ('aceita', 'Aceita'),
        ('rejeitada', 'Rejeitada'),
    ]

    candidato = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='candidaturas')
    vaga = models.ForeignKey(VagaEmprego, on_delete=models.CASCADE, related_name='candidaturas')
    mensagem = models.TextField(blank=True)
    data_candidatura = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CANDIDATURA, default='pendente')

    def __str__(self):
        return f"{self.candidato.nome} -> {self.vaga.titulo}"
    
    class Meta:
        verbose_name = 'Candidatura'
        verbose_name_plural = 'Candidaturas'
        

class Avaliacao(models.Model):
    serviço = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='avaliacoes')
    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes_feitas')
    nota = models.IntegerField()
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.avaliador.nome} para {self.serviço.titulo}"
    
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

