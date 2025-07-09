from typing import Any
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'esportemuz/pages/home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['campeonatos_recentes'] = []
        context['proximas_partidas'] = []

        return context

class CampeonatoListView(TemplateView):
    template_name = 'esportemuz/pages/campeonato_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['campeonatos'] = []

        return context
    
class EquipeListView(TemplateView):
    template_name = 'esportemuz/pages/equipe_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['equipes'] = []

        return context