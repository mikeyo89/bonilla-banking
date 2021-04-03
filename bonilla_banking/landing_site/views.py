from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin

from django.views import generic
from django.contrib.auth import views, authenticate, login

from .models import SupportModel
from .forms import SupportForm, AccountForm, LoginForm
from django.contrib.auth import get_user_model

class IndexView(generic.TemplateView):
    """ View for the index, or landing page, of Bonilla Banking. """
    template_name = 'index.html'

class LearnView(generic.TemplateView):
    """ View for the Learn More page of Bonilla Banking. """
    template_name = 'learn.html'

class SupportView(generic.CreateView):
    """
    View for the support page. Houses the SupportModel form.
    """
    template_name = 'support.html'

    form_class = SupportForm
    model = SupportModel

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(self.object)

    def get_success_url(self):
        return reverse('landing:success')

    def get_error_url(self):
        return reverse('landing:support')

class SuccessView(generic.TemplateView):
    """ View for success page. Landing page of the SupportView. """
    template_name = 'success.html'

class LoginView(views.LoginView):
    """
    View for the Login page. Verifies that user exists and passes that along to Dashboard view in the main_site app.
    """
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse('main:dashboard')


class SignUpView(SuccessMessageMixin, generic.CreateView):
    """
    View for the sign-up page. Verifies form data and, if successful, creates a new user in the Users model.
    """
    template_name = 'accounts/signup.html'
    model = get_user_model()
    form_class = AccountForm
    success_message = 'Account created successfully.'

    def get_success_url(self):
        return reverse('main:dashboard')
    
    def get_error_url(self):
        return reverse('landing:sign-up')