from django.contrib import admin
from .models import Paciente, Solicitacao, Agendamento

admin.site.register(Paciente)
admin.site.register(Solicitacao)
admin.site.register(Agendamento)
