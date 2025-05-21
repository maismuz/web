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

ESTADOS_BRASIL = [
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins"),
]

class Combustivel(models.Model):
    nome = models.CharField("Nome", max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Combustível'
        verbose_name_plural = 'Combustíveis'
        db_table = 'combustivel'


class TipoVeiculo(models.Model):
    nome = models.CharField("Nome", max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Tipo de Veículo'
        verbose_name_plural = 'Tipos de Veículos'
        db_table = 'tipo_veiculo'


class Veiculo(models.Model):
    modelo = models.CharField("Modelo", max_length=100)
    placa = models.CharField("Placa", max_length=7, unique=True)
    cor = models.CharField("Cor", max_length=100)
    ano_fabricacao = models.IntegerField("Ano de fabricação")
    foto = models.ImageField("Foto", upload_to='veiculos/')
    tipo = models.ForeignKey(TipoVeiculo, verbose_name="Tipo", on_delete=models.PROTECT, related_name='veiculos')
    combustivel = models.ForeignKey(Combustivel, verbose_name="Combustível", on_delete=models.PROTECT, related_name='veiculos')
    capacidade = models.PositiveIntegerField("Capacidade", help_text="Número de passageiros ou capacidade de carga", null=True, blank=True)
    condicao_manutencao = models.CharField(
        "Condição de manutenção",
        max_length=50,
        choices=[
            ("bom", "Bom"),
            ("regular", "Regular"),
            ("manutencao", "Em manutenção"),
            ("inativo", "Inativo"),
        ],
        default="bom"
    )

    def __str__(self):
        return f"{self.modelo} - {self.ano_fabricacao}"

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        db_table = 'veiculo'

class Local(models.Model):
    nome = models.CharField("Nome do local", max_length=100, unique=True)
    endereco = models.CharField("Endereço", max_length=200, blank=True, null=True)
    cidade = models.CharField("Cidade", max_length=100, blank=True, null=True)
    estado = models.CharField("Estado", max_length=2, choices=ESTADOS_BRASIL, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"
        ordering = ['nome']
        db_table = 'local'


class EscalaVeiculo(models.Model):
    veiculo = models.ForeignKey(Veiculo, verbose_name="Veículo", on_delete=models.PROTECT, related_name="escalas")
    origem = models.ForeignKey(Local, verbose_name="Origem", on_delete=models.PROTECT, related_name="escalas_origem")
    destino = models.ForeignKey(Local, verbose_name="Destino", on_delete=models.PROTECT, related_name="escalas_destino")
    horario_saida = models.DateTimeField("Horário de saída")
    horario_chegada = models.DateTimeField("Horário de chegada previsto")

    def __str__(self):
        return f"{self.veiculo} ({self.origem} → {self.destino})"

    class Meta:
        verbose_name = "Escala do Veículo"
        verbose_name_plural = "Escalas dos Veículos"
        ordering = ['-horario_saida']
        db_table = 'escala_veiculo'


class HorarioTransporte(models.Model):
    veiculo = models.ForeignKey(Veiculo, verbose_name="Veículo", on_delete=models.PROTECT)
    origem = models.ForeignKey(Local, verbose_name="Origem", on_delete=models.PROTECT, related_name="horarios_origem")
    destino = models.ForeignKey(Local, verbose_name="Destino", on_delete=models.PROTECT, related_name="horarios_destino")
    horario_partida = models.TimeField("Horário de partida")
    dias_semana = models.CharField(
        "Dias da semana",
        max_length=100,
        help_text="Ex: Segunda a sexta, Fins de semana, Todos os dias"
    )

    def __str__(self):
        return f"{self.origem} → {self.destino} ({self.horario_partida.strftime('%H:%M')})"
    
    class Meta:
        verbose_name = "Horário de Transporte"
        verbose_name_plural = "Horários de Transporte"
        db_table = 'horario_transporte'
        ordering = ['-horario_partida']


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


class Passageiro(models.Model):
    viagem = models.ForeignKey(Viagem, on_delete=models.CASCADE, related_name='passageiros')
    nome = models.CharField("Nome do passageiro", max_length=100)
    documento = models.CharField("Documento de identificação", max_length=50, blank=True, null=True)
    observacao = models.TextField("Observação", blank=True, null=True)

    class Meta:
        verbose_name = "Passageiro"
        verbose_name_plural = "Passageiros"
        db_table = 'passageiro'

    def __str__(self):
        return f"{self.nome} ({self.viagem})"

class Ponto(models.Model):
    nome = models.CharField("Nome do ponto", max_length=100)
    localizacao = models.CharField("Descrição ou endereço", max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Ponto de Embarque/Desembarque"
        verbose_name_plural = "Pontos de Embarque/Desembarque"
        ordering = ['nome']
        db_table = 'ponto'

    def __str__(self):
        return self.nome

class Parada(models.Model):
    horario_transporte = models.ForeignKey(
        'HorarioTransporte',
        verbose_name="Horário de Transporte",
        on_delete=models.CASCADE,
        related_name='paradas'
    )
    ponto = models.ForeignKey(Ponto, verbose_name="Ponto", on_delete=models.CASCADE)
    horario = models.TimeField("Horário da parada")
    passageiros_estimados = models.PositiveIntegerField("Nº de passageiros", default=0)

    class Meta:
        verbose_name = "Parada"
        verbose_name_plural = "Paradas"
        ordering = ['horario']
        db_table = 'parada'

    def __str__(self):
        return f"{self.ponto} às {self.horario} - {self.passageiros_estimados} passageiros"
