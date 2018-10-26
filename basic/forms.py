from django import forms
from basic.models import SubscribedEmail, EmailTemplates


class EmailSubscriberAddForm(forms.ModelForm):
    email_address = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'spam.free@yourmail.com'}))

    class Meta:
        model = SubscribedEmail
        fields = ['email_address']

    def clean_email_address(self):
        if SubscribedEmail.objects.filter(email_address=self.cleaned_data.get('email_address', None)).count() > 0:
            raise forms.ValidationError("User with this email already exists.")

        return self.cleaned_data.get('email_address')


class EmailTemplatesUploadForm(forms.ModelForm):
    templates = forms.FileField()

    class Meta:
        model = EmailTemplates
        fields = ['templates']
