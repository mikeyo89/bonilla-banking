from django.shortcuts import render
from django.views import generic

class IndexView(generic.TemplateView):
    template_name = 'index.html'

class LearnView(generic.TemplateView):
    template_name = 'learn.html'

class SupportView(generic.TemplateView):
    template_name = 'support.html'

class LoginView(generic.TemplateView):
    template_name = 'login.html'

class SignUpView(generic.CreateView):
    template_name = 'signup.html'