from django.shortcuts import render

def index(request):
    """
    Função de view para renderizar a página inicial do site.
    """
    return render(request, "index.html")
