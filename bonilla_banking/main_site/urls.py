from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth import views

app_name = 'main_site'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    # Bank Account Urls
    path('accounts/open/', CreateAccountView.as_view(), name='open-account'),
    path('accounts/', AccountsView.as_view(), name='accounts'),
    path('accounts/<int:pk>/', AccountsView.as_view(), name='accounts'),

    # Bill Pay Urls
    path('bill-pay/start/', CreateBillView.as_view(), name='create-bill'),
    path('bill-pay/', BillsView.as_view(), name='bills'),
    path('bill-pay/<int:pk>/', DeleteBillView.as_view(), name='view-bill'),

    path('bill-pay/open-connection/', CreateRecipientView.as_view(), name='create-connection'),

    # Fund Transfer Urls
    path('transfers/create-transfer/', CreateTransferView.as_view(), name='create-transfer'),
    path('transfers/view-all/', TransfersView.as_view(), name='transfers'),

    # Profile Management
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit-settings/', UpdateSettingsView.as_view(), name='update-settings'),
    path('profile/edit-security/', UpdateSecurityView.as_view(), name='update-security'),

    path('logout/', views.LogoutView.as_view(template_name='logout.html'), name='logout')
]