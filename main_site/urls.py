from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth import views

app_name = 'main_site'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('logout/', views.LogoutView.as_view(template_name='logout.html'), name='logout')
]