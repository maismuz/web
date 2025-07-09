from django.shortcuts import render
from .models import Denuncia

def index(request):
    # denuncias_recentes = Denuncia.objects.order_by('-data_ocorrencia')[:5]
    # total_denuncias = Denuncia.objects.count()
    # total_pendentes = Denuncia.objects.filter(status='pendente').count()
    # total_resolvidas = Denuncia.objects.filter(status='resolvido').count()

    # contexto = {
    #     'denuncias_recentes': denuncias_recentes,
    #     'total_denuncias': total_denuncias,
    #     'total_pendentes': total_pendentes,
    #     'total_resolvidas': total_resolvidas,
    # }

    return render(request, 'homereclamemuz.html')

def listar_denuncias(request):
    #denuncias = Denuncia.objects.all()
    return render(request, 'denuncias.html')
