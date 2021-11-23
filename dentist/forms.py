from django import forms
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from mydentist.var import *


class QueryForm(forms.Form):

    reason = forms.CharField(
        label=_("Borish sababi"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("Sababini kiriting")
            }
        ),
        max_length=255,
        localize=True
    )
    comment = forms.CharField(
        label=_("Tish shifokoriga izohlar"),
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
                'placeholder': _("Izohlaringizni kiriting")
            }
        ),
        localize=True
    )


class UserForm(forms.Form):

    first_name = forms.CharField(
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
    gender = forms.CharField(
        label=_("Jins"),
        widget=forms.Select(
            attrs={
                'class': "form-select"
            },
            choices=CHOICES['gender']
        )
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
