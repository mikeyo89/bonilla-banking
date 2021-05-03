from django import forms
from django.db.models import OuterRef, Q
from address.forms import AddressField
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
from .models import BankAccountsModel, TransactionsModel, PaymentConnectionsModel, CorporationsModel
from landing_site.models import AccountModel

# Create your forms here.
class BankAccountsForm(forms.ModelForm):
    """
    Form for Bank Account creation.
    """
    def __init__(self, *args, **kwargs):
        super(BankAccountsForm, self).__init__(*args, **kwargs)

        self.fields['name'].widgets = forms.TextInput()
        self.fields['name'].label = 'Account Nickname'

        self.fields['account_type'].widgets = forms.Select()
        self.fields['account_type'].label = 'Account Type'
        self.fields['account_type'].object = forms.MultipleChoiceField(
            widget = forms.RadioSelect(),
            choices = BankAccountsModel.ACCOUNT_TYPE_CHOICES,
            label = 'Account Type'
        )

    class Meta:
        model = BankAccountsModel
        fields = ['name', 'account_type']

class BillPayForm(forms.ModelForm):
    """
    Form for the Bill Pay feature of Bonilla Banking.
    """
    account = forms.ModelChoiceField(queryset=BankAccountsModel.objects.all())
    destination = forms.ModelChoiceField(queryset=PaymentConnectionsModel.objects.all())

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)

        self.fields['account'].queryset = BankAccountsModel.objects.filter(owner__email=self.owner)

        self.fields['amount'].widgets = forms.TextInput()
        self.fields['amount'].label = 'Bill Amount'

        self.fields['destination'].queryset = PaymentConnectionsModel.objects.filter(user__email=self.owner)
        self.fields['destination'].label = 'Recipient'

        self.fields['scheduled_date'].widget = forms.DateInput(attrs={
            'class': 'datepicker'
        })
        self.fields['scheduled_date'].label = 'Scheduled Date'
        self.fields['scheduled_date'].required = False
        self.fields['scheduled_date'].blank = True

    class Meta:
        model = TransactionsModel
        fields = ['account', 'amount', 'destination', 'scheduled_date']

class PaymentConnectionsForm(forms.ModelForm):
    """
    Form for creation of Payment connections between our esteemed partners and our users.
    """
    corporation = forms.ModelChoiceField(queryset=CorporationsModel.objects.all())

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)

        existing_connections = PaymentConnectionsModel.objects.filter(user=self.owner)
        self.fields['corporation'].queryset = CorporationsModel.objects.filter(~Q(name__in=[connection.corporation for connection in existing_connections]))

    class Meta:
        model = PaymentConnectionsModel
        fields = ['corporation']

class TransfersForm(forms.ModelForm):
    """
    Form for the transfer of funds in between personal accounts.
    """
    account = forms.ModelChoiceField(queryset=BankAccountsModel.objects.all())
    destination = forms.ModelChoiceField(queryset=BankAccountsModel.objects.all())

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)

        self.fields['account'].queryset = BankAccountsModel.objects.filter(owner__email=self.owner)
        self.fields['account'].label = 'From'

        self.fields['destination'].queryset = BankAccountsModel.objects.filter(owner__email=self.owner)
        self.fields['destination'].label = 'To'

        self.fields['amount'].widgets = forms.TextInput()
        self.fields['amount'].label = 'Transfer Amount'

    class Meta:
        model = TransactionsModel
        fields = ['account', 'amount', 'destination']

class UpdateSettingsForm(forms.ModelForm):
    """
    Form for updating user/profile settings.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget = forms.TextInput()
        self.fields['first_name'].label = 'First Name'
        self.fields['first_name'].required = False

        self.fields['last_name'].widget = forms.TextInput()
        self.fields['last_name'].label = 'Last Name'
        self.fields['last_name'].required = False

        address = AddressField(required=False)

        self.fields['phone_number'].widget = forms.NumberInput()
        self.fields['phone_number'].label = 'Phone Number'
        self.fields['phone_number'].required = False

        self.fields['date_of_birth'].widget = forms.DateInput(attrs={
            'class': 'datepicker'
        })
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['date_of_birth'].required = False

    class Meta:
        model = AccountModel
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'date_of_birth']

class UpdateSecurityForm(forms.ModelForm):
    """
    Form for updating user security details.
    """
    password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = AccountModel
        fields = ['password']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user