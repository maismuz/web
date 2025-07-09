from django.shortcuts import render, redirect
from .models import Denuncia
from .forms import DenunciaForm

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

def denuncias(request):
    # REMOVIDO: @login_required e toda a lógica de usuário
    if request.method == 'POST':
        form = DenunciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # Simplesmente salva o formulário no banco de dados
            return redirect('denuncia_sucesso') # Redireciona para uma página de sucesso
    else:
        form = DenunciaForm()
        
    return render(request, 'forms_Denuncia.html', {'form': form})

def denuncia_sucesso(request):
    """
    View para a página de agradecimento após enviar uma denúncia.
    """
    return render(request, 'denuncia_sucesso.html')
