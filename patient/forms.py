from django import forms
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from .var import *


class UserForm(forms.Form):

    last_name = forms.CharField(
        label=_("Familiya"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Familiyangiz")
            }
        ),
        max_length=150,
        localize=True
    )
    name = forms.CharField(
        label=_("Ism"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Ismingiz")
            }
        ),
        max_length=150,
        localize=True
    )
    email = forms.EmailField(
        label=_("Elektron manzil"),
        widget=forms.EmailInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Elektron pochtangiz")
            }
        ),
        localize=True
    )
    birth_year = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': "year_holder",
                'value': datetime.today().year
            }
        ),
        localize=True
    )
    birth_month = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': "month_holder",
                'value': MONTHS[datetime.today().month - 1]
            }
        ),
        localize=True
    )
    birth_day = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': "day_holder",
                'value': datetime.today().day
            }
        ),
        localize=True
    )
    phone_number = forms.CharField(
        label=_("Telefon raqam"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Telefon raqamingiz")
            }
        ),
        max_length=20,
        localize=True
    )
    address = forms.CharField(
        label=_("Manzil"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Manzilingiz")
            }
        ),
        max_length=150,
        localize=True
    )


class LanguageForm(forms.Form):
    language = forms.CharField(
        label=_("Til"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=[
                ('1', "O'zbekcha"),
                ('2', "Русский")
            ]
        )
    )

