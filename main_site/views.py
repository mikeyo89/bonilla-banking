from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from landing_site.models import AccountModel

# Create your views here.
class DashboardView(LoginRequiredMixin, generic.TemplateView):
    """
    View of a neat dashboard that provides information from various other models within the main_site app.
    """
    template_name = 'dashboard.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'