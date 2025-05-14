from django.db import models

class Cemiterio(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do cemitério")
    cidade = models.CharField(max_length=100, verbose_name="Cidade do cemitério")

    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Cemitério"
        verbose_name_plural = "Cemitérios"

class AreaCemiterio(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do área")
    cemiterio = models.ForeignKey(Cemiterio, on_delete = models.PROTECT)

    def __str__(self):
        return f"{self.nome}"
    class Meta:
        verbose_name = "Área do cemitério"
        verbose_name_plural = "Áreas do cemitério"

class Tumulo(models.Model):
    numero = models.CharField(max_length=100, verbose_name="Número do túmulo")
    area = models.ForeignKey(AreaCemiterio, on_delete = models.PROTECT)

    def __str__(self):
        return f"{self.numero}"
    class Meta:
        verbose_name = "Túmulo"
        verbose_name_plural = "Túmulos"

class HorarioVisitacao(models.Model):
    horario = models.CharField(max_length=100, verbose_name="Horário de visitação")
    cemiterio = models.ForeignKey(Cemiterio, on_delete = models.PROTECT)

    def __str__(self):
        return f"{self.horario}"
    class Meta:
        verbose_name = "Horário"
        verbose_name_plural = "Horários"

class Dia(models.Model):
    dia = models.CharField(max_length=3, verbose_name="Dia")
    diahorario = models.ForeignKey(HorarioVisitacao, on_delete = models.PROTECT)

    def __str__(self):
        return f"{self.dia}"
    class Meta:
        verbose_name = "Dia"
        verbose_name_plural = "Dias"

class Hora(models.Model):
    hora = models.CharField(max_length=100, verbose_name="Horas de visitação")
    diahora = models.ForeignKey(Dia, on_delete = models.PROTECT)

    def __str__(self):
        return f"{self.hora}"
    class Meta:
        verbose_name = "Hora"
        verbose_name_plural = "Horas"

class Pessoa(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    data_nasc = models.DateField(verbose_name="Data De Nascimento")
    data_fale = models.DateField(verbose_name="Data De Falecimento")
    cemiterio = models.ForeignKey(Cemiterio, on_delete=models.PROTECT,verbose_name="Cemitério onde entá esterrado(a)")
    tumulo = models.ForeignKey(Tumulo, on_delete=models.PROTECT,verbose_name="Túmulo onde está enterrado")
    def __str__(self) :
        return self.nome
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"