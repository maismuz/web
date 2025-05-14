from django.db import models

class Paciente(models.Model):
    nome_completo = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    historico = models.TextField(blank=True, null=True)
    consentimento_lgpd = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo

class Solicitacao(models.Model):
    TIPO_CHOICES = [
        ('consulta', 'Consulta'),
        ('cirurgia', 'Cirurgia'),
        ('transporte', 'Transporte'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('analise', 'Em Análise'),
        ('agendado', 'Agendado'),
        ('concluido', 'Concluído'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    especialidade = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField()
    arquivos = models.FileField(upload_to='documentos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.paciente.nome_completo} - {self.tipo}"

class Agendamento(models.Model):
    STATUS_AGENDAMENTO = [
        ('agendado', 'Agendado'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),
    ]

    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE)
    data_hora_agendada = models.DateTimeField()
    local = models.CharField(max_length=150)
    observacoes = models.TextField(blank=True, null=True)
    status_agendamento = models.CharField(max_length=20, choices=STATUS_AGENDAMENTO, default='agendado')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.solicitacao} - {self.data_hora_agendada}"
