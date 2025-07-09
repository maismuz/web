<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelform_factory
from .models import (
    Motorista_MoveMuz, Combustivel, TipoVeiculo, Veiculo, Local,
    EscalaVeiculo, HorarioTransporte, Viagem, Passageiro, Ponto,
    Parada, OcupacaoVeiculo
)
from .forms import (
    MotoristaForm, CombustivelForm, TipoVeiculoForm, VeiculoForm, LocalForm,
    EscalaVeiculoForm, HorarioTransporteForm, ViagemForm, PassageiroForm, PontoForm,
    ParadaForm, OcupacaoVeiculoForm
)

def homepage_view(request):
    return render(request, 'homepage.html')

# --- Views for base_forms.html (Full Forms Page) ---
def full_forms_view(request):
    """
    Renders a page with all types of form fields.
    This uses a placeholder form, not directly linked to models.
    """
    return render(request, 'base_forms.html')

# --- Views for base_tabela.html (Table Views with Modals) ---

# Generic function to handle listing, adding, editing, and deleting for any model
def generic_table_view(request, model_name, form_class):
    model = globals()[model_name] # Get the model class from its name
    form_add = form_class()
=======
from django.shortcuts import render, redirect
from .forms import VeiculoForm
from .models import TipoVeiculo, Combustivel, Veiculo
from datetime import datetime
>>>>>>> c82908cbfa9471dfd69a3d07cc441a2dfeda63f0

    if request.method == 'POST':
        if 'add_record' in request.POST:
            form_add = form_class(request.POST, request.FILES)
            if form_add.is_valid():
                form_add.save()
                return redirect(request.path)
        elif 'edit_record' in request.POST:
            instance_id = request.POST.get('instance_id')
            instance = get_object_or_404(model, pk=instance_id)
            form_edit = form_class(request.POST, request.FILES, instance=instance)
            if form_edit.is_valid():
                form_edit.save()
                return redirect(request.path)
        elif 'delete_record' in request.POST:
            instance_id = request.POST.get('instance_id')
            instance = get_object_or_404(model, pk=instance_id)
            instance.delete()
            return redirect(request.path)

    objects = model.objects.all()
    # Prepare edit forms for each object (for modals)
    edit_forms = {obj.pk: form_class(instance=obj) for obj in objects}

    context = {
        'objects': objects,
        'form_add': form_add,
        'edit_forms': edit_forms,
        'model_name': model_name,
        'verbose_name_plural': model._meta.verbose_name_plural,
        'fields': [field.name for field in model._meta.fields if field.name not in ['id', 'foto']], # Exclude 'id' and 'foto' for simple display
        'has_foto': 'foto' in [f.name for f in model._meta.fields], # Check if model has a 'foto' field
    }
<<<<<<< HEAD
    return render(request, 'movemuz_base_tabela.html', context)


# Specific views for each model, using the generic table view
def motoristas_table_view(request):
    return generic_table_view(request, 'Motorista_MoveMuz', MotoristaForm)

def combustiveis_table_view(request):
    return generic_table_view(request, 'Combustivel', CombustivelForm)

def tipo_veiculos_table_view(request):
    return generic_table_view(request, 'TipoVeiculo', TipoVeiculoForm)

def veiculos_table_view(request):
    return generic_table_view(request, 'Veiculo', VeiculoForm)

def locais_table_view(request):
    return generic_table_view(request, 'Local', LocalForm)

def escala_veiculos_table_view(request):
    return generic_table_view(request, 'EscalaVeiculo', EscalaVeiculoForm)

def horario_transportes_table_view(request):
    return generic_table_view(request, 'HorarioTransporte', HorarioTransporteForm)

def viagens_table_view(request):
    return generic_table_view(request, 'Viagem', ViagemForm)

def passageiros_table_view(request):
    return generic_table_view(request, 'Passageiro', PassageiroForm)

def pontos_table_view(request):
    return generic_table_view(request, 'Ponto', PontoForm)

def paradas_table_view(request):
    return generic_table_view(request, 'Parada', ParadaForm)

def ocupacao_veiculos_table_view(request):
    return generic_table_view(request, 'OcupacaoVeiculo', OcupacaoVeiculoForm)


# --- View for base_pagina.html (Base Page Template) ---
def base_page_view(request):
    return render(request, 'base_pagina.html')
=======
    return render(request, 'cadastro_veiculo.html', context)

def lista_veiculos(request):
    veiculos = Veiculo.objects.all().order_by('modelo') # Recupera todos os veículos do banco de dados, ordenados por modelo
    context = {
        'veiculos': veiculos,
    }
    return render(request, 'listar_veiculos.html', context)
>>>>>>> c82908cbfa9471dfd69a3d07cc441a2dfeda63f0
