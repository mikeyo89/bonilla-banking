from django import forms
from .models import SupportModel, AccountModel
from django.contrib.auth import get_user_model

# Enter your forms here.
class SupportForm(forms.ModelForm):
    """
    Form for the support model. Live site responses will be processed with this form.
    """

    def __init__(self, *args, **kwargs):
        super(SupportForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget = forms.TextInput()
        self.fields['first_name'].label = 'First Name'
        self.fields['first_name'].required = True

        self.fields['last_name'].widget = forms.TextInput()
        self.fields['last_name'].label = 'Last Name'
        self.fields['last_name'].required = True

        self.fields['email'].widget = forms.EmailInput()
        self.fields['email'].label = 'Email Address'
        self.fields['email'].required = True

        self.fields['subject'].widget = forms.TextInput()
        self.fields['subject'].label = 'Subject'
        self.fields['subject'].required = True

        self.fields['message'].widget = forms.Textarea(attrs={
            'class': 'materialize-textarea'
        })
        self.fields['message'].label = 'Message'
        self.fields['message'].required = True

    class Meta:
        model = SupportModel
        exclude = ['date_received']

class AccountForm(forms.ModelForm):
    """
    Form for the account model. All regular user accounts are made with this form.
    """

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget = forms.EmailInput()
        self.fields['email'].label = 'Email Address'
        self.fields['email'].required = True

        self.fields['username'].widget = forms.TextInput()
        self.fields['username'].label = 'Username'
        self.fields['username'].required = True

        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].label = 'Password'
        self.fields['password'].required = True

        self.fields['first_name'].widget = forms.TextInput()
        self.fields['first_name'].label = 'First Name'
        self.fields['first_name'].required = True

        self.fields['last_name'].widget = forms.TextInput()
        self.fields['last_name'].label = 'Last Name'
        self.fields['last_name'].required = True

        self.fields['phone_number'].widget = forms.NumberInput()
        self.fields['phone_number'].label = 'Phone Number'
        self.fields['phone_number'].required = True

        self.fields['date_of_birth'].widget = forms.DateInput(attrs={
            'class': 'datepicker'
        })
        self.fields['date_of_birth'].label = 'Date of Birth'
        self.fields['date_of_birth'].required = True

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'date_of_birth']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user