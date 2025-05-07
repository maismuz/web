from django.shortcuts import render

def homepage(request):
    """
    Função de view para renderizar a página inicial do site.
    """
    return render(request, "homepage.html")

def base_forms(request):
    """
    Função de view para renderizar a página de formulários base.
    """
    return render(request, "base_forms.html")
