from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        ),
        localize=True
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        ),
        localize=True
    )
