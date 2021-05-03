from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import BankAccountsForm, BillPayForm, PaymentConnectionsForm, TransfersForm, UpdateSettingsForm, UpdateSecurityForm
from .models import BankAccountsModel, TransactionsModel, PaymentConnectionsModel, CorporationsModel
from landing_site.models import AccountModel

import random

class Authenticate(LoginRequiredMixin):
    """
    Inherit the LoginRequiredMixin and autofill some fields for quick deployment.
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

# Create your views here.
class DashboardView(Authenticate, generic.TemplateView):
    """
    View of a neat dashboard that provides information from various other models within the main_site app.
    """
    template_name = 'dashboard.html'


    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        accounts = BankAccountsModel.objects.filter(owner=self.request.user)
        transactions = TransactionsModel.objects.filter(account__owner=self.request.user)

        bills = transactions.filter(transaction_type='payment').exclude(scheduled_date=None)[:5]
        transfers = transactions.filter(transaction_type='transfer', label='debit')[:5]

        context.update(
            {
                'accounts':accounts,    'accounts_count':accounts.count(),
                'bills':bills,          'bills_count':bills.count(),
                'transfers':transfers,  'transfers_count':transfers.count()
            }
        )
        return context

class CreateAccountView(Authenticate, SuccessMessageMixin, generic.CreateView):
    """
    View for creating bank accounts -- features the BankAccount form.
    """
    template_name = 'accounts/create.html'

    form_class = BankAccountsForm
    model = BankAccountsModel
    success_message = f'Account was opened successfully!'

    def latest_account_number(self):
        last = BankAccountsModel.objects.all().order_by('account_number').last()

        if not last:
            return 1000000 + random.randint(1, 1000)

        return last.account_number + random.randint(1, 100)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.account_number = self.latest_account_number()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('main:accounts')

class AccountsView(Authenticate, generic.TemplateView):
    """
    View of all current accounts tied to logged-in user.
    """
    template_name = 'accounts/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'pk' in context:
            account = BankAccountsModel.objects.filter(owner=self.request.user).get(pk=str(context['pk']))

            transactions = TransactionsModel.objects.filter(account__account_number=account.account_number, scheduled_date=None).order_by('-date_created')
            account.account_number = str(account.account_number)[-4:]
            context.update({'account':account})
            context.update({'transactions':transactions}) if transactions.count() > 0 else None
        else:
            accounts = BankAccountsModel.objects.filter(owner=self.request.user)
            context.update({'accounts':accounts, 'accounts_count':accounts.count()})

        return context

class CreateBillView(Authenticate, SuccessMessageMixin, generic.CreateView):
    """
    View for the creation of Bill Pay & contains the BillPay form.
    """
    template_name = 'bills/create.html'
    success_message = f'Bill payment successful!'

    model = TransactionsModel
    form_class = BillPayForm

    def get_form_kwargs(self):
        kwargs = super(CreateBillView, self).get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs

    def form_valid(self, form):
        account = BankAccountsModel.objects.get(pk=form.instance.account.pk)

        if form.instance.scheduled_date is None:
            if account.balance < form.instance.amount:
                messages.add_message(self.request, messages.ERROR, f'Account balance not enough!\nCurrent balance: ${account.balance}')
                return self.form_invalid(form)

            account.balance -= form.instance.amount
            account.save()
            form.instance.description = f'Bill payment of ${form.instance.amount} to {form.instance.destination} on the {form.instance.account} account.'
        else:
            form.instance.description = f'Bill payment of ${form.instance.amount} to {form.instance.destination} scheduled for {form.instance.scheduled_date} on the {form.instance.account} account.'
        
        form.instance.new_balance = account.balance
        form.instance.transaction_type = 'payment'
        form.instance.label = 'debit'

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:bills')
    
    def get_error_url(self):
        return reverse('main:create-bill')

class CreateRecipientView(Authenticate, SuccessMessageMixin, generic.CreateView):
    """
    View of the connection creation page between a user and a recipient.
    """
    template_name = 'recipients/create.html'
    success_message = 'Recipient registered succesfully!'

    model = PaymentConnectionsModel
    form_class = PaymentConnectionsForm

    def get_form_kwargs(self):
        kwargs = super(CreateRecipientView, self).get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:bills')

class BillsView(Authenticate, SuccessMessageMixin, generic.TemplateView):
    """
    View for upcoming bills and Corporation registration management.
    """
    template_name = 'bills/view.html'
    model = TransactionsModel
    success_message = 'Bill successfully canceled!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        bills = TransactionsModel.objects.filter(account__owner=self.request.user, transaction_type='payment').exclude(scheduled_date=None).order_by('-date_created')
        connections = PaymentConnectionsModel.objects.filter(user=self.request.user).order_by('-date_created')

        if connections.count() > 0:
            context.update({'connections':connections})

        if bills.count() > 0:
            context.update({'bills':bills})

        return context

class DeleteBillView(Authenticate, SuccessMessageMixin, generic.DeleteView):
    """
    View of a specific bill to be removed/canceled.
    """
    template_name = 'bills/delete.html'
    model = TransactionsModel
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'pk' in self.kwargs:
            bill = TransactionsModel.objects.get(pk=self.kwargs.get('pk'))
            balance = BankAccountsModel.objects.get(pk=bill.account.pk).balance
            context.update({'bill':bill, 'balance': balance})
        
        return context
    
    def form_valid(self, form):
       return super().form_valid(form)
    
    def get_success_url(self):
        messages.add_message(self.request, messages.ERROR, 'Bill canceled succesfully.')
        return reverse('main:bills')

class CreateTransferView(Authenticate, SuccessMessageMixin, generic.CreateView):
    """
    View of the CreateTransfer form to initiate transfers.
    """
    template_name = 'transfers/create.html'
    success_message = 'Transfer was successful.'

    model = TransactionsModel
    form_class = TransfersForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs

    def form_valid(self, form):
        # From transacation.
        from_account = BankAccountsModel.objects.filter(owner__email=self.request.user).get(pk=form.instance.account.pk)
        to_account = BankAccountsModel.objects.filter(owner__email=self.request.user).get(name=str(form.instance.destination).split('-')[0][:-1])

        if from_account.balance < form.instance.amount:
            messages.add_message(self.request, messages.ERROR, f'The "From" account balance not enough for the transfer!\nCurrent balance: ${from_account.balance}. Transfer amount: ${form.instance.amount}')
            return self.form_invalid(form)

        from_account.balance -= form.instance.amount
        from_account.save()

        form.instance.origin = form.instance.account
        form.instance.new_balance = from_account.balance
        form.instance.transaction_type = 'transfer'
        form.instance.description = f'Transfer from {form.instance.origin} account to the {form.instance.destination} account of the amount ${form.instance.amount}.'
        form.instance.label = 'debit'

        # To transaction.
        recipient = TransactionsModel()
        recipient.account = to_account
        recipient.destination = form.instance.origin
        recipient.amount = form.instance.amount
        to_account.balance += form.instance.amount
        to_account.save()

        recipient.origin = form.instance.destination
        recipient.new_balance = to_account.balance
        recipient.transaction_type = 'transfer'
        recipient.description = f'Transfer from {form.instance.origin} account to the {form.instance.destination} account of the amount ${form.instance.amount}.'
        recipient.label = 'credit'
        recipient.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('main:transfers')
    
    def get_error_url(self):
        return reverse('main:create-transfers')

class TransfersView(Authenticate, generic.TemplateView):
    """
    View of the transfers page consisting of all transfers made.
    """
    template_name = 'transfers/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transfers = TransactionsModel.objects.filter(account__owner=self.request.user, transaction_type='transfer', label='debit').order_by('-date_created')
        context.update({'transfers':transfers})

        return context

class ProfileView(Authenticate, generic.TemplateView):
    """
    View of a user's profile and settings.
    """
    template_name = 'profile/view.html'

class UpdateSettingsView(Authenticate, SuccessMessageMixin, generic.UpdateView):
    """
    View of a profile and settings -- for editing/updating purposes.
    """
    template_name = 'profile/edit-settings.html'
    success_message = 'Profile settings updated succesfully!'

    model = AccountModel
    form_class = UpdateSettingsForm

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:profile')
    
    def get_error_url(self):
        return reverse('main:update-settings')
    
    def get_object(self):
        return get_object_or_404(AccountModel, pk=self.request.user.pk)

class UpdateSecurityView(Authenticate, SuccessMessageMixin, generic.UpdateView):
    """
    View of a profile and settings -- for editing/updating purposes.
    """
    template_name = 'profile/edit-security.html'
    success_message = 'Security settings updated succesfully!'

    model = AccountModel
    form_class = UpdateSecurityForm

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:profile')
    
    def get_error_url(self):
        return reverse('main:update-security')
    
    def get_object(self):
        return get_object_or_404(AccountModel, pk=self.request.user.pk)
