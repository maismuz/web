from django.db import models

# Create your models here.
class Categoria(models.Model):
        tipo_doação = models.CharField(max_length=100, verbose_name="Tipo de Doação")
        def __str__(self):
            return f"{self.tipo_doação}"
        class Meta:
            verbose_name = "Categoria"
            verbose_name_plural = "Categorias"
            
class Doacao(models.Model):
        titulo = models.CharField(max_length=200)
        descricao = models.TextField(help_text="Descreva o que está sendo solicitado")
        categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
        quantidade_necessaria = models.PositiveIntegerField(null=True, blank=True)
        data_criacao = models.DateTimeField(auto_now_add=True)
        foi_atendido = models.BooleanField(default=False)
        def __str__(self):
            return f"{self.titulo}"
        class Meta:
            verbose_name = "Doação"
            verbose_name_plural = "Doações"

class Feedback(models.Model):
        tipo_doação = models.CharField(max_length=100, verbose_name="Qual foi a categoria da doação?")
        mensagem = models.TextField()
        data_do_comentario = models.DateTimeField(auto_now_add=True)
        AVALIACAO_CHOICES = [(1, 'Positivo'),(2, 'Negativo'),]
        avaliacao = models.IntegerField(choices=AVALIACAO_CHOICES, default=2, verbose_name="Avaliação")

        def __str__(self):
            return f"{self.mensagem}"

        class Meta:
            verbose_name = "Feedback"
            verbose_name_plural = "Feedbacks"
class Cidade(models.Model):
        cidade = models.CharField(max_length=100, verbose_name="Cidade")
        def __str__(self):
            return f"{self.cidade}"
        class Meta:
            verbose_name = "Cidade"
            verbose_name_plural = "Cidades"

class Estado(models.Model):
        cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)
        estado = models.CharField(max_length=100, verbose_name="Estado")
        def __str__(self):
            return f"{self.estado}"
        class Meta:
            verbose_name = "Estado"
            verbose_name_plural = "Estados"
class Ongs(models.Model):
        nome_da_organizacao = models.CharField(max_length=200)
        descricao = models.TextField(help_text="")
        cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)
        estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True)
        categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
        contato = models.IntegerField()
        horario_de_funcionamento = models.TimeField()
        endereco = models.CharField(max_length=200, verbose_name="Endereço")
        def __str__(self):
            return f"{self.descricao}"
        class Meta:
            verbose_name = "Ong"
            verbose_name_plural = "Ongs"
class Pessoa(models.Model):
        nome = models.CharField(max_length=200)
        categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
        prazo =models.TextField(help_text="",null=True, blank=True)
        titulo = models.TextField(help_text="")
        descricao = models.TextField(help_text="")
        imagem = models.ImageField(upload_to='pessoas/', null=True, blank=True, verbose_name="Imagem")  
        contato = models.IntegerField()
        def __str__(self):
            if self.mostrar_nome:
                return f"{self.nome}"
            return "Anônimo"

        class Meta:
            verbose_name = "PessoaOng"
            verbose_name_plural = "PessoasOngs"

class Solicitacao(models.Model):
        nome = models.CharField(max_length=200)
        categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
        prazo =models.TextField(help_text="",null=True, blank=True)
        titulo = models.TextField(help_text="")
        descricao = models.TextField(help_text="")
        imagem = models.ImageField(upload_to='pessoas/', null=True, blank=True, verbose_name="Imagem")  
        def __str__(self):
            if self.mostrar_nome:
                return f"{self.nome}"
            return "Anônimo"

        class Meta:
            verbose_name = "Solicitacao"
            verbose_name_plural = "Solicitacoes"