from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.core.exceptions import ValidationError
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count

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
    """Main homepage view."""
    context = {
        'total_motoristas': Motorista_MoveMuz.objects.filter(ativo=True).count(),
        'total_veiculos': Veiculo.objects.filter(disponivel=True).count(),
        'total_viagens_hoje': Viagem.objects.filter(
            data_viagem__date=timezone.now().date()
        ).count(),
        'horarios_ativos': HorarioTransporte.objects.filter(ativo=True).count(),
    }
    return render(request, 'movemuz/homepage.html', context)


def forms_demo_view(request):
    """
    Demo page showing different form field types.
    Educational purpose only - not linked to actual models.
    """
    return render(request, 'movemuz/base_forms.html')


def base_page_view(request):
    """Base page template view."""
    return render(request, 'movemuz/base_pagina.html')


class BaseTableMixin:
    """Mixin for common table view functionality."""
    
    template_name = 'movemuz/base_tabela.html'
    context_object_name = 'objects'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'model_name': self.model.__name__,
            'verbose_name': self.model._meta.verbose_name,
            'verbose_name_plural': self.model._meta.verbose_name_plural,
            'form_add': self.form_class(),
            'fields': self._get_display_fields(),
            'has_foto': self._has_image_field(),
        })
        return context
    
    def _get_display_fields(self):
        """Get fields to display in table, excluding technical fields."""
        exclude_fields = ['id', 'data_cadastro', 'data_criacao', 'atualizado_em']
        return [
            field.name for field in self.model._meta.fields 
            if field.name not in exclude_fields
        ]
    
    def _has_image_field(self):
        """Check if model has image fields."""
        image_fields = ['foto', 'imagem', 'escudo']
        return any(
            field.name in image_fields 
            for field in self.model._meta.fields
        )


@method_decorator(csrf_protect, name='dispatch')
class GenericTableView(BaseTableMixin, ListView):
    """Generic table view with CRUD operations via AJAX/modals."""
    
    def post(self, request, *args, **kwargs):
        """Handle POST requests for CRUD operations."""
        try:
            action = request.POST.get('action')
            
            if action == 'create':
                return self._handle_create(request)
            elif action == 'update':
                return self._handle_update(request)
            elif action == 'delete':
                return self._handle_delete(request)
            else:
                messages.error(request, 'Ação inválida.')
                
        except ValidationError as e:
            messages.error(request, f'Erro de validação: {e}')
        except Exception as e:
            messages.error(request, f'Erro inesperado: {e}')
            
        return redirect(request.path)
    
    @transaction.atomic
    def _handle_create(self, request):
        """Handle object creation."""
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                obj = form.save()
                messages.success(
                    request, 
                    f'{self.model._meta.verbose_name} "{obj}" criado com sucesso.'
                )
            except Exception as e:
                messages.error(request, f'Erro ao criar: {e}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        return redirect(request.path)
    
    @transaction.atomic
    def _handle_update(self, request):
        """Handle object update."""
        obj_id = request.POST.get('object_id')
        if not obj_id:
            messages.error(request, 'ID do objeto não fornecido.')
            return redirect(request.path)
            
        try:
            obj = get_object_or_404(self.model, pk=obj_id)
            form = self.form_class(request.POST, request.FILES, instance=obj)
            
            if form.is_valid():
                updated_obj = form.save()
                messages.success(
                    request,
                    f'{self.model._meta.verbose_name} "{updated_obj}" atualizado com sucesso.'
                )
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar: {e}')
            
        return redirect(request.path)
    
    @transaction.atomic
    def _handle_delete(self, request):
        """Handle object deletion."""
        obj_id = request.POST.get('object_id')
        if not obj_id:
            messages.error(request, 'ID do objeto não fornecido.')
            return redirect(request.path)
            
        try:
            obj = get_object_or_404(self.model, pk=obj_id)
            obj_name = str(obj)
            obj.delete()
            messages.success(
                request,
                f'{self.model._meta.verbose_name} "{obj_name}" excluído com sucesso.'
            )
        except Exception as e:
            messages.error(request, f'Erro ao excluir: {e}')
            
        return redirect(request.path)


# Specific table views for each model
class MotoristaTableView(GenericTableView):
    model = Motorista_MoveMuz
    form_class = MotoristaForm


class CombustivelTableView(GenericTableView):
    model = Combustivel
    form_class = CombustivelForm


class TipoVeiculoTableView(GenericTableView):
    model = TipoVeiculo
    form_class = TipoVeiculoForm


class VeiculoTableView(GenericTableView):
    model = Veiculo
    form_class = VeiculoForm


class LocalTableView(GenericTableView):
    model = Local
    form_class = LocalForm


class EscalaVeiculoTableView(GenericTableView):
    model = EscalaVeiculo
    form_class = EscalaVeiculoForm


class HorarioTransporteTableView(GenericTableView):
    model = HorarioTransporte
    form_class = HorarioTransporteForm


class ViagemTableView(GenericTableView):
    model = Viagem
    form_class = ViagemForm


class PassageiroTableView(GenericTableView):
    model = Passageiro
    form_class = PassageiroForm


class PontoTableView(GenericTableView):
    model = Ponto
    form_class = PontoForm


class ParadaTableView(GenericTableView):
    model = Parada
    form_class = ParadaForm


class OcupacaoVeiculoTableView(GenericTableView):
    model = OcupacaoVeiculo
    form_class = OcupacaoVeiculoForm


# Function-based views for backward compatibility and special cases
@require_http_methods(["GET", "POST"])
def motorista_detail_view(request, pk):
    """Detailed view for a specific driver."""
    motorista = get_object_or_404(Motorista_MoveMuz, pk=pk)
    
    context = {
        'motorista': motorista,
        'viagens_recentes': motorista.viagens.filter(
            data_viagem__gte=timezone.now().date() - timezone.timedelta(days=30)
        )[:10],
        'escalas_ativas': motorista.escalas.filter(
            data_fim__gte=timezone.now().date()
        ),
    }
    return render(request, 'movemuz/motorista_detail.html', context)


@require_http_methods(["GET"])
def veiculo_detail_view(request, pk):
    """Detailed view for a specific vehicle."""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    
    context = {
        'veiculo': veiculo,
        'horarios': veiculo.horarios.filter(ativo=True),
        'escalas_recentes': veiculo.escalas.filter(
            data_inicio__gte=timezone.now().date() - timezone.timedelta(days=30)
        )[:10],
    }
    return render(request, 'movemuz/veiculo_detail.html', context)


@require_http_methods(["GET"])
def viagem_detail_view(request, pk):
    """Detailed view for a specific trip."""
    viagem = get_object_or_404(Viagem, pk=pk)
    
    context = {
        'viagem': viagem,
        'passageiros': viagem.passageiros.all(),
        'ocupacao': getattr(viagem, 'ocupacao', None),
    }
    return render(request, 'movemuz/viagem_detail.html', context)


# Dashboard and reporting views
@require_http_methods(["GET"])
def dashboard_view(request):
    """Dashboard with statistics and charts."""
    hoje = timezone.now().date()
    
    context = {
        'stats': {
            'motoristas_ativos': Motorista_MoveMuz.objects.filter(ativo=True).count(),
            'veiculos_disponiveis': Veiculo.objects.filter(disponivel=True).count(),
            'viagens_hoje': Viagem.objects.filter(data_viagem=hoje).count(),
            'horarios_ativos': HorarioTransporte.objects.filter(ativo=True).count(),
        },
        'viagens_recentes': Viagem.objects.filter(
            data_viagem__gte=hoje - timezone.timedelta(days=7)
        ).select_related('motorista', 'horario_transporte')[:10],
        'motoristas_mais_ativos': Motorista_MoveMuz.objects.annotate(
            total_viagens=Count('viagens')
        ).filter(ativo=True).order_by('-total_viagens')[:5],
    }
    return render(request, 'movemuz/dashboard.html', context)


# API-like views for AJAX requests
@require_http_methods(["GET"])
def api_motoristas_disponiveis(request):
    """Return available drivers as JSON."""
    from django.http import JsonResponse
    
    motoristas = Motorista_MoveMuz.objects.filter(
        ativo=True,
        cnh_valida=True
    ).values('id', 'nome', 'categoria_cnh')
    
    return JsonResponse({
        'motoristas': list(motoristas)
    })


@require_http_methods(["GET"])
def api_veiculos_disponiveis(request):
    """Return available vehicles as JSON."""
    from django.http import JsonResponse
    
    veiculos = Veiculo.objects.filter(
        disponivel=True
    ).values('id', 'marca', 'modelo', 'placa', 'capacidade')
    
    return JsonResponse({
        'veiculos': list(veiculos)
    })
