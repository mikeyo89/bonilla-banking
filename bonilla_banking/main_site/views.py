from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class DashboardView(generic.TemplateView):
    """
    View of a neat dashboard that provides information from various other models within the main_site app.
    """
    template_name = 'dashboard.html'