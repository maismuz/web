from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    data_nasc = models.DateField(verbose_name="Data De Nascimento")
    data_fale = models.DateField(verbose_name="Data De Falecimento")
    #cemiterio = models.ForeignKey(Cemiterio, on_delete=models.PROTECT,verbose_name="Cemitério onde entá esterrado(a)")
    #tumulo = models.ForeignKey(Tumulo, on_delete.PROTECT,verbose_name="Túmulo enterrado")
    def __str__(self) :
        return self.nome
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
