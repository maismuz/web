from django.shortcuts import render

def homedoa(request):
    return render(request, 'homedoa.html')  # Certifique-se de que o nome do template está correto

def instrucoes(request):
    return render(request, 'instrucoes.html')  # Certifique-se de que o template existe
def doacao(request):
    return render(request, 'doacao.html') 
def login(request):
    return render(request, 'login.html') 
def ongs(request):
    return render(request, 'ongs.html') 
def doador(request):
    return render(request, 'doador.html') 