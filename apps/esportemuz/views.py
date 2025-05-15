from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'esportemuz/pages/index.html'

class EquipeView(TemplateView):
    template_name = 'esportemuz/pages/equipe.html'

class CampeonatoView(TemplateView):
    template_name = 'esportemuz/pages/campeonato.html'