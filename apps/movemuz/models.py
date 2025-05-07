from django.db import models

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