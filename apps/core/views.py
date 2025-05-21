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

def base_tabela(request):
    """
    Função de view para renderizar a página de formulários base.
    """
    return render(request, "base_tabela.html")

def base_pagina(request):
    """
    Função de view para renderizar a página de formulários base.
    """
    return render(request, "base_pagina.html")
