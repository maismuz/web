from django.db import models

<<<<<<< HEAD
class Motorista(models.Model):
    nome = models.CharField("Nome completo", max_length=100)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    telefone = models.CharField("Telefone", max_length=15, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)
    cnh_numero = models.CharField("Número da CNH", max_length=20, unique=True)
    data_nascimento = models.DateField("Data de nascimento")
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Motorista"
        verbose_name_plural = "Motoristas"
        ordering = ['nome']

    def __str__(self):
        return self.nome
=======
class Combustivel(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Combustível'
        verbose_name_plural = 'Combustíveis'
        db_table = 'combustivel'


class TipoVeiculo(models.Model):    
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de Veículo'
        verbose_name_plural = 'Tipos de Veículos'
        db_table = 'tipo_veiculo'


class Veiculo(models.Model):
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=7, unique=True)
    cor = models.CharField(max_length=100)
    ano_fabricacao = models.IntegerField()
    foto = models.ImageField(upload_to='veiculos/')
    tipo = models.ForeignKey(TipoVeiculo, on_delete=models.PROTECT, related_name='veiculos')
    combustivel = models.ForeignKey(Combustivel, on_delete=models.PROTECT, related_name='veiculos')

    def __str__(self):
        return f"{self.modelo} - {self.ano_fabricacao}"

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        db_table = 'veiculo'
<<<<<<< HEAD
>>>>>>> d7ec35e (Adcionando models e admin)
=======
        
class Motorista(models.Model):
    nome = models.CharField("Nome completo", max_length=100)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    telefone = models.CharField("Telefone", max_length=15, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)
    cnh_numero = models.CharField("Número da CNH", max_length=20, unique=True)
    data_nascimento = models.DateField("Data de nascimento")
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Motorista"
        verbose_name_plural = "Motoristas"
        ordering = ['nome']

    def __str__(self):
        return self.nome
<<<<<<< HEAD
>>>>>>> f40509e ([Fix] Corrigir problemas na aplicação MoveMuz (#217))
=======

class Local(models.Model):
    nome = models.CharField("Nome do local", max_length=100, unique=True)
    endereco = models.CharField("Endereço", max_length=200, blank=True, null=True)
    cidade = models.CharField("Cidade", max_length=100, blank=True, null=True)
    estado = models.CharField("Estado", max_length=2, blank=True, null=True)

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Viagem(models.Model):
    motorista = models.ForeignKey(Motorista, verbose_name="motorista", on_delete=models.CASCADE)
    origem = models.ForeignKey(Local, verbose_name="Origem", on_delete=models.CASCADE, related_name='viagens_origem')
    destino = models.ForeignKey(Local, verbose_name="Destino", on_delete=models.CASCADE, related_name='viagens_destino')
    data_saida = models.DateTimeField("Data e hora de saída")
    data_chegada = models.DateTimeField("Previsão de chegada", blank=True, null=True)
    finalidade = models.CharField("Finalidade da viagem", max_length=200, blank=True, null=True)
    observacoes = models.TextField("Observações", blank=True, null=True)

    class Meta:
        verbose_name = "Viagem"
        verbose_name_plural = "Viagens"
        ordering = ['-data_saida']

    def __str__(self):
        return f"{self.origem} → {self.destino} ({self.data_saida.strftime('%d/%m/%Y')})"
>>>>>>> 4b0fddc ([Feature] Gerenciar viagens (#188))
