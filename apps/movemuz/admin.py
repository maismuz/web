from django.contrib import admin
from .models import (
    Motorista_MoveMuz, Combustivel, TipoVeiculo, Veiculo, Local,
    EscalaVeiculo, HorarioTransporte, Viagem, Passageiro, Ponto,
    Parada, OcupacaoVeiculo
)

admin.site.register(Motorista_MoveMuz)
admin.site.register(Combustivel)
admin.site.register(TipoVeiculo)
admin.site.register(Veiculo)
admin.site.register(Local)
admin.site.register(EscalaVeiculo)
admin.site.register(HorarioTransporte)
admin.site.register(Viagem)
admin.site.register(Passageiro)
admin.site.register(Ponto)
admin.site.register(Parada)
admin.site.register(OcupacaoVeiculo)