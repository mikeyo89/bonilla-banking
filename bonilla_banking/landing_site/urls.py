from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('learn-more/', LearnView.as_view(), name='learn'),
    path('support/', SupportView.as_view(), name='support'),
    path('login/', LoginView.as_view(), name='login'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
]