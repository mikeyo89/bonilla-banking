from django import forms
from .models import SupportModel

# Enter your forms here.
class SupportForm(forms.ModelForm):
    """
    Form for the support model. Live site responses will be processed with this model.
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