from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    email = forms.CharField(
        label=_("E-mail"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control"
            }
        ),
        localize=True
    )
    password = forms.CharField(
        label=_("Parol"),
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control"
            }
        ),
        localize=True
    )


class PasswordUpdateForm(forms.Form):
    old_password = forms.CharField(
        label=_("Eski parol"),
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control"
            }
        ),
        localize=True
    )
    password = forms.CharField(
        label=_("Yangi parol"),
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control"
            }
        ),
        localize=True
    )
    password_confirm = forms.CharField(
        label=_("Parolni tasdiqlang"),
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control"
            }
        ),
        localize=True
    )



class PasswordForm(forms.Form):
    password = forms.CharField(
        label=_("Parol"),
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control"
            }
        ),
        localize=True
    )
    password_confirm = forms.CharField(
        label=_("Parolni tasdiqlang"),
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control"
            }
        ),
        localize=True
    )
