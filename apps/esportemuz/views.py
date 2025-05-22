from apps.esportemuz.forms import *
from django.views.generic import TemplateView
from typing import Any

# Create your views here.
class IndexView(TemplateView):
    template_name = 'esportemuz/pages/index.html'

class EquipeView(TemplateView):
    template_name = 'esportemuz/pages/equipe.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = EquipeForm()
        
        return context

class CampeonatoView(TemplateView):
    template_name = 'esportemuz/pages/campeonato.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CampeonatoForm()
        
        return context